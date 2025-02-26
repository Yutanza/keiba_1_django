# from bs4 import BeautifulSoup
# from datetime import datetime
# import os
# from App_1.models import Race, RaceEntry, Horse, Jockey, Trainer  # 必要なモデルをインポート

# BASE_PATH = os.path.dirname(os.path.abspath(__file__))
# # サンプルHTMLを読み込みます。


# class ExtractInfo:
#     def __init__(self,race_id):
#         self.raceid=race_id
#         self.soup=""
#         self.html_path=os.path.join(BASE_PATH,'RaceStatics',f'sample_{race_id}.html')
#         self.race_info={}
#         self.race_entry={}

#     def open_file(self):
#         try:
#             with open(self.html_path, 'r', encoding='utf-8') as file:
#                 html_content = file.read()
#                 self.soup = BeautifulSoup(html_content, 'html.parser')

#         except FileNotFoundError:
#             print(f"Error: The file '{self.html_path}' was not found.")
#         except PermissionError:
#             print(f"Error: Permission denied when trying to read the file '{self.html_path}'.")
#         except Exception as e:
#             print(f"An unexpected error occurred while reading the file '{self.html_path}': {e}")

# # レース情報を抽出
#     def extract_race_info(self):
#         # BeautifulSoupでHTMLを解析
#         race_name = self.soup.find('h1').get_text(strip=True)
#         details = self.soup.find('p', class_='smalltxt').get_text(strip=True)
#         date_str = details.split(' ')[0]  # 日付部分を抽出
#         race_date = datetime.strptime(date_str, '%Y年%m月%d日').date()
#         race_details=self.soup.find('diary_snap_cut').find('span').text.split(':')
#         # print(race_details,race_details)
#         # print(race_details)
#         # print(race_details.split(':'))
#         # distance_text = race_details.split('/')[-3].split(' ')[0]
#         # distance = int(distance_text.split('m')[0].strip('ダ右'))
#         # weather, track_condition = details.split('/')[-2:]  # 天候と馬場情報を抽出
#         # weather = weather.split(':')[1].strip()
#         # track_condition = track_condition.split(':')[1].strip()
#         # data = ['ダ右1200m\xa0/\xa0天候 ', ' 晴\xa0/\xa0ダート ', ' 良\xa0/\xa0発走 ', ' 10', '05']

#         # 距離の抽出
#         distance = int(race_details[0].split('m')[0].strip('ダ右'))

#         # 天候の抽出
#         weather = race_details[1].split('天候 ')[-1].strip()

#         # 馬場状態の抽出
#         track_condition = race_details[2].split('ダート ')[-1].strip('発走 ')

#         # 発走時刻の抽出
#         start_time = f"{race_details[3].strip()}:{race_details[4].strip()}"

#         # # 結果を辞書でまとめる
#         # race_details = {
#         #     'distance': distance,           # 距離 (例: 1200)
#         #     'weather': weather,             # 天候 (例: 晴)
#         #     'track_condition': track_condition, # 馬場状態 (例: 良)
#         #     'start_time': start_time        # 発走時刻 (例: 10:05)
#         # }

#         # # 結果を表示
#         # print(race_details)

#         self.race_info={
#             'race_name': race_name,
#             'race_date': race_date,
#             'distance': distance,
#             'weather': weather,
#             'track_condition': track_condition
#         }


#         # return {
#         #     'race_name': race_name,
#         #     'race_date': race_date,
#         #     'distance': distance,
#         #     'weather': weather,
#         #     'track_condition': track_condition
#         # }

#     # 出馬表情報を抽出
#     def extract_race_entries(self):
#         entries = []
#         rows = self.soup.select('table.race_table_01 tr')[1:]  # ヘッダー行を除外

#         for row in rows:
#             cells = row.find_all('td')
#             if len(cells) < 6:
#                 continue  # データ不足行をスキップ

#             horse_name = cells[3].get_text(strip=True)
#             sex_age = cells[4].get_text(strip=True)
#             weight_carried = float(cells[5].get_text(strip=True))
#             jockey_name = cells[6].get_text(strip=True)

#             entries.append({
#                 'horse_name': horse_name,
#                 'sex_age': sex_age,
#                 'weight_carried': weight_carried,
#                 'jockey_name': jockey_name
#             })
        
#         self.race_entry=entries

#         # return entries

#     # データベースへの保存
#     def save_to_db(self):
#         # レース情報を保存
#         race, created = Race.objects.update_or_create(
#             race_id=self.raceid,
#             defaults={
#                 'race_name':self.race_info['race_name'],
#                 'date':self.race_info['race_date'],
#                 'distance': self.race_info['distance'],
#                 'weather': self.race_info['weather'],
#                 'track_condition': self.race_info['track_condition']
#             }
#         )

#         # 出馬表情報を保存
#         for entry in self.race_entry:
#             # 馬情報を保存
#             horse, _ = Horse.objects.update_or_create(name=entry['horse_name'], defaults={'sex_age': entry['sex_age']})

#             # 騎手情報を保存
#             jockey, _ = Jockey.objects.update_or_create(name=entry['jockey_name'])

#             # 出馬表エントリーを保存
#             RaceEntry.objects.update_or_create(
#                 race=race,
#                 horse=horse,
#                 jockey=jockey,
#                 defaults={
#                     'weight_carried': entry['weight_carried']
#                 }
#             )

#             # 抽出と保存処理を実行
#     # def main(self):
#     #     race_info = self.extract_race_info()
#     #     entries = self.extract_race_entries()
#     #     self.save_to_db(race_info, entries)

#     #     print("データの保存が完了しました。")



                 
###ここからは、修正後のコード
# from bs4 import BeautifulSoup
# from datetime import datetime
# import os
# from collections.abc import MutableMapping

# # 使用するモデルをインポート（Race, RaceEntry, Horse, Jockey, Trainer, Payout など）
# from App_1.models import (
#     Race, RaceEntry, Horse, Jockey, Trainer,
#     Payout, CornerPassageRank, LapTime,RaceHTML
# )

# BASE_PATH = os.path.dirname(os.path.abspath(__file__))


# class ExtractInfo:
#     def __init__(self, race_id):
#         self.raceid = race_id
#         self.soup = None
#         self.html_path = os.path.join(BASE_PATH, 'RaceStatics', f'sample_{race_id}.html')

#         # 取得した情報を格納する変数
#         self.race_info = {}
#         self.race_entries = []
#         self.payouts = []
#         self.corners = []
#         self.lap_times = []

#     def open_file(self):
#         """
#         HTMLファイルをRaceHTMLモデルから読み込み、BeautifulSoupオブジェクトを作成
#         """
#         try:
#             # with open(self.html_path, 'r', encoding='utf-8') as file:
#             #     html_content = file.read()
#             #     self.soup = BeautifulSoup(html_content, 'html.parser')
#             html_content=RaceHTML.objects.get(race_id=self.raceid).html_text
#         except TypeError as e:
#             print(f'エラー:{e}')
            
#         except  :
#             print('an error occured')
#         else:
#             self.soup=BeautifulSoup(html_content, 'html.parser')
#             # print(self.soup)

#         # except FileNotFoundError:
#         #     print(f"Error: The file '{self.html_path}' was not found.")
#         # except PermissionError:
#         #     print(f"Error: Permission denied when trying to read the file '{self.html_path}'.")
#         # except Exception as e:
#         #     print(f"An unexpected error occurred while reading the file '{self.html_path}': {e}")

#     def extract_race_info(self):
#         """
#         レース情報（レース名、日付、距離、天候、馬場、発走時刻など）を抽出
#         """
#         # レース名 
#         race_name_tag = self.soup.find('p', class_='smalltxt')
#         race_name_text=race_name_tag.get_text(strip=True)
#         print(race_name_text)
#         if race_name_text:
#             race_name =race_name_text.split(' ')[1]
#             print(race_name)
#         else:
#             race_name = ''

#         # 例: "2024年1月6日 1回中山1日目 3歳未勝利 (混)[指](馬齢)"
#         details_tag = self.soup.find('p', class_='smalltxt')
#         if details_tag:

#             details_text = details_tag.get_text(strip=True)
#             # "2024年1月6日" だけ切り出して datetime に変換
#             date_str = details_text.split(' ')[0]  # "2024年1月6日"
#             try:
#                 race_date = datetime.strptime(date_str, '%Y年%m月%d日').date()
#             except ValueError:
#                 race_date = None
#         else:
#             race_date = None

#         # 例: "ダ右1200m / 天候 : 晴 / ダート : 良 / 発走 : 10:05"
#         snap_span = self.soup.find('diary_snap_cut')
#         if snap_span:
#             snap_text_tag = snap_span.find('span')
#         else:
#             snap_text_tag = None

#         distance = None
#         weather = None
#         track_condition = None
#         start_time = None

#         if snap_text_tag:
#             snap_text = snap_text_tag.get_text(strip=True)
#             # → "ダ右1200m / 天候 : 晴 / ダート : 良 / 発走 : 10:05"
#             # "/" 区切りで分割する
#             # ["ダ右1200m ", " 天候 : 晴 ", " ダート : 良 ", " 発走 : 10:05"]
#             parts = snap_text.split('/')
#             # parts[0] = "ダ右1200m "
#             # parts[1] = " 天候 : 晴 "
#             # parts[2] = " ダート : 良 "
#             # parts[3] = " 発走 : 10:05"

#             # 距離 (ダ右1200m → 1200)
#             if len(parts) > 0:
#                 dist_str = parts[0].replace('ダ右', '').replace('芝右', '').split('m')[0]
#                 # dist_str → "1200" など
#                 try:
#                     distance = int(dist_str)
#                 except ValueError:
#                     distance = None

#             # 天候 (" 天候 : 晴 " → 晴)
#             if len(parts) > 1:
#                 # parts[1] = " 天候 : 晴 "
#                 if ':' in parts[1]:
#                     weather = parts[1].split(':')[1].strip()

#             # 馬場 (" ダート : 良 " → 良)
#             if len(parts) > 2:
#                 # parts[2] = " ダート : 良 "
#                 if ':' in parts[2]:
#                     track_condition = parts[2].split(':')[1].strip()

