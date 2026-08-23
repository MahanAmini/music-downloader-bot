import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CallbackContext

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    bot_id = context.bot.id
    photos = await context.bot.get_user_profile_photos(user_id=bot_id)
    welcome_text = (
        f"Hi <a href='https://t.me/{user.username}'>{user.first_name}</a>,\n<b>GassLight</b> Team Is Happy To See You Here 😊\n\n"
        "🎵Send Me Any Spotify Or Apple Music Song Link\n"
        "And I'll Download It For you In High Quality!\n\n"
        "<blockquote>If You Face Any Problem Or Bug, Notify The Bug To Developer.</blockquote>"
        "👇Just Paste Your Link Below To Get Started."
    )

    keyboard = [
        [InlineKeyboardButton("About ❗", callback_data="about"),
         InlineKeyboardButton("Developer ⚙️", url="https://t.me/Mahan_aminy"),
         InlineKeyboardButton("Guidance 📖", callback_data="guide")]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_caption(caption=welcome_text, parse_mode=ParseMode.HTML,reply_markup=markup)
        logger.info("User: %s Return to Home", user.id)
        return

    logger.info("User: %s starts bot", user.id)
    await update.message.reply_photo(photo=photos.photos[0][0].file_id, caption=welcome_text,
                                     reply_to_message_id=update.message.message_id, parse_mode=ParseMode.HTML,
                                     reply_markup=markup)

content = {
    'about' : (
        "🐍 Language : <b>Python 3.13</b>\n"
        "📚 Main Libraries : <u>PTB & SpotDL</u>\n"
        "🎵 Music Resources : <a href='https://youtube.com'>YouTube</a> , <a href='https://soundcloud.com/'>SoundCloud</a> , <a href='https://music.youtube.com/'>YouTube Music</a> , . . .\n"
        "👨‍💻 Developer : @Mahan__Aminy\n\n"
        "⏳ SoundCloud & YouTube Music Links Coming Soon . . . "
    ),
    'guide' : (
        "🤖 How To Use <b>GassLight</b> Bot\n\n"
        "🎵 Step 1: Send Your Spotify Or Apple Music Link.\n\n"
        "⏳ Step 2: Wait Just A Moment. The Process Takes Between <b><u>30</u></b> <b>Seconds</b> To <b><u>3</u></b> <b>Minutes</b>.\n\n"
        "🎧 Step 3: Receive Your High-Quality Audio File Instantly.\n\n\n"
        "⚠️ Note: Sit Back And Relax! No Extra Steps Are Needed. If Your Link Is Invalid, The Bot Will Notify You Immediately."
    ),
}

async def start_button_handler(update: Update, contex: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    user_id = user.id

    response = content[query.data]
    logger.info("User: %s Selected: %s", user_id, query.data)
    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_caption(response, parse_mode=ParseMode.HTML, reply_markup=markup)
