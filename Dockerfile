FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y ffmpeg curl unzip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN spotdl --download-deno

COPY . .

CMD ["python", "main.py"]