#             # 発走 (" 発走 : 10:05" → 10:05)
#             if len(parts) > 3:
#                 # parts[3] = " 発走 : 10:05"
#                 if ':' in parts[3]:
#                     # parts[3] → " 発走 : 10:05"
#                     t = parts[3].split(':')
#                     # t → [" 発走 ", " 10", "05"]
#                     # ただし文字列前後に空白があるため、strip() で整形
#                     if len(t) >= 3:
#                         hour_str = t[1].strip()
#                         min_str = t[2].strip()
#                         start_time = f"{hour_str}:{min_str}"
#                     else:
#                         # 別途パターンによってはさらに分解が必要
#                         pass

#         self.race_info = {
#             'race_name': race_name,
#             'race_date': race_date,
#             'distance': distance,
#             'weather': weather,
#             'track_condition': track_condition,
#             # 必要なら 'start_time' フィールドを Race モデルに追加して保存する
#         }

#     def extract_race_entries(self):
#         """
#         レース出走馬情報を抽出する。
#         実際のHTML構造に合わせ、列インデックスを正しく取得。
#         """
#         race_table = self.soup.find('table', class_='race_table_01 nk_tb_common')
#         if not race_table:
#             return

#         # 1行目（tr class="txt_c"）はヘッダー
#         rows = race_table.find_all('tr')[1:]  # ヘッダを除く

#         entries = []
#         for row in rows:
#             cols = row.find_all('td')
#             # 各ト列を見ると、合計 21 列ある (0～20)
#             if len(cols) < 21:
#                 continue

#             # 列インデックスの対応関係（HTMLを目視で確認済み）
#             #  0: 着順
#             #  1: 枠番
#             #  2: 馬番
#             #  3: 馬名
#             #  4: 性齢
#             #  5: 斤量
#             #  6: 騎手
#             #  7: タイム
#             #  8: 着差
#             #  9: タイム指数(非表示など、実際には'**')
#             # 10: 通過(コーナーでの位置)
#             # 11: 上り(末脚タイム)
#             # 12: 単勝オッズ
#             # 13: 人気
#             # 14: 馬体重（例: "466(-12)"）
#             # 15: 調教タイム (省略)
#             # 16: 厩舎コメント (省略)
#             # 17: 備考 (省略)
#             # 18: 調教師 (例: "[東] 田中博康")
#             # 19: 馬主 (例: "サンデーレーシング")
#             # 20: 賞金(万円)

#             position_str = cols[0].get_text(strip=True)  # 着順
#             gate_str = cols[1].get_text(strip=True)      # 枠
#             horse_number_str = cols[2].get_text(strip=True)  # 馬番
#             horse_name = cols[3].get_text(strip=True)
#             sex_age = cols[4].get_text(strip=True)

#             # 斤量
#             weight_carried_str = cols[5].get_text(strip=True)
#             try:
#                 weight_carried = float(weight_carried_str)
#             except ValueError:
#                 weight_carried = None

#             jockey_name = cols[6].get_text(strip=True)

#             # タイム（例: "1:12.6"）
#             time_str = cols[7].get_text(strip=True)
#             # 単勝オッズ
#             odds_str = cols[12].get_text(strip=True)
#             try:
#                 odds = float(odds_str)
#             except ValueError:
#                 odds = None

#             # 人気
#             popularity_str = cols[13].get_text(strip=True)
#             try:
#                 popularity = int(popularity_str)
#             except ValueError:
#                 popularity = None

#             # 馬体重(例: "466(-12)" )
#             body_weight_str = cols[14].get_text(strip=True)
#             # 必要ならここで本体体重と増減をパースして格納
#             # 例: "466(-12)" → body_weight=466, body_weight_diff=-12
#             body_weight = None
#             body_weight_diff = None
#             # print(body_weight_str)
#             if body_weight_str:
#                 # いったんカッコ前後で分割
#                 # "466(-12)" → "466" and "-12"
#                 import re
#                 pattern = r'\(([-]?\d+)\)'  # 括弧内の数値（負の数も含む）にマッチ
#                 pattern = r'\(([-]?\d+)\)|\(([+]?\d+)\)'
#                 pattern = r'\(([-]?\d+)\)|\(\+?(\d+)\)'
#                 match = re.search(pattern, body_weight_str)
#                 # match = re.match(r"^(\d+)\(([-+]\d+)\)$", body_weight_str)
#                 if match:
#                     # print(match)
#                     # body_weight = int(match.group(0))
#                     number_str = match.group(1) or match.group(2)
#                     body_weight_diff = int(number_str)
#             # 調教師(例: "[東]\n田中博康")
#             trainer_str = cols[18].get_text(strip=True)
#             # "[東]"などの文字を取り除いておく
#             trainer_str = trainer_str.replace('[東]', '').replace('[西]', '').strip()

#             # 馬主 (cols[19]) → 例: "サンデーレーシング"
#             owner_str = cols[19].get_text(strip=True)

#             # 賞金(万円) (cols[20]) 例: "550.0"
#             prize_str = cols[20].get_text(strip=True)
#             try:
#                 prize = float(prize_str)
#             except ValueError:
#                 prize = None

#             # 着順を int 変換
#             try:
#                 position = int(position_str)
#             except ValueError:
#                 position = None

#             # gate / 馬番 を int 変換
#             try:
#                 gate = int(gate_str)
#             except ValueError:
#                 gate = None
#             try:
#                 horse_number = int(horse_number_str)
#             except ValueError:
#                 horse_number = None

#             entry_data = {
#                 'position': position,             # 着順
#                 'gate': gate,                     # 枠番
#                 'horse_number': horse_number,     # 馬番
#                 'horse_name': horse_name,
#                 'sex_age': sex_age,
#                 'weight_carried': weight_carried,
#                 'jockey_name': jockey_name,
#                 'time': time_str,
#                 'odds': odds,
#                 'popularity': popularity,
#                 'body_weight': body_weight,
#                 'body_weight_diff': body_weight_diff,
#                 'trainer_name': trainer_str,
#                 'owner_name': owner_str,
#                 'prize': prize,
#             }
#             entries.append(entry_data)

#         self.race_entries = entries

#     def extract_payouts(self):
#         """
#         払戻情報を抽出 (前回の例と同様)
#         """
#         payout_block = self.soup.find('dl', class_='pay_block')
#         if not payout_block:
#             return

#         tables = payout_block.find_all('table', class_='pay_table_01')
#         payouts = []
#         for table in tables:
#             rows = table.find_all('tr')
#             for row in rows:
#                 th = row.find('th')
#                 tds = row.find_all('td')

#                 if not th or len(tds) < 2:
#                     continue

#                 category = th.get_text(strip=True)  # 例: "単勝"、"複勝" など
#                 horse_gate_str = tds[0].get_text(strip=True)
#                 amount_str = tds[1].get_text(strip=True)

#                 # 金額から「円」や「,」を除去
#                 amount_str = amount_str.replace('円', '').replace(',', '')
#                 try:
#                     amount = float(amount_str)
#                 except ValueError:
#                     amount = 0.0

#                 # 人気をとれる場合はとる(例: 右端の td があれば読み取り)
#                 # 今回のHTMLでは3列目(tds[2])が人気だが、ジャンルにより列が違う場合もある
#                 popularity = None
#                 if len(tds) > 2:
#                     pop_str = tds[2].get_text(strip=True)
#                     try:
#                         popularity = int(pop_str)
#                     except:
#                         pass

#                 # 枠・馬番などが複数書かれている場合は、必要に応じて split して複数レコードに分解
#                 # ここでは単一扱い
#                 try:
#                     horse_gate = int(horse_gate_str)
#                 except ValueError:
#                     # 複数・ハイフン区切りなどは適宜パース
#                     horse_gate = 0

#                 payouts.append({
#                     'category': category,
#                     'horse_gate': horse_gate,
#                     'amount': amount,
#                     'popularity': popularity,
#                 })

#         self.payouts = payouts

#     def extract_corner_passages(self):
#         """
#         コーナー通過順位テーブル (summary='コーナー通過順位') を抽出
#         """
#         corner_table = self.soup.find('table', summary='コーナー通過順位')
#         if not corner_table:
#             return

#         corners = []
#         rows = corner_table.find_all('tr')
#         # 例: 
#         # <th>3コーナー</th>
#         # <td>2(11,14)-4(7,9,16)-(12,15)6=8-(5,13)10-(1,3)</td>
#         for row in rows:
#             th = row.find('th')
#             td = row.find('td')
#             if not th or not td:
#                 continue
#             corner_label = th.get_text(strip=True)
#             passage_order_str = td.get_text(strip=True)
#             corners.append({
#                 'corner': corner_label,
#                 'passage_order': passage_order_str,
#             })
#         self.corners = corners

#     def extract_lap_times(self):
#         """
#         ラップタイム (summary='ラップタイム') を抽出
#         例: 
#          ラップ: 11.8 - 10.7 - 11.4 - ...
#          ペース: ...
#         """
#         lap_time_table = self.soup.find('table', summary='ラップタイム')
#         if not lap_time_table:
#             return

#         lap_times = []
#         rows = lap_time_table.find_all('tr')
#         for row in rows:
#             th = row.find('th')
#             td = row.find('td')
#             if not th or not td:
#                 continue
#             category = th.get_text(strip=True)  # "ラップ", "ペース" など
#             value = td.get_text(strip=True)
#             # print(value)
#             lap_times.append({
#                 'category': category,
#                 # 実際に分割して200mごとなどに振り分けるなら追加実装
#                 'lap_text': value,
#             })

#         self.lap_times = lap_times

#     def save_to_db(self):
#         """
#         取得データをDjangoモデルへ保存
#         """
#         # --- Race ---
#         race, created = Race.objects.update_or_create(
#             race_id=self.raceid,
#             defaults={
#                 'race_name': self.race_info.get('race_name'),
#                 'date': self.race_info.get('race_date'),
#                 'distance': self.race_info.get('distance'),
#                 'weather': self.race_info.get('weather'),
#                 'track_condition': self.race_info.get('track_condition'),
#             }
#         )

