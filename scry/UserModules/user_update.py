import os
import csv

# from App_1.models import RaceHTML
# from scry.RaceStatics.raceid_search import SearchID
from scry.html_scry import RacePipeline
from module_csv.create_csv_from_db import create_csv_from_db
from scry.scry_jusho import *
from scry.racedate_scry import *
from scry.new_race_search import *

def main(target_year,html_update_days_threshold):

    race_searcher = NewRaceIDSearch(year=target_year,html_update_days_threshold=html_update_days_threshold)

    # 一連の処理（スクレイピング、DB更新、CSV出力）を実行
    race_searcher.run()
    update_race_schedule(target_year)

    try:
        with open(race_searcher.csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # ヘッダー行をスキップ
            race_ids = [row[0] for row in reader if row]
    except Exception as e:
        print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
        return

    print(f"CSVから {len(race_ids)} 件のレースIDを読み込みました。")
    count = 0

    for raceid in race_searcher.update_race_ids:
        print(f'{len(race_searcher.update_race_ids)}件のレース情報のデータベース更新を行います。')
        count += 1
        print(f"[{count}/{len(race_ids)}] race_id={raceid} の処理を開始します。")

        pipeline = RacePipeline(str(raceid))  # RacePipeline は文字列race_idが想定
        pipeline.run()

    create_csv_from_db()


    pass