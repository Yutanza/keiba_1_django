from App_1.models import *
from scry.RaceStatics.raceid_search import *
from scry.SampleFiles.sample.sample import *
from scry.html_scry import *
from module_csv.create_csv_from_db import *
from keiba_1.settings import *

from tabulate import tabulate
search = SearchID(2024)

# ファイルの存在確認
# if not os.path.exists(search.file_path):
#     print(f"ファイルが見つかりません: {search.file_path}")
# else:
ct=0
try:
    with open(search.file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file) 
        header = next(reader)  # ヘッダー行をスキップ
        race_ids = [int(row[0]) for row in reader]  # データ行の1列目を抽出          
except Exception as e:
    print(f"エラーが発生しました: {e}")
else:
    print(len(race_ids))
    # RaceEntry.objects.filter(race=Race.objects.get(race_id=202406010106)).delete()
    for raceid in race_ids:
        ct+=1
        # Race.objects.update_or_create(
        #     race_id=raceid,  # レースIDを動的に利用
        #     defaults={
        #         'race_name': 'Sample Race'
        #     }
        # )
        # print('Hello2')
        # search.save_html_t_db(raceid)
        pipe=RacePipeline(raceid)
        pipe.run()
        # extra = ExtractInfo(raceid)
        # extra.run()
        print(ct,raceid)

        
finally:
    print('Done')

    # print(RaceEntry.objects.filter(race=Race.objects.get(race_id=raceid)))

# print(RaceHTML.objects.get(race_id=race_ids[13]))

        # 表として出力
print(len(race_ids))
# raceid=race_ids[3]

create_csv_from_db()
# race_obj=Race.objects.get(race_id=raceid)
# fields = [(field.name, getattr(race_obj, field.name)) for field in race_obj._meta.get_fields()]
# print(tabulate(fields, headers=["Field", "Value"], tablefmt="grid"))

# try:
#     lap_obj=Payout.objects.filter(race=Race.objects.get(race_id=raceid))
# except:
#     print('Error')
# else:
#     fields = [(field.name, getattr(lap_obj[2], field.name)) for field in lap_obj.first()._meta.get_fields()]
#     print(tabulate(fields, headers=["Field", "Value"], tablefmt="grid"))

# entry_query_set=RaceEntry.objects.filter(race=Race.objects.get(race_id=raceid))
# model = entry_query_set.model
# fields = [field.name for field in model._meta.get_fields()]

# # # 各オブジェクトのフィールド値を取得
# rows = []
# for obj in entry_query_set:
#     row = [getattr(obj, field) for field in fields]
#     rows.append(row)

# print(tabulate(rows, headers=fields, tablefmt="grid"))

import pandas as pd

import os
# CSVファイルを読み込む
df = pd.read_csv(os.path.join(BASE_DIR,'csv_dir/RaceEntry.csv'))

# データクレンジング：数値に変換できない値をNaNに置き換える
df['人気'] = pd.to_numeric(df['人気'], errors='coerce')
df['順位'] = pd.to_numeric(df['順位'], errors='coerce')

# NaNを含む行を削除
df = df.dropna(subset=['人気', '順位'])

# 必要な列の相関係数を計算
correlation = df['人気'].corr(df['順位'])

print(f"馬人気と順位の相関係数: {correlation}")

