import requests
from bs4 import BeautifulSoup
import csv

# 対象URL（必要に応じて変更）
url = "https://race.netkeiba.com/race/shutuba.html?race_id=202406050811&rf=race_list"

# データ取得
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)
response.encoding = "EUC-JP"
print(response.text)

# soup = BeautifulSoup(response.text, "html.parser")

# # 馬名と騎手名を取得
# horses = [horse.text.strip() for horse in soup.select(".HorseList .HorseName a")]
# jockeys = [jockey.text.strip() for jockey in soup.select(".HorseList .Jockey a")]

# # CSVに保存
# csv_path = "/Users/harukorin/race_data.csv"  # ファイル保存先
# with open(csv_path, "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["馬名", "騎手"])
#     writer.writerows(zip(horses, jockeys))

# print("CSVファイルを作成しました:", csv_path)