#         # --- RaceEntry ---
#         for entry in self.race_entries:
#             # Horse
#             horse, _ = Horse.objects.update_or_create(
#                 name=entry['horse_name'],
#                 defaults={'sex_age': entry['sex_age']}
#             )

#             # Jockey
#             jockey, _ = Jockey.objects.update_or_create(
#                 name=entry['jockey_name']
#             )

#             # 調教師
#             trainer, _ = Trainer.objects.update_or_create(
#                 name=entry['trainer_name']
#             )

#             # 数値系のnull対策
#             gate = entry['gate'] if entry['gate'] is not None else None
#             horse_number = entry['horse_number'] if entry['horse_number'] is not None else None

#             # body_weight_diffを RaceEntry.body_weight_change に保存する例
#             # モデルに馬体重そのものを保存するフィールドがないため、必要ならモデル追加を検討
#             RaceEntry.objects.update_or_create(
#                 race=race,
#                 horse=horse,
#                 jockey=jockey,
#                 gate=gate,
#                 horse_number=horse_number,
#                 defaults={
#                     'weight_carried': entry['weight_carried'],
#                     'odds': entry['odds'],
#                     'popularity': entry['popularity'],
#                     'body_weight_change': entry['body_weight_diff'],  # 例として増減のみ保存
#                     'trainer': trainer,
#                     # position(着順)を格納したい場合は RaceEntry モデルにフィールド追加要
#                     # 'position': entry['position'],
#                     'OrderOfFinish':entry['position'],
#                     'body_weight_change':entry['body_weight_diff']
#                 }
#             )
#             # もし賞金を RaceEntry ではなく Race や Horse に保存したい場合は適宜変更
#         print('You`ve reached here!!')

#         # --- Payout ---
#         for p in self.payouts:
#             # print(p['amount'])
#             Payout.objects.update_or_create(
#                 race=race,
#                 category=p['category'],
#                 horse_gate=p['horse_gate'],
#                 defaults={
#                     'amount': p['amount'],
#                     'popularity': p['popularity'],
#                 }
#             )
#         # --- CornerPassageRank ---
#         for c in self.corners:
#             corner_label = c['corner']
#             passage_str = c['passage_order']
#             # コーナー内の通過順位を細かく保存したい場合は別途パースが必要
#             # print(passage_str)
#             CornerPassageRank.objects.update_or_create(
#                 race=race,
#                 defaults={
#                     'corner':corner_label,
#                     'passage_order':0  # 今回は簡略的に0にしている
#                 }
#             )
#         print("You've defenally reached here!!")
#         # --- LapTime ---

#         #LapTimeモデルで、フィールド名引用のためのサンプルデータを一件、作成しておく
#         LapTime.objects.update_or_create(
#             race=Race.objects.get(race_id=199013131313),
#             defaults={
#                 'category':'ラップ',
#                 'm200':float(12.34)
#             }
            
#         )
#         for lt in self.lap_times:
#             # print(lt)
#             #htmlより取得した、ラップデータの数値を、配列に格納
#             lap_split=[float(lap.split("\xa0")[0]) for lap in lt['lap_text'].split(' - ')]
#             # print(lap_split)
#             #Raceモデルの、サンプルデータを取得(race_id=199013131313)
#             laptime_query_set=LapTime.objects.all().first()
#             # 取得したクエリセットから、メタデータより、フィールド名の文字列が格納されたリストを作成
#             laptime_fields=laptime_query_set._meta.get_fields()
#             laptime_fields_name=[field.name for field in laptime_fields]
#             # print(laptime_fields_name)
#             #ラップデータ、フィールド名、それぞれのリストを使い、
#             #辞書を作成（update_or_create()メソッドの引数に代入する用）
#             lap_update_defaults_dict={}
#             for index in range(len(lap_split)):
#                 lap_update_defaults_dict[laptime_fields_name[4+index]]=lap_split[index]
#             # print(lap_update_defaults_dict)

#             LapTime.objects.update_or_create(
#                 race=race,
#                 category=lt['category'],
#                 defaults=lap_update_defaults_dict
#             )

#     def run(self):
#         """
#         全処理をまとめて実行
#         """
#         self.open_file()
#         if not self.soup:
#             return

#         print('Hello1')
#         self.extract_race_info()
#         print('Hello2')
#         self.extract_race_entries()
#         print('Hello3')
#         self.extract_payouts()
#         print('Hello4')
#         self.extract_corner_passages()
#         print('Hello5')
#         self.extract_lap_times()
#         print('Hello6')
#         self.save_to_db()
#         print("データの保存が完了しました。")

##再修正版コード
# from bs4 import BeautifulSoup
# from datetime import datetime
# import os
# from collections.abc import MutableMapping


# from App_1.models import (
#     Race, RaceEntry, Horse, Jockey, Trainer,
#     Payout, CornerPassageRank, LapTime, RaceHTML
# )

# BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# def parse_race_id(race_id: str) -> dict:
#     """
#     12桁の race_id から以下を抽出する:
#       - 年 (year)
#       - 開催場 (venue)  ← コードを日本語に変換
#       - 開催回数 (cycle_num)
#       - 開催日数 (day_num)
#       - レース番号 (race_num)
#     """
#     place_map = {
#         "01": "札幌",
#         "02": "函館",
#         "03": "福島",
#         "04": "新潟",
#         "05": "東京",
#         "06": "中山",
#         "07": "中京",
#         "08": "京都",
#         "09": "阪神",
#         "10": "小倉",
#     }

#     if len(race_id) != 12 or not race_id.isdigit():
#         raise ValueError("race_idは12桁の数字である必要があります。")

#     year_str = race_id[0:4]        # YYYY
#     place_code = race_id[4:6]      # MM
#     cycle_num_str = race_id[6:8]   # CC
#     day_num_str = race_id[8:10]    # DD
#     race_num_str = race_id[10:12]  # RR

#     year = int(year_str)
#     cycle_num = int(cycle_num_str)
#     day_num = int(day_num_str)
#     race_num = int(race_num_str)

#     # コードを開催場名に変換
#     venue = place_map.get(place_code, "不明な開催場コード")

#     return {
#         'year': year,
#         'venue': venue,
#         'cycle_num': cycle_num,
#         'day_num': day_num,
#         'race_num': race_num
#     }

# class ExtractInfo:
#     def __init__(self, race_id):
#         self.raceid = race_id
#         self.soup = None
#         self.html_path = os.path.join(BASE_PATH, 'RaceStatics', f'sample_{race_id}.html')

#         # 抽出した情報を格納
#         self.race_info = {}
#         self.race_entries = []
#         self.payouts = []
#         self.corners = []
#         self.lap_times = []

#     def open_file(self):
#         """
#         HTMLをRaceHTMLモデルから読み込んでBeautifulSoupへ
#         """
#         try:
#             html_content = RaceHTML.objects.get(race_id=self.raceid).html_text
#         except TypeError as e:
#             print(f'エラー:{e}')
#         except:
#             print('an error occured')
#         else:
#             self.soup = BeautifulSoup(html_content, 'html.parser')

#     def extract_race_info(self):
#         """
#         レースの基本情報を取得
#         """
#         # レース名 (例: "2024年1月6日 1回中山1日目 3歳未勝利 (混)[指](馬齢)")
#         race_name_tag = self.soup.find('p', class_='smalltxt')
#         race_name_text = race_name_tag.get_text(strip=True) if race_name_tag else ''
#         if race_name_text:
#             # 例: "2024年1月6日 1回中山1日目 3歳未勝利 (混)[指](馬齢)"
#             # スペース区切りで2番目あたりがレース名の一部…などHTML次第で調整
#             splitted = race_name_text.split(' ')
#             if len(splitted) > 1:
#                 race_name = splitted[1]
#             else:
#                 race_name = race_name_text
#         else:
#             race_name = ''

#         # 開催日 (HTML上の日付)
#         # 例: "2024年1月6日"
#         details_tag = self.soup.find('p', class_='smalltxt')
#         if details_tag:
#             details_text = details_tag.get_text(strip=True)
#             date_str = details_text.split(' ')[0]  # "2024年1月6日"
#             try:
#                 race_date = datetime.strptime(date_str, '%Y年%m月%d日').date()
#             except ValueError:
#                 race_date = None
#         else:
#             race_date = None

#         # 距離・天候など (diary_snap_cut の下の spanタグ想定)
#         snap_span = self.soup.find('diary_snap_cut')
#         if snap_span:
#             snap_text_tag = snap_span.find('span')
#         else:
#             snap_text_tag = None

#         distance = None
#         weather = None
#         track_condition = None

#         if snap_text_tag:
#             snap_text = snap_text_tag.get_text(strip=True)
#             parts = snap_text.split('/')
#             if len(parts) > 0:
#                 dist_str = parts[0].replace('ダ右', '').replace('芝右', '').split('m')[0]
#                 try:
#                     distance = int(dist_str)
#                 except ValueError:
#                     distance = None

#             if len(parts) > 1:
#                 if ':' in parts[1]:
#                     weather = parts[1].split(':')[1].strip()

#             if len(parts) > 2:
#                 if ':' in parts[2]:
#                     track_condition = parts[2].split(':')[1].strip()

#         self.race_info = {
#             'race_name': race_name,
#             'race_date': race_date,
#             'distance': distance,
#             'weather': weather,
#             'track_condition': track_condition,
#         }

#     def extract_race_entries(self):
#         """
#         出走馬情報をテーブルから取得
#         """
#         race_table = self.soup.find('table', class_='race_table_01 nk_tb_common')
#         if not race_table:
#             return

#         rows = race_table.find_all('tr')[1:]  # ヘッダを除く

#         entries = []
#         for row in rows:
#             cols = row.find_all('td')
#             if len(cols) < 21:
#                 continue
#             position_str = cols[0].get_text(strip=True)
#             gate_str = cols[1].get_text(strip=True)
#             horse_number_str = cols[2].get_text(strip=True)
#             horse_name = cols[3].get_text(strip=True)
#             sex_age = cols[4].get_text(strip=True)

