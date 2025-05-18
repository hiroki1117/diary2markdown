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

