import asyncio
import logging
import os
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from spotdl.types.song import Song
from spotdl.utils.spotify import SpotifyClient, SpotifyError
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,PROXY_URL,COOKIE_PATH
from spotdl.download.downloader import Downloader

SpotifyClient.init(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)

logger = logging.getLogger(__name__)

downloader_settings = {
    "output": "downloads/{artists} - {title}.{output-ext}",
    "threads": 2,
    "audio_providers": ["soundcloud"],
    "cookie_file": COOKIE_PATH if os.path.exists(COOKIE_PATH) else None,
}

yt_dlp_args = []
if PROXY_URL:
    yt_dlp_args.append(f"--proxy {PROXY_URL}")
if os.path.exists(COOKIE_PATH):
    yt_dlp_args.append(f"--cookies {COOKIE_PATH}")

if yt_dlp_args:
    downloader_settings["yt_dlp_args"] = " ".join(yt_dlp_args)

_executor = ThreadPoolExecutor(max_workers=1)
_downloader = None

def _get_downloader() -> Downloader:
    global _downloader
    if _downloader is None:
        _downloader = Downloader(settings=downloader_settings)
    return _downloader

@dataclass
class SongMetadata:
    name: str
    artist: list[str]
    album: str
    track_id: str


def spotify_finder_service(track_id: str):
    downloader = _get_downloader()

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
            return None

        if file_path and os.path.exists(file_path):
            logger.info("Successfully downloaded track %s to %s", track_id, file_path)
            return metadata, str(file_path)

        logger.info("Failed to download track %s", track_id)
        return None

    except SpotifyError as e:
        logger.warning("Spotify Error for track %s - Error: %s", track_id, e)
        return None
    except Exception as e:
        logger.error("Unexpected error for track %s: %s", track_id, e)
        return None

def run_spotify_finder_in_executor(loop: asyncio.AbstractEventLoop, track_id: str):
    return loop.run_in_executor(_executor, spotify_finder_service, track_id)