#             weight_carried_str = cols[5].get_text(strip=True)
#             try:
#                 weight_carried = float(weight_carried_str)
#             except ValueError:
#                 weight_carried = None

#             jockey_name = cols[6].get_text(strip=True)
#             time_str = cols[7].get_text(strip=True)

#             odds_str = cols[12].get_text(strip=True)
#             try:
#                 odds = float(odds_str)
#             except ValueError:
#                 odds = None

#             popularity_str = cols[13].get_text(strip=True)
#             try:
#                 popularity = int(popularity_str)
#             except ValueError:
#                 popularity = None

#             body_weight_str = cols[14].get_text(strip=True)
#             body_weight = None
#             body_weight_diff = None
#             if body_weight_str:
#                 import re
#                 pattern = r'\(([-]?\d+)\)|\(\+?(\d+)\)'
#                 match = re.search(pattern, body_weight_str)
#                 if match:
#                     number_str = match.group(1) or match.group(2)
#                     body_weight_diff = int(number_str)

#             trainer_str = cols[18].get_text(strip=True)
#             trainer_str = trainer_str.replace('[東]', '').replace('[西]', '').strip()

#             owner_str = cols[19].get_text(strip=True)

#             prize_str = cols[20].get_text(strip=True)
#             try:
#                 prize = float(prize_str)
#             except ValueError:
#                 prize = None

#             try:
#                 position = int(position_str)
#             except ValueError:
#                 position = None

#             try:
#                 gate = int(gate_str)
#             except ValueError:
#                 gate = None

#             try:
#                 horse_number = int(horse_number_str)
#             except ValueError:
#                 horse_number = None

#             entry_data = {
#                 'position': position,
#                 'gate': gate,
#                 'horse_number': horse_number,
#                 'horse_name': horse_name,
#                 'sex_age': sex_age,
#                 'weight_carried': weight_carried,
#                 'jockey_name': jockey_name,
#                 'time': time_str,
#                 'odds': odds,
#                 'popularity': popularity,
#                 'body_weight': body_weight,
#                 'body_weight_diff': body_weight_diff,
#                 'trainer_name': trainer_str,
#                 'owner_name': owner_str,
#                 'prize': prize,
#             }
#             entries.append(entry_data)

#         self.race_entries = entries

#     def extract_payouts(self):
#         """
#         払戻情報を抽出
#         """
#         payout_block = self.soup.find('dl', class_='pay_block')
#         if not payout_block:
#             return

#         tables = payout_block.find_all('table', class_='pay_table_01')
#         payouts = []
#         for table in tables:
#             rows = table.find_all('tr')
#             for row in rows:
#                 th = row.find('th')
#                 tds = row.find_all('td')
#                 if not th or len(tds) < 2:
#                     continue

#                 category = th.get_text(strip=True)
#                 horse_gate_str = tds[0].get_text(strip=True)
#                 amount_str = tds[1].get_text(strip=True)

#                 amount_str = amount_str.replace('円', '').replace(',', '')
#                 try:
#                     amount = float(amount_str)
#                 except ValueError:
#                     amount = 0.0

#                 popularity = None
#                 if len(tds) > 2:
#                     pop_str = tds[2].get_text(strip=True)
#                     try:
#                         popularity = int(pop_str)
#                     except:
#                         pass

#                 try:
#                     horse_gate = int(horse_gate_str)
#                 except ValueError:
#                     horse_gate = 0

#                 payouts.append({
#                     'category': category,
#                     'horse_gate': horse_gate,
#                     'amount': amount,
#                     'popularity': popularity,
#                 })

#         self.payouts = payouts

#     def extract_corner_passages(self):
#         """
#         コーナー通過順位を抽出
#         """
#         corner_table = self.soup.find('table', summary='コーナー通過順位')
#         if not corner_table:
#             return

#         corners = []
#         rows = corner_table.find_all('tr')
#         for row in rows:
#             th = row.find('th')
#             td = row.find('td')
#             if not th or not td:
#                 continue
#             corner_label = th.get_text(strip=True)
#             passage_order_str = td.get_text(strip=True)
#             corners.append({
#                 'corner': corner_label,
#                 'passage_order': passage_order_str,
#             })
#         self.corners = corners

#     def extract_lap_times(self):
#         """
#         ラップタイムを抽出
#         """
#         lap_time_table = self.soup.find('table', summary='ラップタイム')
#         if not lap_time_table:
#             return

#         lap_times = []
#         rows = lap_time_table.find_all('tr')
#         for row in rows:
#             th = row.find('th')
#             td = row.find('td')
#             if not th or not td:
#                 continue
#             category = th.get_text(strip=True)
#             value = td.get_text(strip=True)
#             lap_times.append({
#                 'category': category,
#                 'lap_text': value,
#             })
#         self.lap_times = lap_times

#     def save_to_db(self):
#         """
#         取得したデータを Djangoモデルへ保存
#         """
#         # === ここで race_id を解析して辞書を取得 ===
#         parsed_id = parse_race_id(str(self.raceid))
#         # parsed_id = {
#         #   'year': 2013, 
#         #   'venue': '中山', 
#         #   'cycle_num': 12, 
#         #   'day_num': 12, 
#         #   'race_num': 12
#         # }

#         # --- Race ---
#         race, created = Race.objects.update_or_create(
#             race_id=self.raceid,
#             defaults={
#                 'race_name': self.race_info.get('race_name'),
#                 # 日付はHTMLから抽出したものを優先
#                 'date': self.race_info.get('race_date'),
#                 'distance': self.race_info.get('distance'),
#                 'weather': self.race_info.get('weather'),
#                 'track_condition': self.race_info.get('track_condition'),
#                 # ↓ ここで年, コース, (レース番号) を追加して保存
#                 'year': parsed_id['year'],
#                 'course': parsed_id['venue'],
#                 # race_numberフィールドを「第何レースか」に使う場合:
#                 'race_number': parsed_id['race_num'],
#             }
#         )

#         # --- RaceEntry ---
#         for entry in self.race_entries:
#             # Horse
#             horse, _ = Horse.objects.update_or_create(
#                 name=entry['horse_name'],
#                 defaults={'sex_age': entry['sex_age']}
#             )
#             print(horse.name)

#             # Jockey
#             jockey, _ = Jockey.objects.update_or_create(
#                 name=entry['jockey_name']
#             )
#             print(jockey.name)
#             # 調教師
#             trainer, _ = Trainer.objects.update_or_create(
#                 name=entry['trainer_name']
#             )

#             gate = entry['gate'] if entry['gate'] is not None else None
#             horse_number = entry['horse_number'] if entry['horse_number'] is not None else None
#             try:
#                 RaceEntry.objects.update_or_create(
#                     race=race,
#                     horse=horse,
#                     jockey=jockey,
#                     gate=gate,
#                     horse_number=horse_number,
#                     defaults={
#                         'weight_carried': entry['weight_carried'],
#                         'odds': entry['odds'],
#                         'popularity': entry['popularity'],
#                         'body_weight_change': entry['body_weight_diff'],
#                         'trainer': trainer,
#                         'order_of_finish': entry['position'],
#                     }
#                 )
#             except :
#                 print('RaceEntryモデルへの保存で、何かしらのエラーが発生しました。')
#                 try:
#                     RaceEntry.objects.create(
#                         race=race,
#                         horse=horse,
#                         jockey=jockey,
#                         gate=gate,
#                         horse_number=horse_number,
#                     )
#                 except:
#                     print(f'データを作成できないようです{self.raceid}')
#                 else:
#                     RaceEntry.objects.filter(
#                         race=race,
#                         horse=horse,
#                         jockey=jockey,
#                         gate=gate,
#                         horse_number=horse_number,
#                     ).delete()
#                     RaceEntry.objects.update_or_create(
#                         race=race,
#                         horse=horse,
#                         jockey=jockey,
#                         gate=gate,
#                         horse_number=horse_number,
#                         defaults={
#                             'weight_carried': entry['weight_carried'],
#                             'odds': entry['odds'],
#                             'popularity': entry['popularity'],
#                             'body_weight_change': entry['body_weight_diff'],
#                             'trainer': trainer,
#                             'order_of_finish': entry['position'],
#                         }
#                     )
#                     print('データは作成されました。')
#             finally:
#                 print(f'順位は{entry['position']}です')
#         print('You`ve reached here!!')

#         # --- Payout ---
#         for p in self.payouts:
#             Payout.objects.update_or_create(
#                 race=race,
#                 category=p['category'],
#                 horse_gate=p['horse_gate'],
#                 defaults={
#                     'amount': p['amount'],
#                     'popularity': p['popularity'],
#                 }
#             )

#         # --- CornerPassageRank ---
#         for c in self.corners:
#             corner_label = c['corner']
#             passage_str = c['passage_order']
#             CornerPassageRank.objects.update_or_create(
#                 race=race,
#                 # cornerをユニークに扱いたい場合は filter条件に corner_label を含める
#                 defaults={
#                     'corner': corner_label,
#                     'passage_order': 0  # ここでは簡略化
#                 }
#             )
#         print("You've definitely reached here!!")

#         # --- LapTime ---
#         # (サンプル) まずは固定のサンプルを1件作成
#         LapTime.objects.update_or_create(
#             race=Race.objects.get(race_id=199013131313),
#             defaults={
#                 'category': 'ラップ',
#                 'm200': float(12.34)
#             }
#         )
#         # 実際のレースのラップタイムを保存
#         for lt in self.lap_times:
#             try:
#                 lap_split = [float(lap.split("\xa0")[0]) for lap in lt['lap_text'].split(' - ')]
#                 laptime_query_set = LapTime.objects.all().first()
#                 laptime_fields = laptime_query_set._meta.get_fields()
#                 laptime_fields_name = [field.name for field in laptime_fields]
#                 lap_update_defaults_dict = {}
#                 for index in range(len(lap_split)):
#                     # laptime_fields_name[4+index] は m200, m400, ...等のフィールドに相当
#                     lap_update_defaults_dict[laptime_fields_name[4 + index]] = lap_split[index]

