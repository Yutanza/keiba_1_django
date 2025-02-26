
# shell.py (修正版サンプル)

import os
import csv

from App_1.models import RaceHTML
from scry.RaceStatics.raceid_search import SearchID
from scry.html_scry import RacePipeline
from module_csv.create_csv_from_db import create_csv_from_db
from scry.scry_jusho import *
from scry.racedate_scry import *
from scry.new_race_search import *

def main():
    # year = 2025
    # search = SearchID(year)

    # # 1) race_ids_YYYY.csv が無い、または空ファイルの場合、レースIDを取得してCSVに保存
    # if (not os.path.exists(search.file_path)) or (os.path.getsize(search.file_path) == 0):
    #     print(f"{search.file_path} が存在しないか空です。レースIDを取得します...")
    #     search.get_race_date_ids()   # カレンダーを巡回し、 date_id_list を取得
    #     search.get_race_ids()        # date_id_list から race_id_list を取得
    #     search.save_to_csv()         # race_ids_YYYY.csv に保存
    #     print("レースIDの取得とCSV保存が完了しました。")

    # 2) race_ids_YYYY.csv を読み込み、1レースずつ HTML を取得して RaceHTML に保存
    #    その後に RacePipeline.run() を呼び出し、HTMLから各モデルへ情報を展開


    # print("全レースのHTML取得＆パースが完了しました。")

    # # 3) 最後に CSV出力など別処理を実行
    # create_csv_from_db()
    # print("create_csv_from_db() が完了しました。")
    # update_race_schedule(2024)
    # create_csv_from_db()

    # trush_ids=[race.race_id for race in Race.objects.filter(year=2025)]
    # for trush_id in trush_ids:
    #     RaceHTML.objects.filter(trush_id).delete
    # RaceHTML.objects.filter(race=None).delete()

    target_year=2023
    race_searcher = NewRaceIDSearch(year=target_year,html_update_days_threshold=500)

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

        # 2-1) レースIDに対応するHTMLを取得・保存 (RaceHTML) 
        #      既に保存済みの場合は update_or_create の仕組みで更新・スキップ
        # race_searcher.save_html_t_db(raceid)

        # 2-2) 取得したHTMLをパイプラインでパースし、DBに保存
        pipeline = RacePipeline(str(raceid))  # RacePipeline は文字列race_idが想定
        pipeline.run()
        print(count)

    create_csv_from_db()



    pass

if __name__ == "__main__":
    main()
else:
    main()
