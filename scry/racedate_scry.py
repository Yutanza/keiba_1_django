import requests
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup
from scry.datafecher import *

# Django環境下でのインポート（適切なアプリ名に合わせて調整してください）
from App_1.models import Race  # 例: アプリ名が "myapp" の場合

class GetRaceDate:
    """
    指定された年から、その年のレース開催予定と日付を取得してくれるクラスです。
    Raceモデルへのupdate_or_create()も行います。
    run()メソッドを使って実行してください。
    """
    def __init__(self, year, fetcher=None):
        self.year = year
        self.race_info = []
        # DataFetcher のインスタンスを外部から注入できるようにし、
        # ない場合はデフォルトの DataFetcher を使用します
        self.fetcher = fetcher if fetcher else DataFetcher(sleep_time=1.0)

    def get_race_dates_and_ids(self):
        """
        指定した開催年の各月のカレンダーから、開催日とその日のレース一覧ページを取得し、
        レース一覧ページ内から12桁のレースIDを抽出する。

        戻り値はタプル (race_date, race_id) のリストです。
        """
        year = self.year
        race_info = []  # (開催日, レースID) のリスト
        calendar_url_template = "https://race.netkeiba.com/top/calendar.html?year={year}&month={month}"

        # 1月～12月分をループ
        for month in range(1, 13):
            url = calendar_url_template.format(year=year, month=month)
            # DataFetcher で HTML を取得
            calendar_html = self.fetcher.fetch(url)
            if not calendar_html:
                # 取得に失敗した場合は次の月へ
                continue

            soup = BeautifulSoup(calendar_html, "html.parser")

            # カレンダー内のリンクから、開催日のページ（kaisai_date=YYYYMMDD）を探す
            for link in soup.find_all("a", href=True):
                # print(link)
                if "/top/race_list.html?kaisai_date=" in link["href"]:
                    date_match = re.search(r'kaisai_date=(\d{8})', link["href"])
                    if date_match:
                        race_date_str = date_match.group(1)
                        print(f"Found date: {race_date_str}")

                        # レース一覧ページにアクセス
                        race_list_url = f"https://race.netkeiba.com/top/race_list.html?kaisai_date={race_date_str}"
                        race_list_url=f"https://db.netkeiba.com/race/list/{race_date_str}"
                        # https://race.netkeiba.com/top/race_list.html?kaisai_date=20250125
                        race_list_html = self.fetcher.fetch(race_list_url)
                        if not race_list_html:
                            # 取得に失敗した場合は次のリンクへ
                            print('失敗')
                            continue

                        race_list_soup = BeautifulSoup(race_list_html, "html.parser")

                        # レース一覧ページ内から、12桁のrace_id（例: 202401010303）を含むリンクを抽出
                        # for race_link in race_list_soup.find_all("a", href=True):
                        #     if f"/race/{race_date_str}" in race_link["href"]:
                        #         # https://race.netkeiba.com/race/result.html?race_id=202506010303&rf=race_list
                        #         # https://race.netkeiba.com/race/result.html?race_id=202506010801&rf=race_list
                        #         id_match = re.search(r'race_id=(\d{12})', race_link["href"])
                        #         if id_match:
                        #             race_id = id_match.group(1)
                        #             # 文字列の開催日を datetime.date 型に変換
                        #             race_date = datetime.strptime(race_date_str, "%Y%m%d").date()
                        #             race_info.append((race_date, race_id))
                        #             print(f'ありましたよ！{race_id}')
                        for race_link in race_list_soup.find_all("a", href=True):
                            # db.netkeiba.com では /race/202501010101/ のようにURLパラメータではなくパスで表現される
                            id_match = re.search(r'/race/(\d{12})/', race_link["href"])
                            if id_match:
                                race_id = id_match.group(1)
                                # 文字列の開催日(YYYYMMDD)を datetime.date 型に変換
                                race_date = datetime.strptime(race_date_str, "%Y%m%d").date()
                                race_info.append((race_date, race_id))
                                print(f'ありましたよ！{race_id}')
                                # else:
                                #     print("マッチはしてないみたい")
                            # else:
                                # print('no match')
                    else:
                        print("date_match なし")
                # else:
                #     # デバッグ用に不要であれば削除
                #     print("None")
        print("All race info:", race_info)
        self.race_info = race_info

    def update_race_records(self):
        """
        指定した開催年のレース情報をスクレイピングして、
        Raceモデルにupdate_or_createで登録・更新する。
        """
        year = self.year
        race_info_list = self.race_info

        for race_date, race_id in race_info_list:
            # race_idをキーに、開催日(date)と開催年(year)を更新・作成
            obj, created = Race.objects.update_or_create(
                race_id=race_id,
                defaults={
                    "date": race_date,
                    "year": year,
                    # 必要に応じて他のフィールド（race_name, distance など）も追加可能
                }
            )
            if created:
                print(f"Created: RaceID {race_id} on {race_date}")
            else:
                print(f"Updated: RaceID {race_id} on {race_date}")

    def run(self):
        self.get_race_dates_and_ids()
        self.update_race_records()

# if __name__ == "__main__":
#     # 実行例: 2023年のデータを取得
#     target_year = 2023
#     update_race_records(target_year)
