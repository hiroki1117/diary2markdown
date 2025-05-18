import subprocess
import os
import argparse
from datetime import datetime, timedelta
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import List

OUTPUT_DIR = "output"

def collect_entries_for_month(project: str, year: int, month: int) -> (str, List[str]):
    """1ヶ月分のScrapboxページを取得してリストで返す"""
    entries = []
    date = datetime(year, month, 1)
    # 翌月1日を求めてループの終わりにする
    next_month = (date.replace(day=28) + timedelta(days=4)).replace(day=1)

    while date < next_month and date <= datetime.now():
        date_str = f"{date.year}/{date.month}/{date.day}"
        page_path = f"{project}/{date_str}"

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
                entries.append(header + content + "\n")
            else:
                print(f"⚠️ {date_str}: 出力なし（空のページ）")
        except subprocess.CalledProcessError as e:
            print(f"❌ {date_str}: 取得失敗\n    {e.stderr.strip()}")

        date += timedelta(days=1)

    yyyymm = f"{year:04d}-{month:02d}"
    return yyyymm, entries


def write_monthly_file(yyyymm: str, entries: List[str]):
    """指定月のファイルに出力"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{yyyymm}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(entries))
    print(f"📄 {yyyymm}.txt を書き出しました")


def parse_args():
    parser = argparse.ArgumentParser(description="Scrapboxの日記を月ごとのMarkdownファイルに変換")
    parser.add_argument("project_name", help="Scrapboxのプロジェクト名）")
    parser.add_argument("start_date", help="開始日（例: 2019-10-18）")
    parser.add_argument("--end-date", help="終了日（例: 2020-01-31）。指定がなければ今日。", default=None)
    return parser.parse_args()


def get_month_range(start_date: datetime, end_date: datetime) -> List[tuple]:
    """start〜endの間の年月リストを返す"""
    months = []
    current = datetime(start_date.year, start_date.month, 1)
    while current <= end_date:
        months.append((current.year, current.month))
        # 次の月
        current = (current.replace(day=28) + timedelta(days=4)).replace(day=1)
    return months


def main():
    args = parse_args()

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

    months = get_month_range(start_date, end_date)

    def process_month(year_month):
        year, month = year_month
        yyyymm, entries = collect_entries_for_month(args.project_name, year, month)
        if entries:
            write_monthly_file(yyyymm, entries)
        else:
            print(f"🕳 {yyyymm}: 出力対象なし（スキップ）")

    print(f"🚀 {len(months)} ヶ月分を並列で処理します...")

    with ThreadPoolExecutor() as executor:
        executor.map(process_month, months)

    print("✅ 全出力完了")


if __name__ == "__main__":
    main()
