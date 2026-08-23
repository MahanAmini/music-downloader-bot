import asyncio
import logging
from telegram.error import BadRequest
from telegram.constants import ChatAction

logger = logging.getLogger(__name__)

async def keep_uploading_status(context, chat_id, stop_event: asyncio.Event):
    while not stop_event.is_set():
        try:
            await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_DOCUMENT)
        except Exception as e:
            logger.warning("Failed to send chat action: %s", e)

        try:
            await asyncio.wait_for(stop_event.wait(), timeout=4.0)
        except asyncio.TimeoutError:
            pass

async def animate_loading(message, stop_event: asyncio.Event):
    frames = [
        "🔗 Downloading Track .",
        "🔗 Downloading Track . .",
        "🔗 Downloading Track . . .",
        "🔗 Downloading Track . . . .",
        "🔗 Downloading Track . . . . ."
    ]

    base_text = (
        "⏱ Estimated Time: 30s – 3m\n"
        "📢 We’ll Update You If The Download Gets Canceled."
    )

    idx = 0
    sec = 0
    while not stop_event.is_set():
        try:
            current_frame = frames[idx % len(frames)]
            new_text = f"{current_frame}\n⏳Timer : {sec} Secend\n{base_text}"

            await message.edit_text(new_text)
            idx += 1
            sec += 2
        except BadRequest as e:
            if "Message is not modified" not in str(e):
                pass
        except Exception:
            break

        try:
            await asyncio.wait_for(stop_event.wait(), timeout=2.0)
        except asyncio.TimeoutError:
            pass
