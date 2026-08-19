#!/bin/sh
# دانلود deno اینجا (موقع اجرا) انجام میشه، نه موقع build
# چون شبکه‌ی build environment ری‌ولی گاهی برای این دانلود پایدار نیست
if [ ! -f "$HOME/.spotdl/deno" ] && [ ! -f "$HOME/.local/share/spotdl/deno" ]; then
    echo "در حال دانلود deno..."
    spotdl --download-deno || echo "دانلود deno با خطا مواجه شد، ادامه بدون آن..."
fi
 
exec python main.py
