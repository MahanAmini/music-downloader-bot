import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import BotCommand
from config import TELEGRAM_BOT_TOKEN,validate_config
from handlers.start import start_command,start_button_handler
from handlers.link_handler import spotify_finder_handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def setup_bot_commands(application):
    commands = [
        BotCommand("start", "Let's Start - Home Page")
    ]
    await application.bot.set_my_commands(commands)

def main() -> None:
    validate_config()

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).concurrent_updates(True).post_init(setup_bot_commands).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, spotify_finder_handler))
    application.add_handler(CallbackQueryHandler(start_button_handler,pattern=r"^(about|guide)$"))
    application.add_handler(CallbackQueryHandler(start_command,pattern=r"^home$"))

    logger.info("Bot is running | (polling mode) ...")
    application.run_polling()

if __name__ == "__main__":
    main()