# import os
# import csv
# import requests
# import time
# from bs4 import BeautifulSoup
# import re
# import os

# base_dir = os.path.dirname(os.path.abspath(__file__))
# # race_file_path = file_path = os.path.join(base_dir,"SampleFiles", "Race.html")

# # 定数の設定
# BASE_DIR = "./race_data"  # 保存先ディレクトリ
# CALENDAR_URL = "https://race.netkeiba.com/top/calendar.html?year={year}&month={month}"
# RACEDATE_URL = "https://db.netkeiba.com/race/list/{racedate}/"
# # YEAR = 2023


# class SearchID:
#     def __init__(self,year):
#         self.year=year
#         self.date_id_list = []
#         self.race_id_list = []
#         self.file_path=os.path.join(base_dir, f"race_ids_{self.year}.csv")

#     # レースIDをCSVに保存
#     def save_to_csv(self):
#         with open(self.file_path, mode="w", newline="", encoding="EUC-JP") as file:
#             writer = csv.writer(file)
#             writer.writerow(["Race ID"])
#             for row in self.race_id_list:
#                 writer.writerow([row])

#     # カレンダー情報を取得してレース日IDを抽出
#     def get_race_date_ids(self,year):
#         calendar_url_list = [CALENDAR_URL.format(year=year, month=month) for month in range(1, 13)]
#         # date_id_list = []
#         # race_id_list=[]

#         for calendar_url in calendar_url_list:
#             response = requests.get(calendar_url)
#             time.sleep(1)  # アクセス間隔を確保
#             soup = BeautifulSoup(response.content, "html.parser")
#             links = soup.find_all("a", href=True)
#             for link in links:
#                 match = re.search(r'/race/list/(\d{8})/', link['href'])
#                 if match:
#                     self.date_id_list.append(match.group(1))

#         # return date_id_list

#     # レース日IDからレースIDを抽出
#     def get_race_ids(self,date_id_list):
#         # race_id_list = []

#         for date_id in date_id_list:
#             racedate_url = RACEDATE_URL.format(racedate=date_id)
#             response = requests.get(racedate_url)
#             time.sleep(1)  # アクセス間隔を確保
#             soup = BeautifulSoup(response.content, "html.parser")
#             links = soup.find_all("a", href=True)
#             for link in links:
#                 match = re.search(r'/race/(\d{12})/', link['href'])
#                 if match:
#                     self.race_id_list.append(match.group(1))

#         # return race_id_list

# # メイン処理
#     def main(self):
#         # ディレクトリ作成

#         # レース日IDを取得
#         print("Fetching race date IDs...")
#         self.get_race_ids()
#         # race_date_ids = get_race_date_ids(YEAR)
#         print(f"Found {len(self.date_id_list)} race date IDs.")

#         # レースIDを取得
#         print("Fetching race IDs...")
#         # race_ids = get_race_ids(race_date_ids)
#         self.get_race_ids()
#         print(f"Found {len(self.race_id_list)} race IDs.")

#         # CSVファイルに保存
#         # csv_file_path = os.path.join(BASE_DIR, f"race_ids_{YEAR}.csv")
#         self.save_to_csv()
#         print(f"Race IDs saved to {self.file_path}")


import os
import csv
import requests
import time
from bs4 import BeautifulSoup
import re
import logging
from scry.datafecher import DataFetcher
import csv
from django.db import transaction
from App_1.models import RaceHTML
from django.core.exceptions import ObjectDoesNotExist

# 設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CALENDAR_URL = "https://race.netkeiba.com/top/calendar.html?year={year}&month={month}"
RACEDATE_URL = "https://db.netkeiba.com/race/list/{racedate}/"
RACE_URL="https://db.netkeiba.com/race/{race_id}"

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# class RaceDataFetcher:
#     def __init__(self, sleep_time=1):
#         self.sleep_time = sleep_time

#     def fetch(self, url):
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             time.sleep(self.sleep_time)
#             return response.content
#         except requests.RequestException as e:
#             logging.error(f"Failed to fetch {url}: {e}")
#             return None

