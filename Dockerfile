FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg curl unzip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

ENV DENO_INSTALL="/usr/local"
RUN curl -fsSL --retry 5 --retry-delay 5 --retry-connrefused --retry-max-time 120 \
    https://deno.land/install.sh -o /tmp/deno_install.sh && \
    sh /tmp/deno_install.sh -y && \
    rm /tmp/deno_install.sh && \
    deno --version

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
