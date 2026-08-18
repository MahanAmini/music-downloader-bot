import os
import logging
import sys
from dotenv import load_dotenv
from urllib.parse import quote
from pathlib import Path

load_dotenv()

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

# Fundamental Configs
TELEGRAM_BOT_TOKEN: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
SPOTIFY_CLIENT_ID: str | None = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET: str | None = os.getenv("SPOTIFY_CLIENT_SECRET")

# Proxy
PROXY_USERNAME = os.getenv("PROXY_USERNAME", "")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD", "")
PROXY_HOST = os.getenv("PROXY_HOST", "")
PROXY_PORT = os.getenv("PROXY_PORT", "")

PROXY_URL = None
if PROXY_HOST and PROXY_PORT:
    PROXY_URL = (
        f"http://{quote(PROXY_USERNAME, safe='')}:"
        f"{quote(PROXY_PASSWORD, safe='')}@{PROXY_HOST}:{PROXY_PORT}"
    )

# Cookie Path
COOKIE_FILENAME = os.getenv("COOKIE_FILENAME", "cookies.txt")
COOKIE_PATH = str(BASE_DIR / COOKIE_FILENAME)

def validate_config() -> None:
    missing: list[str] = []

    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")

    if not SPOTIFY_CLIENT_ID:
        missing.append("SPOTIFY_CLIENT_ID")

    if not SPOTIFY_CLIENT_SECRET:
        missing.append("SPOTIFY_CLIENT_SECRET")

    if missing:
        logger.error("Environmental variables in .env has not set correctly : %s",
                     ", ".join(missing), )
        sys.exit(1)

    logger.info("Settings has been loading successfully.")