#                 LapTime.objects.update_or_create(
#                     race=race,
#                     category=lt['category'],
#                     defaults=lap_update_defaults_dict
#                 )
#             except:
#                 LapTime.objects.update_or_create(
#                     race=race,
#                 )
#             # if not laptime_query_set:
#             #     continue
                

#     def run(self):
#         """
#         全処理をまとめて実行
#         """
#         self.open_file()
#         if not self.soup:
#             return

#         print('Hello1')
#         self.extract_race_info()
#         print('Hello2')
#         self.extract_race_entries()
#         print('Hello3')
#         self.extract_payouts()
#         print('Hello4')
#         self.extract_corner_passages()
#         print('Hello5')
#         self.extract_lap_times()
#         print('Hello6')
#         self.save_to_db()
#         print("データの保存が完了しました。")


#再々修正版コード
# from bs4 import BeautifulSoup
# from datetime import datetime
# import os,re
# from collections.abc import MutableMapping

# from App_1.models import (
#     Race, RaceEntry, Horse, Jockey, Trainer,
#     Payout, CornerPassageRank, LapTime, RaceHTML
# )

# BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# def parse_race_id(race_id: str) -> dict:
#     """
#     12桁の race_id から以下を抽出する:
#       - 年 (year)
#       - 開催場 (venue)  ← コードを日本語に変換
#       - 開催回数 (cycle_num)
#       - 開催日数 (day_num)
#       - レース番号 (race_num)
#     """
#     place_map = {
#         "01": "札幌",
#         "02": "函館",
#         "03": "福島",
#         "04": "新潟",
#         "05": "東京",
#         "06": "中山",
#         "07": "中京",
#         "08": "京都",
#         "09": "阪神",
#         "10": "小倉",
#     }

#     if len(race_id) != 12 or not race_id.isdigit():
#         raise ValueError("race_idは12桁の数字である必要があります。")

#     year_str = race_id[0:4]        # YYYY
#     place_code = race_id[4:6]      # MM
#     cycle_num_str = race_id[6:8]   # CC
#     day_num_str = race_id[8:10]    # DD
#     race_num_str = race_id[10:12]  # RR

#     year = int(year_str)
#     cycle_num = int(cycle_num_str)
#     day_num = int(day_num_str)
#     race_num = int(race_num_str)

#     # コードを開催場名に変換
#     venue = place_map.get(place_code, "不明な開催場コード")

#     return {
#         'year': year,
#         'venue': venue,
#         'cycle_num': cycle_num,
#         'day_num': day_num,
#         'race_num': race_num
#     }

# class ExtractInfo:
#     def __init__(self, race_id):
#         self.raceid = race_id
#         self.soup = None
#         self.html_path = os.path.join(BASE_PATH, 'RaceStatics', f'sample_{race_id}.html')

#         # 抽出した情報を格納
#         self.race_info = {}
#         self.race_entries = []
#         self.payouts = []
#         self.corners = []
#         self.lap_times = []

#     def open_file(self):
#         """
#         HTMLをRaceHTMLモデルから読み込んでBeautifulSoupへ
#         """
#         try:
#             html_content = RaceHTML.objects.get(race_id=self.raceid).html_text
#         except TypeError as e:
#             print(f'エラー:{e}')
#         except:
#             print('an error occured')
#         else:
#             self.soup = BeautifulSoup(html_content, 'html.parser')

#     def extract_race_info(self):
#         """
#         レースの基本情報を取得
#         """

#         # --- ① レース名を <h1> タグから取得 ---
#         title_tag = self.soup.find('title')
#         if title_tag:
#             # コメントや余分な空白があっても strip=True で除去
#             try:
#                 race_name_text = re.match(r'^(.*?)\s*[｜|]', title_tag.get_text(strip=True)).group(1).strip()
#             except:
#                 race_name_text=''
#         else:
#             race_name_text = ''

#         # 例: <h1>3歳未勝利<!--img ...--></h1> → "3歳未勝利" が欲しいのでここで上書き
#         race_name = race_name_text

#         # --- ② <p class="smalltxt"> に含まれる日付を取得 (既存ロジック) ---
#         details_tag = self.soup.find('p', class_='smalltxt')
#         if details_tag:
#             details_text = details_tag.get_text(strip=True)
#             # "2024年1月6日 1回中山1日目 3歳未勝利 (混)[指](馬齢)" → 日付部分だけ取り出す
#             date_str = details_text.split(' ')[0]  # "2024年1月6日"
#             try:
#                 race_date = datetime.strptime(date_str, '%Y年%m月%d日').date()
#             except ValueError:
#                 race_date = None
#         else:
#             race_date = None

#         # --- ③ 芝・天候・馬場状態などを <span> ～ から取得 ---
#         snap_span = self.soup.find('diary_snap_cut')
#         if snap_span:
#             snap_text_tag = snap_span.find('span')
#         else:
#             snap_text_tag = None

#         distance = None
#         weather = None
#         track_condition = None
#         race_type = None  # ← 新規追加

#         if snap_text_tag:
#             snap_text = snap_text_tag.get_text(strip=True)
#             # 例: "芝右2000m / 天候 : 晴 / 芝 : 良 / 発走 : 12:25"
#             parts = [p.strip() for p in snap_text.split('/')]

#             if len(parts) > 0:
#                 # parts[0] = "芝右2000m"
#                 dist_str = parts[0]
#                 # レース種別を判定する
#                 if '障' in dist_str:
#                     race_type = '障害'
#                 elif 'ダ' in dist_str:
#                     race_type = 'ダート'
#                 elif '芝' in dist_str:
#                     race_type = '芝'
#                 else:
#                     race_type = '不明'

#                 # 距離を数値化 (例: "芝右2000m" → "2000" → 2000)
#                 dist_str_numeric = dist_str.replace('ダ右', '')\
#                                           .replace('芝右', '')\
#                                           .replace('ダ左', '')\
#                                           .replace('芝左', '')\
#                                           .replace('障', '')\
#                                           .replace('外','')\
#                                           .replace('ダート','')\
#                                           .replace('芝','')\
#                                           .split('m')[0]
#                 try:
#                     distance = int(dist_str_numeric)
#                     print(f'成功{dist_str_numeric}')
#                 except ValueError:
#                     distance = None
#                     print(f'{dist_str_numeric}-------------------------------------')

#             if len(parts) > 1:
#                 # parts[1] = "天候 : 晴"
#                 if ':' in parts[1]:
#                     # "天候 : 晴" → "晴"
#                     weather = parts[1].split(':')[1].strip()

#             if len(parts) > 2:
#                 # parts[2] = "芝 : 良" or "ダート : 稍重" など
#                 if ':' in parts[2]:
#                     track_condition = parts[2].split(':')[1].strip()

#         # --- race_info に格納 ---
#         self.race_info = {
#             'race_name': race_name,
#             'race_date': race_date,
#             'distance': distance,
#             'weather': weather,
#             'track_condition': track_condition,
#             'race_type': race_type,   # ← 新規追加
#         }

#     def extract_race_entries(self):
#         """
#         出走馬情報をテーブルから取得
#         """
#         race_table = self.soup.find('table', class_='race_table_01 nk_tb_common')
#         if not race_table:
#             return

#         rows = race_table.find_all('tr')[1:]  # ヘッダを除く

#         entries = []
#         for row in rows:
#             cols = row.find_all('td')
#             if len(cols) < 21:
#                 continue
#             position_str = cols[0].get_text(strip=True)
#             gate_str = cols[1].get_text(strip=True)
#             horse_number_str = cols[2].get_text(strip=True)
#             horse_name = cols[3].get_text(strip=True)
#             sex_age = cols[4].get_text(strip=True)

#             weight_carried_str = cols[5].get_text(strip=True)
#             try:
#                 weight_carried = float(weight_carried_str)
#             except ValueError:
#                 weight_carried = None

#             jockey_name = cols[6].get_text(strip=True)
#             time_str = cols[7].get_text(strip=True)

#             odds_str = cols[12].get_text(strip=True)
#             try:
#                 odds = float(odds_str)
#             except ValueError:
#                 odds = None

#             popularity_str = cols[13].get_text(strip=True)
#             try:
#                 popularity = int(popularity_str)
#             except ValueError:
#                 popularity = None

#             body_weight_str = cols[14].get_text(strip=True)
#             body_weight_diff = None
#             if body_weight_str:
#                 import re
#                 pattern = r'\(([-]?\d+)\)|\(\+?(\d+)\)'
#                 match = re.search(pattern, body_weight_str)
#                 if match:
#                     number_str = match.group(1) or match.group(2)
#                     body_weight_diff = int(number_str)

#             trainer_str = cols[18].get_text(strip=True)
#             trainer_str = trainer_str.replace('[東]', '').replace('[西]', '').strip()

#             owner_str = cols[19].get_text(strip=True)

#             prize_str = cols[20].get_text(strip=True)
#             try:
#                 prize = float(prize_str)
#             except ValueError:
#                 prize = None

#             try:
#                 position = int(position_str)
#             except ValueError:
#                 position = None

#             try:
#                 gate = int(gate_str)
#             except ValueError:
#                 gate = None

#             try:
#                 horse_number = int(horse_number_str)
#             except ValueError:
#                 horse_number = None

#             entry_data = {
#                 'position': position,
#                 'gate': gate,
#                 'horse_number': horse_number,
#                 'horse_name': horse_name,
#                 'sex_age': sex_age,
#                 'weight_carried': weight_carried,
#                 'jockey_name': jockey_name,
#                 'time': time_str,
#                 'odds': odds,
#                 'popularity': popularity,
#                 'body_weight_diff': body_weight_diff,
#                 'trainer_name': trainer_str,
#                 'owner_name': owner_str,
#                 'prize': prize,
#             }
#             entries.append(entry_data)

#         self.race_entries = entries

#     def extract_payouts(self):
#         """
#         払戻情報を抽出
#         """
#         payout_block = self.soup.find('dl', class_='pay_block')
#         if not payout_block:
#             return

#         tables = payout_block.find_all('table', class_='pay_table_01')
#         payouts = []
#         for table in tables:
#             rows = table.find_all('tr')
#             for row in rows:
#                 th = row.find('th')
#                 tds = row.find_all('td')
#                 if not th or len(tds) < 2:
#                     continue

