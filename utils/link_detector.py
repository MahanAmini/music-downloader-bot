from enum import Enum
import re
from dataclasses import dataclass

class Platform(Enum):
    SPOTIFY = "spotify"
    APPLE_MUSIC = "apple_music"
    UNKNOWN = "unknown"

@dataclass
class DetectedLink:
    platform: Platform
    track_id: str | None = None

SPOTIFY_TRACK_PATTERN = re.compile(
    r"(?:https?://)?(?:open\.)?spotify\.com/track/([a-zA-Z0-9]+)"
)

APPLE_MUSIC_TRACK_PATTERN = re.compile(
    r"(?:https?://)?(?:music|itunes)\.apple\.com/(?:[a-z]{2}/)?(?:album|song)/(?:[^/]+/)?(\d+)(?:\?i=(\d+))?"
)

def detect_platform(link: str) -> DetectedLink:
    spotify_match = SPOTIFY_TRACK_PATTERN.search(link)
    if spotify_match:
        track_id = spotify_match.group(1)
        return DetectedLink(platform=Platform.SPOTIFY, track_id=track_id)

    apple_match = APPLE_MUSIC_TRACK_PATTERN.search(link)
    if apple_match:
        track_id = apple_match.group(2) or apple_match.group(1)
        return DetectedLink(platform=Platform.APPLE_MUSIC, track_id=track_id)

    return DetectedLink(platform=Platform.UNKNOWN)
