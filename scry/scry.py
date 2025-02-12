# import requests
# from bs4 import BeautifulSoup
# import re
# import datetime
# import csv
# import os

# # Define URLs or HTML file paths
# date_schedule_file = "開催日程 _ レース情報(JRA) - netkeiba.html"
# race_entry_file = "SampleFiles/Race.html"
# base_dir = os.path.dirname(os.path.abspath(__file__))
# pedigree_file = file_path = os.path.join(base_dir, "SampleFiles", "Race.html")

# # Function to extract race information
# def parse_race_info(file_path):
#     file_path=pedigree_file
#     with open(file_path, "r", encoding="utf-8",errors="ignore") as f:
#         soup = BeautifulSoup(f, "html.parser")

#     race_info = {}

#     # Extract race name and basic details
#     race_name = soup.find("h1", class_="RaceName").text.strip()
#     details = soup.find("div", class_="RaceData01").text.strip()
    
#     # Extract individual elements using regex
#     distance_match = re.search(r"(\d+)m", details)
#     weather_match = re.search(r"天候:(\S+)", details)
#     condition_match = re.search(r"馬場:(\S+)", details)

#     race_info["race_name"] = race_name
#     race_info["distance"] = int(distance_match.group(1)) if distance_match else None
#     race_info["weather"] = weather_match.group(1) if weather_match else None
#     race_info["track_condition"] = condition_match.group(1) if condition_match else None

#     return race_info

# print(parse_race_info(file_path))
# Function to extract race entries
# def parse_race_entries(file_path):
#     with open(file_path, "r", encoding="utf-8") as f:
#         soup = BeautifulSoup(f, "html.parser")

#     entries = []

#     # Extract table rows with horse data
#     rows = soup.select("div.RaceTableArea table tr")
#     for row in rows[1:]:  # Skip header
#         cols = row.find_all("td")
#         if len(cols) < 5:
#             continue

#         entry = {
#             "gate": cols[0].text.strip(),
#             "horse_number": cols[1].text.strip(),
#             "horse_name": cols[3].text.strip(),
#             "jockey": cols[4].text.strip(),
#         }
#         entries.append(entry)

#     return entries

# # Function to extract horse pedigree
# def parse_pedigree(file_path):
#     with open(file_path, "r", encoding="utf-8") as f:
#         soup = BeautifulSoup(f, "html.parser")

#     pedigree = {}

#     pedigree["name"] = soup.find("div", class_="horse_title").h1.text.strip()

#     # Extract sire, dam, and damsire
#     pedigree_table = soup.find("table", class_="blood_table")
#     if pedigree_table:
#         rows = pedigree_table.find_all("tr")
#         pedigree["sire"] = rows[0].find("a").text.strip() if rows[0].find("a") else None
#         pedigree["dam"] = rows[1].find("a").text.strip() if rows[1].find("a") else None
#         pedigree["damsire"] = rows[2].find("a").text.strip() if rows[2].find("a") else None

#     return pedigree

# Save results to CSV
# def save_to_csv(data, filename):
#     keys = data[0].keys()
#     with open(filename, "w", newline="", encoding="utf-8",errors="ignore") as f:
#         writer = csv.DictWriter(f, fieldnames=keys)
#         writer.writeheader()
#         writer.writerows(data)

# # Main script
# if __name__ == "__main__":
#     race_info = parse_race_info(race_entry_file)
#     # race_entries = parse_race_entries(race_entry_file)
#     # horse_pedigree = parse_pedigree(pedigree_file)

#     print("Race Info:", race_info)
#     # print("Race Entries:", race_entries)
#     # print("Horse Pedigree:", horse_pedigree)

#     # Save results
#     save_to_csv(race_info, "race_entries.csv")

import os
from bs4 import BeautifulSoup

base_dir = os.path.dirname(os.path.abspath(__file__))
race_file_path = file_path = os.path.join(base_dir,"SampleFiles", "Race.html")

def parse_race_results(file_path):
    """
    レース結果情報をHTMLファイルから抽出して辞書リストとして返す関数
    """
    with open(file_path, "r", encoding="utf-8",errors="replace") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    race_results = []
    
    # 出馬表のテーブルを取得
    table = soup.find("table", class_="Shutuba_Table")
    if not table:
        raise ValueError("出馬表のテーブルが見つかりません")
    
    rows = table.find_all("tr", class_="HorseList")
    for row in rows:
        columns = row.find_all("td")
        
        # レース結果情報を抽出
        race_result = {
            "item": None,  # 項は自動生成する
            "race_id": None,  # 必要なら別途設定
            "position": None,  # 着順はHTMLから取得不可の場合も
            "gate": None,
            "horse_number": None,
            "horse_name": None,
            "sex_age": None,
            "weight_carried": None,
            "jockey": None,
            "time": None,  # タイムはHTMLに存在しない場合がある
            "difference": None,  # 着差はHTMLに存在しない場合がある
            "popularity": None,
            "odds_win": None,
            "last3f": None,  # 後3FはHTMLに存在しない場合がある
            "corner_passage_order": None,  # コーナー通過順位は別途取得
            "trainer": None,
            "body_weight_change": None,
        }
        
        try:
            # 枠
            race_result["gate"] = int(columns[0].text.strip())
            
            # 馬番
            race_result["horse_number"] = int(columns[1].text.strip())
            
            # 馬名
            horse_name_element = columns[3].find("a")
            if horse_name_element:
                race_result["horse_name"] = horse_name_element.text.strip()
            
            # 性齢
            race_result["sex_age"] = columns[4].text.strip()
            
            # 斤量
            race_result["weight_carried"] = float(columns[5].text.strip())
            
            # 騎手
            jockey_element = columns[6].find("a")
            if jockey_element:
                race_result["jockey"] = jockey_element.text.strip()
            
            # 人気
            popularity_element = columns[10].find("span")
            if popularity_element:
                race_result["popularity"] = int(popularity_element.text.strip())
            
            # オッズ
            odds_element = columns[9].find("span")
            if odds_element:
                race_result["odds_win"] = float(odds_element.text.strip())
            
            # 馬体重(増減)
            weight_text = columns[8].text.strip()
            if weight_text:
                body_weight, _, change = weight_text.partition("(")
                race_result["body_weight_change"] = int(change.replace(")", "")) if change else None
            
            # 調教師
            trainer_element = columns[7].find("a")
            if trainer_element:
                race_result["trainer"] = trainer_element.text.strip()
            
            # 出力リストに追加
            race_results.append(race_result)
        except (ValueError, IndexError):
            # 行データが不完全な場合はスキップ
            continue

    return race_results


if __name__ == "__main__":
    race_results = parse_race_results(race_file_path)
    for result in race_results:
        print(result)