#                 category = th.get_text(strip=True)
#                 horse_gate_str = tds[0].get_text(strip=True)
#                 amount_str = tds[1].get_text(strip=True)

#                 # 金額（"," や "円" を除去してfloat化）
#                 amount_str = amount_str.replace('円', '').replace(',', '')
#                 try:
#                     amount = float(amount_str)
#                 except ValueError:
#                     amount = 0.0

#                 popularity = None
#                 if len(tds) > 2:
#                     pop_str = tds[2].get_text(strip=True)
#                     try:
#                         popularity = int(pop_str)
#                     except:
#                         pass

#                 try:
#                     horse_gate = int(horse_gate_str)
#                 except ValueError:
#                     horse_gate = 0

#                 payouts.append({
#                     'category': category,
#                     'horse_gate': horse_gate,
#                     'amount': amount,
#                     'popularity': popularity,
#                 })

#         self.payouts = payouts

#     def extract_corner_passages(self):
#         """
#         コーナー通過順位を抽出
#         """
#         corner_table = self.soup.find('table', summary='コーナー通過順位')
#         if not corner_table:
#             return

#         corners = []
#         rows = corner_table.find_all('tr')
#         for row in rows:
#             th = row.find('th')
#             td = row.find('td')
#             if not th or not td:
#                 continue
#             corner_label = th.get_text(strip=True)
#             passage_order_str = td.get_text(strip=True)
#             corners.append({
#                 'corner': corner_label,
#                 'passage_order': passage_order_str,
#             })
#         self.corners = corners

#     def extract_lap_times(self):
#         """
#         ラップタイムを抽出
#         """
#         lap_time_table = self.soup.find('table', summary='ラップタイム')
#         if not lap_time_table:
#             return

#         lap_times = []
#         rows = lap_time_table.find_all('tr')
#         for row in rows:
#             th = row.find('th')
#             td = row.find('td')
#             if not th or not td:
#                 continue
#             category = th.get_text(strip=True)
#             value = td.get_text(strip=True)
#             lap_times.append({
#                 'category': category,
#                 'lap_text': value,
#             })
#         self.lap_times = lap_times

#     def save_to_db(self):
#         """
#         取得したデータを Djangoモデルへ保存
#         """
#         parsed_id = parse_race_id(str(self.raceid))

#         # --- Raceモデルへ保存 ---
#         race, created = Race.objects.update_or_create(
#             race_id=self.raceid,
#             defaults={
#                 'race_name': self.race_info.get('race_name'),
#                 'date': self.race_info.get('race_date'),
#                 'distance': self.race_info.get('distance'),
#                 'weather': self.race_info.get('weather'),
#                 'track_condition': self.race_info.get('track_condition'),
#                 'year': parsed_id['year'],
#                 'course': parsed_id['venue'],
#                 'race_number': parsed_id['race_num'],

#                 # ここでレース種別を保存
#                 'race_type': self.race_info.get('race_type'),  # ← 新規追加
#             }
#         )

#         # --- RaceEntry ---
#         for entry in self.race_entries:
#             # Horse
#             horse, _ = Horse.objects.update_or_create(
#                 name=entry['horse_name'],
#                 defaults={'sex_age': entry['sex_age']}
#             )
#             # Jockey
#             jockey, _ = Jockey.objects.update_or_create(
#                 name=entry['jockey_name']
#             )
#             # Trainer
#             trainer, _ = Trainer.objects.update_or_create(
#                 name=entry['trainer_name']
#             )

#             gate = entry['gate']
#             horse_number = entry['horse_number']
#             try:
#                 RaceEntry.objects.update_or_create(
#                     race=race,
#                     horse=horse,
#                     jockey=jockey,
#                     gate=gate,
#                     horse_number=horse_number,
#                     defaults={
#                         'weight_carried': entry['weight_carried'],
#                         'odds': entry['odds'],
#                         'popularity': entry['popularity'],
#                         'body_weight_change': entry['body_weight_diff'],
#                         'trainer': trainer,
#                         'order_of_finish': entry['position'],
#                     }
#                 )
#             except:
#                 print('RaceEntryモデルへの保存でエラーが発生しました。')
#                 # 必要に応じて例外処理を入れる

#         # --- Payout ---
#         for p in self.payouts:
#             Payout.objects.update_or_create(
#                 race=race,
#                 category=p['category'],
#                 horse_gate=p['horse_gate'],
#                 defaults={
#                     'amount': p['amount'],
#                     'popularity': p['popularity'],
#                 }
#             )

#         # --- CornerPassageRank ---
#         for c in self.corners:
#             corner_label = c['corner']
#             passage_str = c['passage_order']
#             # 例では corner だけをキーにして update_or_create しているが、
#             # 実際には複数行に分割するなど必要があれば工夫
#             CornerPassageRank.objects.update_or_create(
#                 race=race,
#                 corner=corner_label,
#                 defaults={
#                     # passage_order フィールドは単一の順位保存だが、
#                     # 実際は "1-2-3" のように文字列で来る場合もある。
#                     'passage_order': 0
#                 }
#             )

#         # --- LapTime ---
#         for lt in self.lap_times:
#             try:
#                 # "12.5 - 10.6 - 12.6 - ..." などの形を数値に変換
#                 lap_split = [float(lap.strip()) for lap in lt['lap_text'].split('-')]
#                 # 既存のLapTimeインスタンスのフィールド一覧を利用して動的にマッピング
#                 laptime_query_set = LapTime.objects.all().first()
#                 # 万が一まだ一件もLapTimeが無い場合はスキップ
#                 if not laptime_query_set:
#                     continue
#                 laptime_fields = laptime_query_set._meta.get_fields()
#                 laptime_fields_name = [field.name for field in laptime_fields]

#                 # index 0 から順番に m200, m400... に入れるイメージ
#                 lap_update_defaults_dict = {}
#                 # laptime_fields_name の最初には id, item, race などがあるため
#                 # m200フィールドが何番目かを確認する
#                 # ここでは雑に "m200" フィールドのindexを探している例
#                 start_idx = laptime_fields_name.index('m200')

#                 for index, lap_val in enumerate(lap_split):
#                     field_name = laptime_fields_name[start_idx + index]
#                     lap_update_defaults_dict[field_name] = lap_val

#                 LapTime.objects.update_or_create(
#                     race=race,
#                     category=lt['category'],
#                     defaults=lap_update_defaults_dict
#                 )
#             except:
#                 # 簡易的に例外を握りつぶしておく
#                 LapTime.objects.update_or_create(
#                     race=race,
#                     category=lt['category'],
#                 )

#     def run(self):
#         """
#         全処理をまとめて実行
#         """
#         self.open_file()
#         if not self.soup:
#             return

#         self.extract_race_info()
#         # self.extract_race_entries()
#         # self.extract_payouts()
#         # self.extract_corner_passages()
#         # self.extract_lap_times()
#         self.save_to_db()
#         print("データの保存が完了しました。")

###再々修正版のオブジェクト指向リファクタリング版
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re

from App_1.models import (
    Race, RaceEntry, Horse, Jockey, Trainer,
    Payout, CornerPassageRank, LapTime,Owner, RaceHTML
)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# ----------------------------
# 共通的なユーティリティ関数
# ----------------------------

def parse_race_id(race_id: str) -> dict:
    """
    12桁の race_id から以下を抽出する:
      - 年 (year)
      - 開催場 (venue)  ← コードを日本語に変換
      - 開催回数 (cycle_num)
      - 開催日数 (day_num)
      - レース番号 (race_num)
    """
    place_map = {
        "01": "札幌",
        "02": "函館",
        "03": "福島",
        "04": "新潟",
        "05": "東京",
        "06": "中山",
        "07": "中京",
        "08": "京都",
        "09": "阪神",
        "10": "小倉",
    }

    if len(race_id) != 12 or not race_id.isdigit():
        raise ValueError("race_idは12桁の数字である必要があります。")

    year_str = race_id[0:4]        # YYYY
    place_code = race_id[4:6]      # MM
    cycle_num_str = race_id[6:8]   # CC
    day_num_str = race_id[8:10]    # DD
    race_num_str = race_id[10:12]  # RR

    venue = place_map.get(place_code, "不明な開催場コード")

    return {
        'year': int(year_str),
        'venue': venue,
        'cycle_num': int(cycle_num_str),
        'day_num': int(day_num_str),
        'race_num': int(race_num_str)
    }

def try_parse_float(value: str) -> float | None:
    """
    文字列をfloatに変換できる場合は変換して返す。
    変換できない場合は None を返す。
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def try_parse_int(value: str) -> int | None:
    """
    文字列をintに変換できる場合は変換して返す。
    変換できない場合は None を返す。
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

# ----------------------------------------
# 1) RaceHTML の取得と BeautifulSoup 生成
# ----------------------------------------
class RaceHTMLFetcher:
    """
    RaceHTMLモデルからHTMLテキストを取得し、BeautifulSoupオブジェクトを返す。
    """
    def __init__(self, race_id: str):
        self.race_id = race_id
        self.soup = None

    def get_soup(self) -> BeautifulSoup | None:
        try:
            html_content = RaceHTML.objects.get(race__race_id=self.race_id).html_text
            self.soup = BeautifulSoup(html_content, 'html.parser')
        except RaceHTML.DoesNotExist:
            print(f"RaceHTML(race_id={self.race_id}) がDBに存在しません。")
            self.soup = None
        except Exception as e:
            print(f"HTML取得時にエラーが発生しました: {e}")
            self.soup = None

        return self.soup

