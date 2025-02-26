# new_raceid_search.py

# new_raceid_search.py
import os
import csv
import re
from django.utils import timezone
from datetime import datetime,date,timedelta
from bs4 import BeautifulSoup
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from keiba_1.settings import BASE_DIR

# Django環境下でのインポート（適切なアプリ名に合わせて調整してください）
from App_1.models import Race, RaceHTML
from scry.datafecher import DataFetcher

# ---- ここからURL等の定数設定 ----
RACE_LIST_URL = "https://db.netkeiba.com/race/list/{race_date_str}"
CALENDAR_URL_TEMPLATE = "https://race.netkeiba.com/top/calendar.html?year={year}&month={month}"
RACE_DETAIL_URL = "https://db.netkeiba.com/race/{race_id}"
# CSV保存先ディレクトリ（必要に応じて調整してください）
FILE_PATH=os.path.join(BASE_DIR,'scry','RaceStatics')
# ---- ここまで定数設定 ----


class NewRaceIDSearch:
    """
    「開催されるレースIDの取得、RaceモデルへのレースID/開催日保存、
     レースHTMLをRaceHTMLへ保存、レースID一覧CSVの作成と保存」
    を一括して行うクラス。
    """

    def __init__(self, year,html_update_days_threshold:int, fetcher=None):
        """
        :param year: 対象年 (int)
        :param fetcher: デフォルトの DataFetcher を差し替えたい場合に注入
        """
        self.year = year
        self.fetcher = fetcher if fetcher else DataFetcher(sleep_time=0.1)
        self.race_info = []  # (race_date: date, race_id: str) を格納
        self.html_update_days_threshold=html_update_days_threshold
        # CSVの保存先パスを指定
        self.csv_file_path = os.path.join(FILE_PATH, f"race_ids_{self.year}.csv")
        self.update_race_ids=[]


    def get_race_dates_and_ids(self):
        """
        指定年の1月〜12月を対象に、カレンダー画面から開催日のURLを取得し、
        さらに各開催日のレース一覧ページからレースIDを取得する。
        race_info に (date, race_id) を蓄積する。
        """
        for month in range(1, 13):
            url = CALENDAR_URL_TEMPLATE.format(year=self.year, month=month)
            calendar_html = self.fetcher.fetch(url)
            if not calendar_html:
                continue  # 取得失敗時は次の月へ

            soup = BeautifulSoup(calendar_html, "html.parser")

            # "/top/race_list.html?kaisai_date=YYYYMMDD" を探す
            for link in soup.find_all("a", href=True):
                if "/top/race_list.html?kaisai_date=" in link["href"]:
                    date_match = re.search(r'kaisai_date=(\d{8})', link["href"])
                    if date_match:
                        race_date_str = date_match.group(1)
                        race_list_url = RACE_LIST_URL.format(race_date_str=race_date_str)

                        # レース一覧HTML取得
                        race_list_html = self.fetcher.fetch(race_list_url)
                        if not race_list_html:
                            continue

                        race_list_soup = BeautifulSoup(race_list_html, "html.parser")

                        # レースIDを取得: "/race/(\d{12})/" 形式
                        for race_link in race_list_soup.find_all("a", href=True):
                            id_match = re.search(r'/race/(\d{12})/', race_link["href"])
                            if id_match:
                                race_id = id_match.group(1)
                                # 日付文字列を date 型に変換
                                race_date = datetime.strptime(race_date_str, "%Y%m%d").date()
                                self.race_info.append((race_date, race_id))

    def update_race_records(self):
        """
        取得した (race_date, race_id) を Race モデルに登録または更新する。
        """
        for race_date, race_id in self.race_info:
            if Race.objects.filter(race_id=race_id).exists():
                pass
            else:
                Race.objects.update_or_create(
                    race_id=race_id,
                    defaults={
                        "date": race_date,
                        "year": self.year,
                    }
                )

    def save_race_html_to_db(self):
        """
        race_info のうち、現在の日時から数えて (html_update_days_threshold) 日前以降の
        レースのみ HTML を取得し、RaceHTML モデルへ保存・更新する。
        """
        cutoff_date = timezone.now().date() - timedelta(days=self.html_update_days_threshold)

        with transaction.atomic():
            for (race_date, race_id) in self.race_info:
                # race_date が cutoff_date 以降であれば取得・更新
                if race_date >= cutoff_date:
                    html_content = self.fetcher.fetch(RACE_DETAIL_URL.format(race_id=race_id))
                    if html_content is None:
                        continue  # 失敗した場合はスキップ

                    RaceHTML.objects.update_or_create(
                        race=Race.objects.get(race_id=race_id),
                        defaults={"html_text": html_content}
                    )
                    self.update_race_ids.append(race_id)
                else:
                    # race_date が cutoff_date より前であれば何もしない
                    pass

    def create_csv_of_race_ids(self):
        """
        取得したレースIDのみを羅列した CSV を作成・保存する。
        """
        # race_info から race_id のみを抜き出し（重複を排除）
        unique_race_ids = {race_id for (_, race_id) in self.race_info}

        # CSVファイル書き込み
        os.makedirs(BASE_DIR, exist_ok=True)
        with open(self.csv_file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Race ID"])
            for race_id in sorted(unique_race_ids):
                writer.writerow([race_id])

    def run(self):
        """
        上記一連の処理をまとめて実行するメソッド。
        """
        self.get_race_dates_and_ids()
        self.update_race_records()
        self.save_race_html_to_db()
        self.create_csv_of_race_ids()

        print(f"【完了】レースID・日付を取得し、Raceモデル・RaceHTMLモデルへ保存、"
              f"さらにCSV({self.csv_file_path})を作成しました。")


# メイン実行例 (Django管理外などで単体実行したい場合)
# if __name__ == "__main__":
#     target_year = 2023
#     new_search = NewRaceIDSearch(year=target_year)
#     new_search.run()
