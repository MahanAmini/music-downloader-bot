import asyncio
import os
import re
from difflib import SequenceMatcher
from spotdl.utils.spotify import SpotifyClient, SpotifyError
import requests
from dataclasses import dataclass
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from utils.link_detector import detect_platform, Platform
from services.spotify_service import run_spotify_finder_in_executor

logger = logging.getLogger(__name__)


@dataclass
class AppleSongMetadata:
    track_name: str
    artist_name: str
    album_name: str


def _clean_track_name(track_name: str) -> str:
    if not track_name:
        return ""
    return re.sub(r"[\(\[].*?(feat\.|ft\.|with).*?[\)\]]", "", track_name, flags=re.IGNORECASE).strip()


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def apple_music(track_id: str):
    url_format = "https://itunes.apple.com/lookup"
    params = {
        "id": track_id,
        "entity": "song",
    }
    response = requests.get(url_format, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("resultCount", 0) == 0:
        return None

    results = data["results"][0]
    metadata = AppleSongMetadata(track_name=results.get("trackName"), artist_name=results.get("artistName"),
                                 album_name=results.get("collectionName"))
    if not metadata.track_name or not metadata.artist_name:
        logger.warning("Apple Music lookup returned incomplete metadata for id=%s", track_id)
        return None
    spotify_id = spotify_trackid_finder(metadata.track_name, metadata.artist_name)
    if not spotify_id:
        return None

    return spotify_id


def spotify_trackid_finder(track_name: str, artist_name: str) -> str | None:
    spotify_client = SpotifyClient()
    cleaned_name = _clean_track_name(track_name)
    query = f"track:{cleaned_name} artist:{artist_name}"
    results = spotify_client.search(query, type="track", limit=10)
    items = results["tracks"]["items"]

    if not items:
        fallback_query = f"{cleaned_name} {artist_name}"
        results = spotify_client.search(fallback_query, type="track", limit=10)
        items = results["tracks"]["items"]
        if not items:
            logger.info("No Spotify match found for: %s - %s", (track_name, artist_name))
            return None

    best_item = None
    best_score = 0.0
    for item in items:
        title_score = _similarity(cleaned_name, item["name"])
        item_artists = [a["name"] for a in item.get("artists", [])]
        artist_score = max((_similarity(artist_name, a) for a in item_artists), default=0.0)
        combined_score = min(title_score, artist_score)
        if artist_score > best_score:
            best_score = artist_score
            best_item = item

    if best_item is None or best_score < 0.5:
        logger.info(
            "Best Spotify match too weak for: %s - %s (score=%.2f)",
            track_name, artist_name, best_score,
        )
        return None

    return best_item["id"]
