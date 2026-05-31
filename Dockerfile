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
RUN cd site && npm ci && npm run build

# Astroがルートindex.htmlを上書きするので、添削SPAで復元
RUN cp /app/correction-app/frontend-src/index.html /app/correction-app/frontend/index.html

# FastAPI の起動
WORKDIR /app/correction-app/backend
EXPOSE 8000
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
