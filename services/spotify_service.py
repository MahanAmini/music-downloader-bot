import asyncio
import logging
import os
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from spotdl.types.song import Song
from spotdl.utils.spotify import SpotifyClient, SpotifyError
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, COOKIE_PATH, PROXY_URL
from spotdl.download.downloader import Downloader

SpotifyClient.init(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)

logger = logging.getLogger(__name__)

downloader_settings = {
    "output": "downloads/{artists} - {title}.{output-ext}",
    "threads": 4,
    "audio_providers": ["youtube"],
    "cookie_file": COOKIE_PATH if os.path.exists(COOKIE_PATH) else None,
}

yt_dlp_args = []
#if PROXY_URL:
#    yt_dlp_args.append(f"--proxy {PROXY_URL}")
if os.path.exists(COOKIE_PATH):
    yt_dlp_args.append(f"--cookies {COOKIE_PATH}")

if yt_dlp_args:
    downloader_settings["yt_dlp_args"] = " ".join(yt_dlp_args)

_executor = ThreadPoolExecutor(max_workers=1)
_downloader = None
_current_provider = None

def _get_downloader(provider: str) -> Downloader:
    global _downloader, _current_provider
    if _downloader is None or _current_provider != provider:
        if _downloader is not None:
            _downloader.progress_handler.close()
        downloader_settings["audio_providers"] = [provider]
        _downloader = Downloader(settings=downloader_settings)
        _current_provider = provider
    return _downloader


@dataclass
class SongMetadata:
    name: str
    artist: list[str]
    album: str
    track_id: str


def spotify_finder_service(track_id: str, provider: str = "youtube"):
    downloader = _get_downloader(provider)

    try:
        song = Song.from_url(f"https://open.spotify.com/track/{track_id}")
        metadata = SongMetadata(
            name=song.name,
            artist=song.artists,
            album=song.album_name,
            track_id=track_id,
        )
        logger.info("Spotify - track_id: %s - SongName: %s", track_id, song.name)

        try:
            song_obj, file_path = downloader.download_song(song)
        except Exception as e:
            logger.exception("Download failed for track %s: %s", track_id, e)
            file_path = None

        if file_path and os.path.exists(file_path):
            logger.info("Successfully downloaded track %s to %s from ----> s%", track_id, file_path, provider)
            return metadata, str(file_path)

        logger.info("Download failed for track %s with provider %s", track_id, provider)
        if provider != "soundcloud":
            return spotify_finder_service(track_id, provider="soundcloud")
        return None

    except SpotifyError as e:
        logger.warning("Spotify Error for track %s - Error: %s", track_id, e)
        return None
    except Exception as e:
        logger.error("Unexpected error for track %s: %s", track_id, e)
        return None


def run_spotify_finder_in_executor(loop: asyncio.AbstractEventLoop, track_id: str):
    return loop.run_in_executor(_executor, spotify_finder_service, track_id)
