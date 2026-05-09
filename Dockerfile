FROM python:3.11-slim

# Node.js 22 のインストール
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ソースをコピー
COPY . .

# Python 依存関係のインストール
RUN pip install --no-cache-dir -r requirements.txt

# Astro ビルド（correction-app/frontend/ に出力）
ARG PUBLIC_GA4_ID
ENV PUBLIC_GA4_ID=$PUBLIC_GA4_ID
RUN cd site && npm ci && npm run build

# FastAPI の起動
WORKDIR /app/correction-app/backend
EXPOSE 8000
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
