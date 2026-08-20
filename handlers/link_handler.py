import asyncio
import time
import os
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LinkPreviewOptions
from utils.link_detector import detect_platform, Platform
from services.spotify_service import run_spotify_finder_in_executor
from services.apple_music_service import apple_music

logger = logging.getLogger(__name__)

async def spotify_finder_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    link = update.message.text
    user = update.effective_user
    user_id = user.id
    logger.info("User: %s sent this link: %s\n", user_id, link)
    detected_link = detect_platform(link)

    if not detected_link or detected_link.platform == Platform.UNKNOWN or not detected_link.track_id:
        await update.message.reply_text(
            "❌ Oops! That Link Isn't Supported.\nPlease Make Sure You're Sending A Valid Link From Spotify Or Apple Music.")
        return

    logger.info("User: %s - Track ID: %s - Platform %s\n", user_id, detected_link.track_id, detected_link.platform)
    processing_msg = await update.message.reply_text(
        "⏳ Downloading Track, Please Wait...\n⏱ Estimated Time: 30s – 3m\n📢 We’ll Update You If The Download Gets Canceled.")

    if detected_link.platform == Platform.APPLE_MUSIC and detected_link.track_id:
        detected_link.track_id = await asyncio.to_thread(apple_music, detected_link.track_id)
        if not detected_link.track_id:
            logger.info("Track hasn't been detected: %s At ALL ---- Initial Fail\n", detected_link.track_id)
            await processing_msg.delete()
            await update.message.reply_text(
                "❌ <b>No Matching Track Found</b>\n\n"
                "<blockquote expandable>🤖 This Song Seems To Be Exclusive To Apple Music,And We Couldn't Find A Matching Version On Spotify.\n"
                "💡 We Can Currently Only Download Tracks Available On Spotify.\n\n🔗 Please Try A Different Song Or Link!</blockquote>",
                parse_mode=ParseMode.HTML, )
            return

    loop = asyncio.get_running_loop()
    result = await run_spotify_finder_in_executor(loop, detected_link.track_id)

    if result:
        metadata, file_path = result
        logger.info("Track has been detected: %s ---- Successful\n", metadata.name)

        unique_payload = f"{metadata.track_id}_{int(time.time())}"
        deep_link = f"https://t.me/gasslight_lyrics_bot?start={unique_payload}"

        keyboard = [
            [InlineKeyboardButton("📜 Get Lyrics", url=deep_link)]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        try:
            with open(file_path, "rb") as audio_file:
                await update.message.reply_audio(audio=audio_file, title=metadata.name,
                                                 performer=', '.join(metadata.artist),
                                                 caption=f"🎵 *{metadata.name}*\n🎤 {', '.join(metadata.artist)}\n💿 {metadata.album}",
                                                 parse_mode=ParseMode.MARKDOWN,
                                                 read_timeout=120,
                                                 write_timeout=120,
                                                 reply_markup=markup
                                                 )
            logger.info("Audio sent successfully: %s\n", file_path)

        except Exception as e:
            logger.info("Error sending audio: %s\n", e)
            await update.message.reply_text("⚠️ <b>Download Succeeded, But Sending Failed!</b>\n\n"
                                            "📥 The Track Was Downloaded Successfully, But We Hit A Snag While Delivery It To You.\n"
                                            "🔄 Please Try Sending The Link One More Time In A Moment!",
                                            parse_mode=ParseMode.HTML, )

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info("File removed: %s\n", file_path)

        await processing_msg.delete()

    else:
        logger.info("Track hasn't been detected: %s ---- Fail\n", detected_link.track_id)
        await processing_msg.delete()
        await update.message.reply_text(f"❌ <b>Download Failed</b>\n\n"
                                        f"<blockquote expandable>🔗 Track Link: https://open.spotify.com/track/{detected_link.track_id}\n\n"
                                        f"⚠️ We Found The Track, But Audio Fetching Failed Due To Copyright Restrictions.\n\n"
                                        f"🔄 Please Try Again In A Few Moments, Or Try A Different Song!</blockquote>",
                                        parse_mode=ParseMode.HTML,
                                        link_preview_options=LinkPreviewOptions(is_disabled=True))