class SearchID:
    def __init__(self, year):
        self.year = year
        self.file_path = os.path.join(BASE_DIR, f"race_ids_{self.year}.csv")
        self.html_file_path=""
        self.date_id_list = []
        self.race_id_list = []
        self.fetcher = DataFetcher()

    def save_to_csv(self):
        try:
            os.makedirs(BASE_DIR, exist_ok=True)
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Race ID"])
                for row in self.race_id_list:
                    writer.writerow([row])
            logging.info(f"Race IDs successfully saved to {self.file_path}")
        except Exception as e:
            logging.error(f"Failed to save CSV: {e}")

    def get_race_date_ids(self):
        calendar_url_list = [CALENDAR_URL.format(year=self.year, month=month) for month in range(1, 13)]

        for calendar_url in calendar_url_list:
            content = self.fetcher.fetch(calendar_url)
            if content:
                soup = BeautifulSoup(content, "html.parser")
                links = soup.find_all("a", href=True)
                for link in links:
                    match = re.search(r'kaisai_date=(\d{8})', link['href'])
                    if match:
                        self.date_id_list.append(match.group(1))

    def get_race_ids(self):
        for date_id in self.date_id_list:
            racedate_url = RACEDATE_URL.format(racedate=date_id)
            content = self.fetcher.fetch(racedate_url)
            if content:
                soup = BeautifulSoup(content, "html.parser")
                links = soup.find_all("a", href=True)
                for link in links:
                    match = re.search(r'/race/(\d{12})/', link['href'])
                    if match:
                        self.race_id_list.append(match.group(1))

    def main(self):
        logging.info("Fetching race date IDs...")
        self.get_race_date_ids()
        logging.info(f"Found {len(self.date_id_list)} race date IDs.")

        logging.info("Fetching race IDs...")
        self.get_race_ids()
        logging.info(f"Found {len(self.race_id_list)} race IDs.")

        self.save_to_csv()

  # モデルのインポート（アプリ名を置き換えてください）

    def create_query_set(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # ヘッダー行をスキップ
                # race_ids = [row[0] for _, row in zip(range(15), reader)]#先頭5行のみ抽出
                race_ids = [int(row[0]) for row in reader]
                self.race_id_list=race_ids

            with transaction.atomic():
                for race_id in race_ids:
                    # RaceHTMLエントリを作成、存在しない場合のみ作成
                    content = self.fetcher.fetch(RACE_URL.format(race_id=race_id))
                    # print(content[:1000])
                    RaceHTML.objects.update_or_create(
                        race_id=race_id,
                        defaults={'html_text':content}
                    )
            print("データの作成が完了しました。")
        except Exception as e:
            print(f"エラーが発生しました: {e}")

    def save_html_t_db(self,raceid):
        with  transaction.atomic():
            content=self.fetcher.fetch(RACE_URL.format(race_id=raceid))
            RaceHTML.objects.update_or_create(
                race_id=raceid,
                defaults={'html_text':content}
            )
            print("データの作成が完了しました。")

    def save_race_html_to_file(self,race_id, file_name="sample_race.html"):
        try:
            race_html = RaceHTML.objects.get(race_id=race_id)
            # 指定した race_id で RaceHTML レコードを取得
            # base_dir = os.path.dirname(os.path.abspath(__file__))
            # file_path = file_path = os.path.join(base_dir,file_name)

            # ファイル保存先のフルパスを生成
            self.html_file_path = os.path.join(BASE_DIR,f"sample_{race_id}.html")

            # HTML をファイルに書き込む
            with open(self.html_file_path, "w", encoding='utf-8') as file:
                file.write(race_html.html_text)

            print(f"HTML successfully saved to {self.html_file_path}")
            return self.html_file_path

        except ObjectDoesNotExist:
            print(f"RaceHTML with race_id {race_id} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")


# if __name__ == "__main__":
#     YEAR = 2023  # 例として2023年を指定
#     search = SearchID(YEAR)
#     search.main()