# -----------------------------------
# 2) HTML解析クラス (Parser)
# -----------------------------------
class RaceParser:
    """
    BeautifulSoupオブジェクトから、レースに関する各種データを抽出する。
    解析結果は辞書やリストの形で保持・返却する。
    """
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def parse_all(self) -> dict:
        """
        全ての解析を実行し、結果を辞書にまとめて返す。
        """
        return {
            'race_info': self._parse_race_info(),
            'race_entries': self._parse_race_entries(),
            'payouts': self._parse_payouts(),
            'corners': self._parse_corner_passages(),
            'lap_times': self._parse_lap_times()
        }

    def _parse_race_info(self) -> dict:
        """
        レースの基本情報を取得
        旧コードでの改良ロジック（titleタグからレース名を取得、レースタイプ等）を反映
        """
        # -----------------------------
        # ① レース名を <title> から優先取得
        # -----------------------------
        race_name = ""
        title_tag = self.soup.find('title')
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            # 例: 「3歳未勝利｜JRA」 → 「3歳未勝利」を取得したい
            m = re.match(r'^(.*?)\s*[｜|]', title_text)
            if m:
                race_name = m.group(1).strip()
            else:
                # 取得できなかった場合はとりあえずタイトル全文を入れる
                race_name = title_text

        # -----------------------------
        # ② <p class="smalltxt"> から日付や予備のレース名を取得
        #    (titleタグから取れなかった場合のフォールバックにも使う)
        # -----------------------------
        race_date = None
        smalltxt_tag = self.soup.find('p', class_='smalltxt')
        if smalltxt_tag:
            details_text = smalltxt_tag.get_text(strip=True)
            # "2024年1月6日 1回中山1日目 3歳未勝利 (混)[指](馬齢)" の例
            parts = details_text.split()
            if len(parts) > 0:
                # parts[0] には "2024年1月6日" が入るはず
                date_str = parts[0]
                try:
                    race_date = datetime.strptime(date_str, '%Y年%m月%d日').date()
                except ValueError:
                    race_date = None

            # タイトルから取れなかった場合はこちらをレース名に
            if not race_name and len(parts) > 1:
                race_name = parts[1]
        
        # -----------------------------
        # ③ 芝/ダ/障などのレースタイプ ＆ 距離・天候・馬場状態を取得
        # -----------------------------
        snap_span = self.soup.find('diary_snap_cut')
        if snap_span:
            snap_text_tag = snap_span.find('span')
        else:
            snap_text_tag = None

        distance = None
        weather = None
        track_condition = None
        race_type = None

        if snap_text_tag:
            snap_text = snap_text_tag.get_text(strip=True)
            # 例: "芝右2000m / 天候 : 晴 / 芝 : 良 / 発走 : 12:25"
            parts = [p.strip() for p in snap_text.split('/')]

            if len(parts) > 0:
                dist_str = parts[0]
                # レース種別を判定する
                if '障' in dist_str:
                    race_type = '障害'
                elif 'ダ' in dist_str:
                    race_type = 'ダート'
                elif '芝' in dist_str:
                    race_type = '芝'
                else:
                    race_type = '不明'

                # 距離部分（2000 など）を抽出
                dist_str_numeric = dist_str
                # 不要文字をいろいろ除去
                for keyword in ['芝右', '芝左', 'ダ右', 'ダ左', '芝', 'ダート', '障', '外']:
                    dist_str_numeric = dist_str_numeric.replace(keyword, '')
                dist_str_numeric = dist_str_numeric.split('m')[0]

                try:
                    distance = int(dist_str_numeric)
                except ValueError:
                    distance = None
            
            if len(parts) > 1:
                # "天候 : 晴" → "晴"
                if ':' in parts[1]:
                    weather = parts[1].split(':')[1].strip()

            if len(parts) > 2:
                # "芝 : 良" "ダート : 稍重" 等
                if ':' in parts[2]:
                    track_condition = parts[2].split(':')[1].strip()

        return {
            'race_name': race_name,      # 旧コード: <title> → smalltxt の順で取得
            'race_date': race_date,
            'distance': distance,
            'weather': weather,
            'track_condition': track_condition,
            'race_type': race_type,      # ← 新規追加
        }

    def _parse_race_entries(self) -> list[dict]:
        """
        出走馬情報をテーブルから取得し、
        各リンクURL中のID(馬・騎手・調教師・馬主)も抽出して保存する。
        """
        entries = []
        race_table = self.soup.find('table', class_='race_table_01 nk_tb_common')
        if not race_table:
            return entries

        rows = race_table.find_all('tr')[1:]  # ヘッダを除く
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 21:
                continue

            position_str = cols[0].get_text(strip=True)
            gate_str = cols[1].get_text(strip=True)
            horse_number_str = cols[2].get_text(strip=True)

            # ---------------------------
            # 馬名と馬IDの抽出
            # ---------------------------
            horse_link_tag = cols[3].find('a')
            horse_name = cols[3].get_text(strip=True)  # 従来の馬名
            horse_id = None
            if horse_link_tag and horse_link_tag.has_attr('href'):
                # 例: "/horse/2021101930/"
                href = horse_link_tag['href']
                # 正規表現で数値部分を取得
                # 例えば r"/horse/(\d+)/" にマッチ
                match = re.search(r"/horse/(\d+)/", href)
                if match:
                    horse_id = int(match.group(1))

            sex_age = cols[4].get_text(strip=True)
            weight_carried_str = cols[5].get_text(strip=True)

            # ---------------------------
            # 騎手名と騎手IDの抽出
            # ---------------------------
            jockey_link_tag = cols[6].find('a')
            jockey_name = cols[6].get_text(strip=True)
            jockey_id = None
            if jockey_link_tag and jockey_link_tag.has_attr('href'):
                # 例: "/jockey/result/recent/01169/"
                href = jockey_link_tag['href']
                match = re.search(r"/jockey/result/recent/(\d+)/", href)
                if match:
                    jockey_id = int(match.group(1))

            time_str = cols[7].get_text(strip=True)

            odds_str = cols[12].get_text(strip=True)
            popularity_str = cols[13].get_text(strip=True)
            body_weight_str = cols[14].get_text(strip=True)

            # ---------------------------
            # 調教師名と調教師IDの抽出
            # ---------------------------
            trainer_link_tag = cols[18].find('a')
            trainer_str = cols[18].get_text(strip=True)
            # [東][西]など除去
            trainer_str = trainer_str.replace('[東]', '').replace('[西]', '').strip()
            trainer_id = None
            if trainer_link_tag and trainer_link_tag.has_attr('href'):
                # 例: "/trainer/result/recent/01064/"
                href = trainer_link_tag['href']
                match = re.search(r"/trainer/result/recent/(\d+)/", href)
                if match:
                    trainer_id = int(match.group(1))

            # ---------------------------
            # 馬主名と馬主IDの抽出
            # ---------------------------
            owner_link_tag = cols[19].find('a')
            owner_str = cols[19].get_text(strip=True)
            owner_id = None
            if owner_link_tag and owner_link_tag.has_attr('href'):
                # 例: "/owner/result/recent/783033/"
                href = owner_link_tag['href']
                match = re.search(r"/owner/result/recent/(\d+)/", href)
                if match:
                    owner_id = int(match.group(1))

            prize_str = cols[20].get_text(strip=True)

            # ---------------------------
            # 数値変換
            # ---------------------------
            def try_parse_int(value):
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return None

            def try_parse_float(value):
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return None

            position = try_parse_int(position_str)
            gate = try_parse_int(gate_str)
            horse_number = try_parse_int(horse_number_str)
            weight_carried = try_parse_float(weight_carried_str)
            odds = try_parse_float(odds_str)
            popularity = try_parse_int(popularity_str)
            prize = try_parse_float(prize_str)

            body_weight_diff = None
            if body_weight_str:
                pattern = r'\(([-]?\d+)\)|\(\+?(\d+)\)'
                bw_match = re.search(pattern, body_weight_str)
                if bw_match:
                    number_str = bw_match.group(1) or bw_match.group(2)
                    body_weight_diff = try_parse_int(number_str)

            # ---------------------------
            # entry_data へ詰め込み
            # ---------------------------
            entry_data = {
                'position': position,
                'gate': gate,
                'horse_number': horse_number,
                'horse_name': horse_name,
                'horse_id': horse_id,             # ★追加（馬ID）
                'sex_age': sex_age,
                'weight_carried': weight_carried,
                'jockey_name': jockey_name,
                'jockey_id': jockey_id,           # ★追加（騎手ID）
                'time': time_str,
                'odds': odds,
                'popularity': popularity,
                'body_weight_diff': body_weight_diff,
                'trainer_name': trainer_str,
                'trainer_id': trainer_id,         # ★追加（調教師ID）
                'owner_name': owner_str,
                'owner_id': owner_id,             # ★追加（馬主ID）
                'prize': prize,
            }
            entries.append(entry_data)

        return entries

    def _parse_payouts(self) -> list[dict]:
        """
        払戻情報を抽出
        """
        payouts = []
        payout_block = self.soup.find('dl', class_='pay_block')
        if not payout_block:
            return payouts

        tables = payout_block.find_all('table', class_='pay_table_01')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                th = row.find('th')
                tds = row.find_all('td')
                if not th or len(tds) < 2:
                    continue

                category = th.get_text(strip=True)
                horse_gate_str = tds[0].get_text(strip=True)
                amount_str = tds[1].get_text(strip=True)

                # 整形
                amount_str = amount_str.replace('円', '').replace(',', '')
                amount = try_parse_float(amount_str) or 0.0

                # 人気
                popularity = None
                if len(tds) > 2:
                    pop_str = tds[2].get_text(strip=True)
                    popularity = try_parse_int(pop_str)

                horse_gate = try_parse_int(horse_gate_str) or 0

                payouts.append({
                    'category': category,
                    'horse_gate': horse_gate,
                    'amount': amount,
                    'popularity': popularity,
                })

        return payouts

    def _parse_corner_passages(self) -> list[dict]:
        """
        コーナー通過順位を抽出
        """
        corners = []
        corner_table = self.soup.find('table', summary='コーナー通過順位')
        if not corner_table:
            return corners

        rows = corner_table.find_all('tr')
        for row in rows:
            th = row.find('th')
            td = row.find('td')
            if not th or not td:
                continue
            corner_label = th.get_text(strip=True)
            passage_order_str = td.get_text(strip=True)
            corners.append({
                'corner': corner_label,
                'passage_order': passage_order_str,
            })
        return corners

    def _parse_lap_times(self) -> list[dict]:
        """
        ラップタイムを抽出
        """
        lap_times = []
        lap_time_table = self.soup.find('table', summary='ラップタイム')
        if not lap_time_table:
            return lap_times

        rows = lap_time_table.find_all('tr')
        for row in rows:
            th = row.find('th')
            td = row.find('td')
            if not th or not td:
                continue
            category = th.get_text(strip=True)
            value = td.get_text(strip=True)
            lap_times.append({
                'category': category,
                'lap_text': value,
            })
        return lap_times

