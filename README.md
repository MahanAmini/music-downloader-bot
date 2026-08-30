# Gaslight Lyricsor Bot

**Gaslight** یه ربات تلگرامیه که اسم یه آهنگ رو بهش می‌دی و لیریکس (متن) اون آهنگ رو برات پیدا می‌کنه و برمی‌گردونه.

> این پروژه در حال توسعه‌ست و اولین پروژه‌ی من به‌عنوان یه توسعه‌دهنده‌ست 🌱

---

## ✨ امکانات

- 🔎 جستجوی آهنگ با اسم (و در صورت امکان اسم خواننده)
- 🧠 تشخیص خودکار غلط املایی در جستجو و نمایش بهترین تطبیق ممکن
- 📋 جستجوی هوشمند از طریق **iTunes API** که تا ۱۰ نتیجه‌ی مشابه پیدا می‌کنه تا کاربر بتونه دقیق‌ترین گزینه رو انتخاب کنه
- ⌨️ جستجوی دستی و دقیق با دستور:
  ```
  /search music by artist
  ```
- 📜 دریافت لیریکس از چند منبع مختلف (ترتیب اولویت قابل تنظیم):
  - [Genius](https://genius.com/developers) (از طریق `lyricsgenius`)
  - [lrclib](https://lrclib.net/)
  - [lyrics.ovh](https://lyricsovh.docs.apiary.io/)
  - [iTunes Search API](https://performance-partners.apple.com/search-api)
- 🌐 پشتیبانی از دو زبان: **فارسی** و **انگلیسی** (قابل تغییر توسط کاربر)
- ✂️ تقسیم خودکار پیام‌های طولانی (رعایت محدودیت ۴۰۹۶ کاراکتری تلگرام)

> ℹ️ این پروژه قرار نیست فیچرهایی مثل **کش کردن نتایج**، **شناسایی موزیک از فایل صوتی**، یا **آمار استفاده از ربات** داشته باشه — تمرکز فقط روی جستجو و دریافت دقیق لیریکسه.

---

## 🛠️ تکنولوژی‌های استفاده‌شده

| بخش | تکنولوژی |
|---|---|
| زبان برنامه‌نویسی | Python 3.11+ |
| کتابخونه‌ی ربات تلگرام | [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (نسخه‌ی async) |
| منابع لیریکس و جستجو | `lyricsgenius` ، iTunes Search API ، lrclib ، lyrics.ovh |

---

## 📁 ساختار پروژه

```
gaslight/
├── bot.py                     # نقطه ورود اصلی، اجرای ربات
├── config.py                   # خواندن تنظیمات و متغیرهای محیطی
├── .env                        # توکن‌ها و کلیدهای API (هرگز commit نمی‌شه)
├── .env.example                 # نمونه‌ی بدون مقدار واقعی
├── handlers/                     # هندلرهای دستورات و پیام‌ها
│   ├── start.py
│   ├── search.py                 # هندل کردن جستجوی خودکار آهنگ
│   ├── manual_search.py           # هندل دستور /search music by artist
│   └── language.py                # تغییر زبان
├── services/
│   ├── lyrics_service.py         # منطق گرفتن لیریکس از چند منبع + fallback
│   ├── itunes_service.py          # جستجو و پیدا کردن ۱۰ نتیجه‌ی مشابه از iTunes
│   └── spell_correction.py        # تشخیص غلط املایی و بهترین تطبیق
├── locales/                        # فایل‌های ترجمه (fa.json / en.json)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 راه‌اندازی و اجرا (Local Setup)

### پیش‌نیازها
- Python نسخه‌ی 3.11 یا بالاتر
- یه اکانت تلگرام و ساخت ربات از طریق [@BotFather](https://t.me/BotFather)
- یه API key از [Genius](https://genius.com/api-clients)

### مراحل

**۱. کلون کردن پروژه**
```bash
git clone https://github.com/YOUR-USERNAME/gaslight.git
cd gaslight
```

**۲. ساخت محیط مجازی (Virtual Environment)**

> 💡 `venv` یه محیط ایزوله می‌سازه که کتابخونه‌های این پروژه رو از بقیه‌ی سیستمت جدا نگه می‌داره.

```bash
python -m venv venv
source venv/bin/activate   # ویندوز: venv\Scripts\activate
```

**۳. نصب کتابخونه‌ها**
```bash
pip install -r requirements.txt
```

**۴. تنظیم متغیرهای محیطی**

فایل `.env.example` رو کپی کن و اسمش رو بذار `.env`، بعد مقادیر واقعی رو داخلش بذار:

```bash
cp .env.example .env
```

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
GENIUS_API_TOKEN=your_genius_api_key_here
```

> ⚠️ فایل `.env` هرگز نباید commit بشه — داخل `.gitignore` قرار داره.

> ℹ️ iTunes، lrclib و lyrics.ovh نیازی به API key ندارن، پس فقط توکن‌های بالا کافیه.

**۵. اجرای ربات**
```bash
python bot.py
```

ربات فعلاً به روش **polling** اجرا می‌شه (یعنی خودش مدام از تلگرام سوال می‌کنه «پیام جدیدی هست؟») که برای اجرای لوکال ساده‌تره و نیازی به دامنه یا HTTPS نداره.

---

## 💬 نحوه‌ی استفاده

### جستجوی عادی (خودکار)
1. ربات رو با `/start` استارت کن
2. اسم آهنگ (و ترجیحاً اسم خواننده) رو بفرست
3. ربات با استفاده از iTunes تا ۱۰ نتیجه‌ی مشابه پیدا می‌کنه و بهترین تطبیق (حتی اگه غلط املایی داشته باشی) رو نشون می‌ده
4. لیریکس از یکی از منابع (Genius، lrclib، lyrics.ovh یا iTunes) برات ارسال می‌شه — اگه طولانی باشه، در چند پیام تقسیم می‌شه

### جستجوی دستی (دقیق)
اگه دقیقاً می‌دونی اسم آهنگ و خواننده چیه، می‌تونی مستقیم بنویسی:
```
/search music by artist
```
مثال:
```
/search Blinding Lights by The Weeknd
```

### تغییر زبان
با دستور تغییر زبان می‌تونی بین فارسی/انگلیسی جابه‌جا شی.

---

## ⚖️ نکته‌ی کپی‌رایت

متن آهنگ‌ها معمولاً کپی‌رایت دارن. این ربات فقط از طریق APIهایی که مجوز نمایش این محتوا رو دارن (Genius، lrclib، lyrics.ovh، iTunes) لیریکس رو دریافت می‌کنه و هیچ ذخیره‌سازی انبوه یا توزیع مجدد لیریکس بیرون از context ربات انجام نمی‌ده.

---

## 🤝 مشارکت

این پروژه در حال یادگیریه، پس اگه پیشنهاد یا باگی دیدی خوشحال می‌شم از طریق Issue یا Pull Request مطرحش کنی.

---

## 📄 لایسنس

این پروژه تحت لایسنس [MIT](LICENSE) منتشر شده.
