"""
scry_jusho.py

中山金杯などの重賞日程を掲載したページをスクレイピングし、
Raceモデルに G1, G2, G3 などのグレード、およびレースID等を
update_or_create()で登録・更新します。

使用方法(例)
    python manage.py scry_jusho --year 2014

"""

import re
import datetime
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

# models.py のあるアプリを適宜指定してください
from App_1.models import Race
# ↑ "yourapp" は実際のアプリ名に置き換えてください

# datafecher.py で定義されているクラスをインポート
from datafecher import DataFetcher

# class Command(BaseCommand):
#     help = "スクレイピングで重賞日程(レースID, G1~G3)を取得・更新するコマンド"

# def add_arguments(self, parser):
#     # 例えば「--year 2014」のように開催年を指定して実行できるようにしておく例
#     parser.add_argument('--year', type=int, help='取得したい開催年（例: 2014）', required=True)

import datetime
import re
from bs4 import BeautifulSoup

# 必要に応じて、DataFetcher や Race モデルのインポートを行ってください
# from your_module import DataFetcher, Race

def update_race_schedule(target_year):
    """
    指定された年の重賞日程をnetkeibaから取得し、Raceモデルに登録・更新する関数。
    """
    # netkeibaの "重賞日程" ページURL例: https://race.netkeiba.com/top/schedule.html?year=2014
    base_url = f"https://race.netkeiba.com/top/schedule.html?year={target_year}"

    # DataFetcherを使ってHTMLを取得
    fetcher = DataFetcher()
    html = fetcher.fetch(base_url)
    if not html:
        print("ERROR: HTMLの取得に失敗しました。")
        return

    soup = BeautifulSoup(html, 'html.parser')
    
    # 「年 重賞競走」の見出しチェック（見つからなくても処理を続行）
    heading = soup.find('h3', text=re.compile(rf'{target_year}年\s+重賞競走'))
    if not heading:
        print(f"WARNING: {target_year}年の見出しが見つかりませんでした。")
    
    # テーブル内の <tr> タグを取得
    schedule_rows = soup.find_all('tr', class_=re.compile(r'schedule_list[34]'))
    count_updated = 0

    for row in schedule_rows:
        cells = row.find_all('td')
        if len(cells) < 3:
            continue
        
        # 1列目: "01/05(日)" のような日付テキスト
        date_text = cells[0].get_text(strip=True)
        md_match = re.match(r'(\d{2})/(\d{2})', date_text)
        if not md_match:
            continue
        month = int(md_match.group(1))
        day = int(md_match.group(2))
        race_date = datetime.date(target_year, month, day)

        # 2列目: レース名とリンク
        race_name_td = cells[1]
        link = race_name_td.find('a')
        if link:
            race_name = link.get_text(strip=True)
            href = link.get('href', '')
            # URLから12桁のレースIDを抽出
            match = re.search(r'/race/(\d{12})/', href)
            if not match:
                continue
            race_id_str = match.group(1)
        else:
            # リンクがない場合はスキップ
            continue

        # 3列目: グレード（例: G1, G2, G3 など）
        grade = cells[2].get_text(strip=True)

        # DBに update_or_create で登録・更新
        obj, created = Race.objects.update_or_create(
            race_id=race_id_str,
            defaults={
                'race_name': race_name,
                'date': race_date,
                'year': target_year,
                'grade': grade,
            }
        )
        count_updated += 1

    print(f"SUCCESS: 重賞日程を更新しました: 登録/更新件数={count_updated}")
