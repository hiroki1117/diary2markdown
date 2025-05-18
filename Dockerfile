FROM python:3.11-slim

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    golang \
    curl \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# sb2md を clone して build（cpせずに /usr/local/bin に直置き）
WORKDIR /tmp
RUN git clone -b fix/pagetitle_regex https://github.com/hiroki1117/sb2md.git && \
    cd sb2md && \
    go build -o /usr/local/bin/sb2md . && \
    chmod +x /usr/local/bin/sb2md

# 作業ディレクトリ作成
WORKDIR /app

# Pythonスクリプトをコピー
COPY main.py .

# 認証用 Cookie（必要に応じて）
ENV SB_COOKIE_ID=connect.sid
ENV SB_COOKIE_VALUE=your-cookie-value


# エントリーポイントなし → 実行時にコマンドを指定
# 例: docker run --rm diary-exporter python main.py hogeproject 2019-10-01
