import os
import sys
import csv
import django
from django.apps import apps
from django.conf import settings
# 必要に応じて設定モジュールを指定 (プロジェクトによる)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keiba_1.settings')
django.setup()

def create_csv_from_db():
    """
    RaceHTMLを除く全モデルのレコードをCSVファイルに出力する。
    出力先はこのファイル(create_csv_from_db.py)と同階層の「csv」ディレクトリ配下に、
    {モデル名}.csv の形式で保存する。
    """
    # 出力先ディレクトリを "csv" として作成
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir = os.path.join(base_dir, 'csv')
    os.makedirs(csv_dir, exist_ok=True)

    # すべてのアプリケーションから、すべてのモデルを取得
    all_models = apps.get_models()

    # 除外するモデル名
    exclude_model_names = ['RaceHTML']

    print("=== 全モデル一覧(除外含む) ===")
    print([model.__name__ for model in all_models])
    print("================================")

    for model in all_models:
        model_name = model.__name__

        # RaceHTML はスキップ
        if model_name in exclude_model_names:
            print(f"Skipping excluded model: {model_name}")
            continue

        print(f"Processing model: {model_name}")

        # CSVファイルのパスを定義
        csv_file_path = os.path.join(csv_dir, f"{model_name}.csv")

        # 多対多・逆リレーション（一対多）を除いたフィールドを取得
        print(model._meta.get_fields())
        fields = [
            field
            for field in model._meta.get_fields()
            if not field.many_to_many and not field.one_to_many and not field.many_to_one
        ]
        print(fields)
        # CSV出力用にフィールド名リストを作成
        # 外部キーの場合は "xx_id" を出力するため、field.get_attname() を使用
        field_names = []
        for field in fields:
            if field.is_relation and not field.one_to_one:
                field_names.append(field.get_attname())  # 例: trainer_id
            else:
                field_names.append(field.name)

        # CSV書き込み開始
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # ヘッダー（列名）を書き込む
            writer.writerow(field_names)

            # 全オブジェクトを取得して書き込む
            for obj in model.objects.all():
                row = []
                for field in fields:
                    try:
                        if field.is_relation:
                            # ForeignKey / OneToOneField の場合は "xxx_id" の数値を取得
                            value = getattr(obj, field.get_attname())
                        else:
                            # 通常フィールドはそのまま取得
                            value = getattr(obj, field.name)
                    except:
                        value=None

                    # None は空文字に
                    if value is None:
                        value = ""

                    row.append(value)
                writer.writerow(row)

        print(f"Saved data for model '{model_name}' to '{csv_file_path}'")

if __name__ == "__main__":
    create_csv_from_db()
