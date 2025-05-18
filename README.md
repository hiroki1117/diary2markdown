# Scrapbox Diary Exporter

このツールは、Scrapbox の日記ページを `sb2md` コマンドを使って Markdown に変換し、月ごとにまとめたテキストファイルとして保存する Python スクリプトです。

## 📦 概要

- `sb2md <プロジェクト名>/<日付>` コマンドで Scrapbox ページを Markdown に変換
- 日付範囲を指定して、1日ごとに日記ページを収集
- 月単位（例: `2023-08.txt`）でファイルを出力
- ログを標準出力に出して、成功・失敗がわかる

## 🛠 必要要件

- Python 3.7+
- `sb2md` コマンドが使える状態になっていること  
  → [sb2md GitHub](https://github.com/hiroki1117/sb2md) またはフォーク版からインストール
  `go install github.com/hiroki1117/sb2md` でインストール

## 📂 出力

- 出力先ディレクトリ：`output/`
- ファイル名形式：`YYYY-MM.txt`
- ファイル内容：Scrapboxの日記を1か月分まとめたMarkdownテキスト

## 🚀 使い方

```bash
python main.py <project_name> <start_date> [--end-date <end_date>]
```

## 🔐 PrivateなScrapboxにアクセスする場合

**Privateプロジェクト**のページを取得するには、Scrapboxのセッションクッキーを環境変数として設定する必要があります。
[mamezou-tech/sbgraph: Fetch Scrapbox project data and visualize activities.](https://github.com/mamezou-tech/sbgraph)

```bash
export SB_COOKIE_ID=connect.sid
export SB_COOKIE_VALUE=your-fancy-cookie
```

以下は、あなたの `README.md` に追記できる「Docker イメージのビルドと実行手順」セクションです。`diary-exporter` イメージのビルドと実行が簡単に行えるように整理されています。


## 🐳 Dockerでのビルドと実行

このプロジェクトは Docker を使って、Scrapbox の日記を Markdown にエクスポートできます。

### 🔧 1. Dockerイメージのビルド

まず、リポジトリのルートディレクトリで以下を実行します：

```bash
docker build -t diary-exporter .
```

* `-t diary-exporter` はイメージ名を指定しています（任意で `:v1` などタグをつけてもOK）

---

### 🔐 2. Private Scrapbox 用の Cookie を設定

**Privateプロジェクト**にアクセスするには、Scrapbox にログインしているブラウザから以下のクッキーを取得して、環境変数として渡す必要があります。

```bash
export SB_COOKIE_ID=connect.sid
export SB_COOKIE_VALUE=（実際のCookie値）
```

※ Chrome の「開発者ツール → Application → Cookies」から確認できます。

---

### 🚀 3. Dockerコンテナの実行

```bash
docker run --rm -it \
  -e SB_COOKIE_ID=$SB_COOKIE_ID \
  -e SB_COOKIE_VALUE=$SB_COOKIE_VALUE \
  -v $(pwd)/output:/app/output \
  diary-exporter \
  python main.py <project_name> <start_date> [--end-date <end_date>]
```

#### 📌 引数の例

* `<project_name>`: Scrapboxのプロジェクト名
* `<start_date>`: 日記取得の開始日（例：`2019-10-01`）
* `--end-date`: （任意）取得終了日。指定しなければ現在日付まで。

---

### ✅ 実行例

```bash
docker run --rm -it \
  -e SB_COOKIE_ID=$SB_COOKIE_ID \
  -e SB_COOKIE_VALUE=$SB_COOKIE_VALUE \
  -v $(pwd)/output:/app/output \
  diary-exporter \
  python main.py target-project 2019-10-01 --end-date 2020-01-31
```

この例では、2019年10月〜2020年1月の日記を月ごとに Markdown ファイルに変換し、`output/` ディレクトリに `YYYY-MM.txt` として保存します。

---

### 🧼 イメージの削除（再ビルド時など）

古い `diary-exporter` イメージをすべて削除したい場合：

```bash
docker rmi $(docker images | grep diary-exporter | awk '{print $3}')
```

