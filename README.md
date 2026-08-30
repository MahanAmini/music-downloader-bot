# 🎵 GassLight — Music Downloader Bot

A Telegram bot that downloads high-quality audio tracks from **Spotify** and **Apple Music** links. Send a link, get an MP3 back — no extra steps.

---

## 🇬🇧 English

### ✨ Features

- 🔗 **Spotify & Apple Music support** — paste a track link from either platform
- 🍎 **Apple Music → Spotify resolution** — Apple Music links are automatically matched to their Spotify equivalent before downloading
- ⬇️ **High-quality downloads** powered by [`spotdl`](https://github.com/spotDL/spotify-downloader)
- 🔁 **Automatic provider fallback** — tries YouTube first, then falls back to SoundCloud if the track isn't found
- 🎬 **Live progress animation** while the bot searches for and downloads your track
- 📜 **Deep link to a lyrics bot** — every downloaded track comes with a button to fetch its lyrics
- ⚠️ **Friendly error handling** — clear messages for unsupported links, missing tracks, or failed downloads
- 🍪 Optional cookie file support for providers that require authentication
- 🐳 **Docker-ready** for easy deployment

> ℹ️ The bot currently supports single **track** links only (no playlists or albums yet).

### 🛠️ Tech Stack

| Part | Technology |
|---|---|
| Language | Python 3.13 |
| Telegram bot library | [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (async) |
| Downloading | [`spotdl`](https://github.com/spotDL/spotify-downloader) |
| Audio sources | YouTube (primary), SoundCloud (fallback) |
| Deployment | Docker |

### 📁 Project Structure

```
music-downloader-bot/
├── bot.py                        # Entry point — builds and runs the bot
├── config.py                     # Loads environment variables and config
├── cookies.txt                   # Optional cookies file for yt-dlp/spotdl
├── env.example                   # Example environment variables
├── requirements.txt
├── Dockerfile
├── handlers/
│   ├── start.py                  # /start command, welcome message, About/Guide buttons
│   └── link_handler.py           # Main handler: detects link, downloads, replies with audio
├── services/
│   ├── spotify_service.py        # Downloads a track via spotdl (YouTube → SoundCloud fallback)
│   └── apple_music_service.py    # Resolves an Apple Music track to its Spotify ID
└── utils/
    ├── link_detector.py          # Regex-based Spotify/Apple Music link + track ID detection
    └── helper.py                 # Loading animation & "uploading audio" status helpers
```

### 🚀 Local Setup

**Prerequisites**

- Python 3.11+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- Spotify API credentials (Client ID & Secret) from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

**Steps**

1. Clone the repository

   ```bash
   git clone https://github.com/MahanAmini/music-downloader-bot.git
   cd music-downloader-bot
   ```

2. Create a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables

   ```bash
   cp env.example .env
   ```

   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   ```
   > ⚠️ Never commit your `.env` file.

5. Run the bot

   ```bash
   python bot.py
   ```

   The bot runs in **polling** mode, which needs no domain or HTTPS setup.

**Run with Docker** (alternative to steps 2–5)

```bash
docker build -t gasslight-bot .
docker run --env-file .env gasslight-bot
```

### 💬 Usage

1. Start the bot with `/start`
2. Paste any **Spotify** or **Apple Music** track link
3. The bot searches for the track, shows a live progress animation, and downloads the audio (YouTube first, SoundCloud as fallback)
4. You receive the track as an audio file, along with a **"📜 Get Lyrics"** button that opens a companion lyrics bot

### ⚖️ Copyright Note

This bot fetches audio through publicly available streaming sources for personal use. Respect the copyright terms of the platforms and content involved.

### 🤝 Contributing

This project is a learning journey — bug reports and pull requests are welcome.

### 📄 License

Licensed under the [MIT License](LICENSE).

---

## 🇮🇷 فارسی

### ✨ امکانات

- 🔗 **پشتیبانی از اسپاتیفای و اپل موزیک** — کافیه لینک آهنگ رو از هرکدوم بفرستی
- 🍎 **تبدیل لینک اپل موزیک به اسپاتیفای** — لینک‌های اپل موزیک به‌صورت خودکار با معادل اسپاتیفاییشون تطبیق داده می‌شن و بعد دانلود می‌شن
- ⬇️ **دانلود با کیفیت بالا** با استفاده از [`spotdl`](https://github.com/spotDL/spotify-downloader)
- 🔁 **جایگزینی خودکار منبع دانلود** — اول از یوتیوب امتحان می‌کنه، اگه پیدا نشد میره سراغ SoundCloud
- 🎬 **انیمیشن زنده‌ی پیشرفت** حین جستجو و دانلود آهنگ
- 📜 **لینک مستقیم به ربات لیریکس** — بعد از دریافت هر آهنگ، دکمه‌ای برای گرفتن متن آهنگ نمایش داده می‌شه
- ⚠️ **مدیریت خطای کاربرپسند** — پیام‌های واضح برای لینک‌های نامعتبر، پیدا نشدن آهنگ یا خطا در دانلود
- 🍪 پشتیبانی اختیاری از فایل کوکی برای منابعی که نیاز به احراز هویت دارن
- 🐳 **آماده برای Docker** جهت دیپلوی راحت‌تر

> ℹ️ فعلاً ربات فقط از لینک تک **آهنگ (track)** پشتیبانی می‌کنه، نه پلی‌لیست یا آلبوم.

### 🛠️ تکنولوژی‌های استفاده‌شده

| بخش | تکنولوژی |
|---|---|
| زبان برنامه‌نویسی | Python 3.13 |
| کتابخانه‌ی ربات تلگرام | [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (نسخه‌ی async) |
| دانلودر | [`spotdl`](https://github.com/spotDL/spotify-downloader) |
| منابع صوتی | یوتیوب (اصلی)، SoundCloud (جایگزین) |
| دیپلوی | Docker |

### 📁 ساختار پروژه

```
music-downloader-bot/
├── bot.py                        # نقطه‌ی ورود اصلی — ساخت و اجرای ربات
├── config.py                     # خواندن متغیرهای محیطی و تنظیمات
├── cookies.txt                   # فایل کوکی اختیاری برای yt-dlp/spotdl
├── env.example                   # نمونه‌ی متغیرهای محیطی
├── requirements.txt
├── Dockerfile
├── handlers/
│   ├── start.py                  # دستور /start، پیام خوش‌آمدگویی، دکمه‌های About/Guide
│   └── link_handler.py           # هندلر اصلی: تشخیص لینک، دانلود، ارسال فایل صوتی
├── services/
│   ├── spotify_service.py        # دانلود آهنگ با spotdl (یوتیوب → SoundCloud)
│   └── apple_music_service.py    # تبدیل آهنگ اپل موزیک به شناسه‌ی اسپاتیفای
└── utils/
    ├── link_detector.py          # تشخیص لینک اسپاتیفای/اپل موزیک و استخراج شناسه با regex
    └── helper.py                 # توابع کمکی انیمیشن لودینگ و وضعیت "در حال آپلود"
```

### 🚀 راه‌اندازی محلی (Local Setup)

**پیش‌نیازها**

- پایتون نسخه‌ی 3.11 یا بالاتر
- یه توکن ربات تلگرام از [@BotFather](https://t.me/BotFather)
- کلیدهای API اسپاتیفای (Client ID و Secret) از [پنل توسعه‌دهندگان اسپاتیفای](https://developer.spotify.com/dashboard)

**مراحل**

۱. کلون کردن پروژه

   ```bash
   git clone https://github.com/MahanAmini/music-downloader-bot.git
   cd music-downloader-bot
   ```

۲. ساخت محیط مجازی

   ```bash
   python -m venv venv
   source venv/bin/activate   # ویندوز: venv\Scripts\activate
   ```

۳. نصب کتابخانه‌ها

   ```bash
   pip install -r requirements.txt
   ```

۴. تنظیم متغیرهای محیطی

   ```bash
   cp env.example .env
   ```

   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   ```
   > ⚠️ فایل `.env` رو هرگز commit نکن.

۵. اجرای ربات

   ```bash
   python bot.py
   ```

   ربات به روش **polling** اجرا می‌شه و نیازی به دامنه یا HTTPS نداره.

**اجرا با Docker** (جایگزین مراحل ۲ تا ۵)

```bash
docker build -t gasslight-bot .
docker run --env-file .env gasslight-bot
```

### 💬 نحوه‌ی استفاده

۱. ربات رو با `/start` استارت کن
۲. لینک آهنگ از **اسپاتیفای** یا **اپل موزیک** رو بفرست
۳. ربات دنبال آهنگ می‌گرده، انیمیشن پیشرفت رو نشون می‌ده و فایل صوتی رو دانلود می‌کنه (اول یوتیوب، در صورت نیاز SoundCloud)
۴. فایل صوتی همراه با دکمه‌ی **«📜 دریافت لیریکس»** که به یه ربات لیریکس مکمل وصل می‌شه، برات ارسال می‌شه

### ⚖️ نکته‌ی کپی‌رایت

این ربات فایل صوتی رو از منابع استریم عمومی و برای استفاده‌ی شخصی دریافت می‌کنه. لطفاً به قوانین کپی‌رایت پلتفرم‌ها و محتوای مربوطه احترام بذار.

### 🤝 مشارکت

این پروژه در مسیر یادگیریه — گزارش باگ و Pull Request خوش‌آمده.

### 📄 لایسنس

این پروژه تحت لایسنس [MIT](LICENSE) منتشر شده.
