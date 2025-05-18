import subprocess
import os
import argparse
from datetime import datetime, timedelta
from collections import defaultdict

# --- 引数の取得 ---
parser = argparse.ArgumentParser(description="Scrapboxの日記を月ごとのMarkdownファイルに変換")
parser.add_argument("project_name", help="Scrapboxのプロジェクト名")
parser.add_argument("start_date", help="開始日（例: 2019-10-18）")
parser.add_argument("--end-date", help="終了日（例: 2020-01-31）。指定がなければ今日。", default=None)

args = parser.parse_args()
PROJECT_NAME = args.project_name

# 開始日と終了日をパース
try:
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
except ValueError:
    print("❌ start_date は YYYY-MM-DD 形式で入力してください")
    exit(1)

if args.end_date:
    try:
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    except ValueError:
        print("❌ end_date は YYYY-MM-DD 形式で入力してください")
        exit(1)
else:
    end_date = datetime.now()

if start_date > end_date:
    print("❌ 開始日は終了日より前である必要があります")
    exit(1)

# --- データ収集 ---
monthly_entries = defaultdict(list)
current_date = start_date

while current_date <= end_date:
    date_str = f"{current_date.year}/{current_date.month}/{current_date.day}"
    yyyymm = current_date.strftime("%Y-%m")
    page_path = f"{PROJECT_NAME}/{date_str}"

    try:
        result = subprocess.run(
            ["sb2md", page_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        content = result.stdout.strip()
        if content:
            print(f"✅ {date_str}: 出力あり")
            header = f"# {date_str}\n"
            monthly_entries[yyyymm].append(header + content + "\n")
        else:
            print(f"⚠️ {date_str}: 出力なし（空のページ）")
    except subprocess.CalledProcessError as e:
        print(f"❌ {date_str}: 取得失敗\n    {e.stderr.strip()}")

    current_date += timedelta(days=1)

# --- ファイル出力 ---
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

for yyyymm, entries in monthly_entries.items():
    output_path = os.path.join(output_dir, f"{yyyymm}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(entries))

print("✅ 全出力完了")
