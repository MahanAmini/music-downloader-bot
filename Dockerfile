FROM python:3.11-slim

# ۱. نصب ابزارهای مورد نیاز سیستم از جمله curl و unzip
RUN apt-get update && \
    apt-get install -y ffmpeg curl unzip && \
    rm -rf /var/lib/apt/lists/*

# ۲. نصب مستقیم و استاندارد Deno روی سیستم
RUN curl -fsSL https://deno.land/x/install/install.sh | sh
ENV DENO_INSTALL="/root/.deno"
ENV PATH="$DENO_INSTALL/bin:$PATH"

WORKDIR /app

# ۳. نصب پکیج‌های پایتون
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ۴. کپی کردن کدهای پروژه
COPY . .

# ۵. اجرای ربات
CMD ["python", "main.py"]
