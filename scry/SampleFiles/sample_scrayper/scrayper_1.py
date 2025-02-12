import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from App_1.models import RaceHTML  # your_app_nameを適切な名前に置き換えてください

def save_race_html_to_file(race_id, file_name="sample_race.html"):
    try:
        race_html = RaceHTML.objects.get(race_id=race_id)
        # 指定した race_id で RaceHTML レコードを取得
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = file_path = os.path.join(base_dir,file_name)

        # ファイル保存先のフルパスを生成
        # file_path = os.path.join(settings.BASE_DIR, file_name)

        # HTML をファイルに書き込む
        with open(file_path, "w", encoding="EUC-JP") as file:
            file.write(race_html.html_text)

        print(f"HTML successfully saved to {file_path}")
        return file_path

    except ObjectDoesNotExist:
        print(f"RaceHTML with race_id {race_id} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# 使用例
# save_race_html_to_file(12345)  # race_id=12345 のデータを保存