# -----------------------------------
# 3) DB保存専用クラス
# -----------------------------------
class RaceDataSaver:
    """
    解析済みデータを受け取り、Djangoモデルへ保存する。
    """
    def __init__(self, race_id: str, parsed_data: dict):
        """
        parsed_data は以下のような構造を想定：
          {
              'race_info': {...},
              'race_entries': [...],  # ここに horse_id, jockey_id, trainer_id, owner_id が含まれる
              'payouts': [...],
              'corners': [...],
              'lap_times': [...]
          }
        """
        self.race_id = race_id
        self.race_info = parsed_data.get('race_info', {})
        self.race_entries = parsed_data.get('race_entries', [])
        self.payouts = parsed_data.get('payouts', [])
        self.corners = parsed_data.get('corners', [])
        self.lap_times = parsed_data.get('lap_times', [])

    def save_all(self):
        """
        全データをまとめて保存する。
        """
        # レースID解析（year, venue, race_numなど）
        parsed_id = parse_race_id(str(self.race_id))

        # 1) Race テーブル
        race = self._save_race(parsed_id)

        # 2) RaceEntry テーブル (馬・騎手・調教師・馬主のID登録を含む)
        self._save_race_entries(race)

        # 3) Payout テーブル
        # self._save_payouts(race)

        # 4) CornerPassageRank テーブル
        # self._save_corner_passages(race)

        # 5) LapTime テーブル
        # self._save_lap_times(race)

        print(f"データの保存が完了しました。")

    def _save_race(self, parsed_id: dict) -> Race:
        race, created = Race.objects.update_or_create(
            race_id=self.race_id,
            defaults={
                'race_name': self.race_info.get('race_name'),
                'date': self.race_info.get('race_date'),
                'distance': self.race_info.get('distance'),
                'weather': self.race_info.get('weather'),
                'track_condition': self.race_info.get('track_condition'),
                'year': parsed_id['year'],
                'course': parsed_id['venue'],
                'race_number': parsed_id['race_num'],
                # race_typeも追加
                'race_type': self.race_info.get('race_type'),
                # 'grade': self.race_info.get('grade'),  # ★追加
            }
        )
        return race

    def _save_race_entries(self, race: Race):
        """
        レースエントリー情報を保存する。
        ここで netkeiba_id を使った update_or_create を行い、IDを一意管理する。
        """

        for entry in self.race_entries:
            # -------------------------
            # 1) Horse の保存
            # -------------------------
            horse_id_val = entry.get('horse_id')
            if horse_id_val:
                horse_obj, _ = Horse.objects.update_or_create(
                    horse_netkeiba_id=horse_id_val,
                    defaults={
                        'name': entry['horse_name'],
                        'sex_age': entry['sex_age']
                    }
                )
            else:
                horse_obj, _ = Horse.objects.update_or_create(
                    name=entry['horse_name'],
                    defaults={'sex_age': entry['sex_age']}
                )

            # -------------------------
            # 2) Jockey の保存
            # -------------------------
            jockey_id_val = entry.get('jockey_id')
            if jockey_id_val:
                jockey_obj, _ = Jockey.objects.update_or_create(
                    jockey_netkeiba_id=jockey_id_val,
                    defaults={'name': entry['jockey_name']}
                )
            else:
                jockey_obj, _ = Jockey.objects.update_or_create(
                    name=entry['jockey_name']
                )

            # -------------------------
            # 3) Trainer の保存
            # -------------------------
            trainer_id_val = entry.get('trainer_id')
            if trainer_id_val:
                trainer_obj, _ = Trainer.objects.update_or_create(
                    trainer_netkeiba_id=trainer_id_val,
                    defaults={'name': entry['trainer_name']}
                )
            else:
                trainer_obj, _ = Trainer.objects.update_or_create(
                    name=entry['trainer_name']
                )

            # -------------------------
            # 4) Owner の保存
            # -------------------------
            owner_id_val = entry.get('owner_id')
            if owner_id_val:
                owner_obj, _ = Owner.objects.update_or_create(
                    owner_netkeiba_id=owner_id_val,
                    defaults={'name': entry['owner_name']}
                )
            else:
                owner_obj, _ = Owner.objects.update_or_create(
                    name=entry['owner_name']
                )

            # -------------------------
            # 5) RaceEntry の保存
            # -------------------------
            gate = entry['gate']
            horse_number = entry['horse_number']

            try:
                RaceEntry.objects.update_or_create(
                    race=race,
                    gate=gate,
                    horse_number=horse_number,
                    horse=horse_obj,
                    jockey=jockey_obj,
                    owner=owner_obj,        # 新たにOwnerを紐付け
                    defaults={
                        'weight_carried': entry['weight_carried'],
                        'odds': entry['odds'],
                        'popularity': entry['popularity'],
                        'body_weight_change': entry['body_weight_diff'],
                        'trainer': trainer_obj,
                        'order_of_finish': entry['position'],
                        # ↓ RaceEntry側にもIDを保存したい場合（オプション）
                        # 'horse_netkeiba_id': horse_id_val,
                        # 'jockey_netkeiba_id': jockey_id_val,
                        # 'trainer_netkeiba_id': trainer_id_val,
                        # 'owner_netkeiba_id': owner_id_val,
                    }
                )
            except Exception as e:
                print(f'RaceEntryモデルへの保存でエラー: {e}')
                # エラー時のフォールバック例（必要なければ省略可）
                try:
                    RaceEntry.objects.create(
                        race=race,
                        horse=horse_obj,
                        jockey=jockey_obj,
                        owner=owner_obj,
                        gate=gate,
                        horse_number=horse_number
                    )
                except Exception as e2:
                    print(f'RaceEntry 作成フォールバックも失敗: {e2}')
                else:
                    RaceEntry.objects.filter(
                        race=race,
                        horse=horse_obj,
                        jockey=jockey_obj,
                        owner=owner_obj,
                        gate=gate,
                        horse_number=horse_number,
                    ).delete()

                    RaceEntry.objects.update_or_create(
                        race=race,
                        gate=gate,
                        horse_number=horse_number,
                        horse=horse_obj,
                        jockey=jockey_obj,
                        owner=owner_obj,
                        defaults={
                            'weight_carried': entry['weight_carried'],
                            'odds': entry['odds'],
                            'popularity': entry['popularity'],
                            'body_weight_change': entry['body_weight_diff'],
                            'trainer': trainer_obj,
                            'order_of_finish': entry['position'],
                            # 'horse_netkeiba_id': horse_id_val,
                            # 'jockey_netkeiba_id': jockey_id_val,
                            # 'trainer_netkeiba_id': trainer_id_val,
                            # 'owner_netkeiba_id': owner_id_val,
                        }
                    )

    def _save_payouts(self, race: Race):
        for p in self.payouts:
            Payout.objects.update_or_create(
                race=race,
                category=p['category'],
                horse_gate=p['horse_gate'],
                defaults={
                    'amount': p['amount'],
                    'popularity': p['popularity'],
                }
            )

    def _save_corner_passages(self, race: Race):
        for c in self.corners:
            corner_label = c['corner']
            CornerPassageRank.objects.update_or_create(
                race=race,
                corner=corner_label,
                defaults={
                    'passage_order': 0  # ここは簡易的に固定値を設定
                }
            )

    def _save_lap_times(self, race: Race):
        """
        ラップタイムの保存。
        例として旧コードと同様の動的割当ロジックを活用する場合は、
        lap_times内にある "lap_text" からスプリットして保存。
        """
        # 例: サンプルの1件を固定保存
        LapTime.objects.update_or_create(
            race=Race.objects.get(race_id=199013131313),
            defaults={
                'category': 'ラップ(サンプル)',
                'm200': float(12.34)
            }
        )

        # 実際のラップタイムを保存
        for lt in self.lap_times:
            try:
                lap_split = [float(x.strip()) for x in lt['lap_text'].split('-')]
            except (ValueError, TypeError):
                LapTime.objects.update_or_create(
                    race=race,
                    category=lt['category']
                )
                continue

            sample_obj = LapTime.objects.first()
            if not sample_obj:
                continue

            laptime_fields = sample_obj._meta.get_fields()
            laptime_fields_names = [field.name for field in laptime_fields]

            lap_update_defaults_dict = {}
            # 「m200」がモデル上4番目にあるなどの仮定に合わせて動的に割り当てる例
            start_index = 4  # "id","item","race","category" を飛ばして4番目が m200 という仮定
            for i, lap_val in enumerate(lap_split):
                field_idx = start_index + i
                if field_idx < len(laptime_fields_names):
                    field_name = laptime_fields_names[field_idx]
                    lap_update_defaults_dict[field_name] = lap_val

            LapTime.objects.update_or_create(
                race=race,
                category=lt['category'],
                defaults=lap_update_defaults_dict
            )


# -----------------------------------
# 4) 全体実行用パイプライン
# -----------------------------------
class RacePipeline:
    """
    1. HTML 取得 (RaceHTMLFetcher)
    2. HTML 解析 (RaceParser)
    3. DB保存 (RaceDataSaver)
    という流れをまとめて実行するパイプライン。
    """
    def __init__(self, race_id: str):
        self.race_id = race_id

    def run(self):
        # 1) RaceHTMLの取得
        fetcher = RaceHTMLFetcher(self.race_id)
        soup = fetcher.get_soup()
        if not soup:
            print("HTMLの取得に失敗したため、処理を中断します。")
            return

        # 2) HTML解析
        parser = RaceParser(soup)
        parsed_data = parser.parse_all()

        # 3) DB保存
        saver = RaceDataSaver(self.race_id, parsed_data)
        saver.save_all()
