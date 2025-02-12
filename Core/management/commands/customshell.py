# import sys
# import os
# import time
# import threading
# from django.core.management.base import BaseCommand
# from django.conf import settings

# try:
#     import IPython
#     from IPython import embed
# except ImportError:
#     print("IPythonがインストールされていません。`pip install ipython` を実行してください。")
#     sys.exit(1)

# class Command(BaseCommand):
#     help = 'カスタムシェルを起動し、shell.pyの内容を自動的に読み込みます。'

#     def handle(self, *args, **options):
#         shell_file = os.path.join(settings.BASE_DIR, 'shell.py')

#         if not os.path.exists(shell_file):
#             self.stderr.write(self.style.ERROR(f"{shell_file} が存在しません。"))
#             sys.exit(1)

#         # shell.pyの内容を実行する関数
#         def execute_shell_py():
#             with open(shell_file, 'r', encoding='utf-8') as f:
#                 code = f.read()
#             exec(code, globals())

#         # 初回実行
#         execute_shell_py()

#         # shell.pyの変更を監視して再実行するスレッド
#         def watch_file():
#             last_mtime = os.path.getmtime(shell_file)
#             while True:
#                 time.sleep(1)
#                 try:
#                     current_mtime = os.path.getmtime(shell_file)
#                     if current_mtime != last_mtime:
#                         last_mtime = current_mtime
#                         self.stdout.write(self.style.WARNING("shell.pyが更新されました。再実行します。"))
#                         execute_shell_py()
#                 except FileNotFoundError:
#                     self.stderr.write(self.style.ERROR(f"{shell_file} が削除されました。"))
#                     break

#         watcher = threading.Thread(target=watch_file, daemon=True)
#         watcher.start()

#         # IPythonシェルの起動
#         embed()

import os
import time
import importlib.util
from django.core.management.base import BaseCommand, CommandError
from keiba_1.settings import BASE_DIR

class Command(BaseCommand):
    help = '自動的にshell.pyを実行し、ファイル更新を監視します。'

    def handle(self, *args, **options):
        # shell.pyのパスを取得
        shell_path = os.path.join( BASE_DIR,'Core','shell.py')
        
        if not os.path.exists(shell_path):
            raise CommandError(f"{shell_path} が存在しません。")

        self.stdout.write(self.style.SUCCESS(f"{shell_path} の監視を開始します。"))

        last_mtime = None

        try:
            while True:
                current_mtime = os.path.getmtime(shell_path)
                if last_mtime is None or current_mtime > last_mtime:
                    last_mtime = current_mtime
                    self.execute_shell(shell_path)
                time.sleep(1)  # 1秒ごとにチェック
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("監視を停止しました。"))

    def execute_shell(self, shell_path):
        try:
            spec = importlib.util.spec_from_file_location("shell_module", shell_path)
            shell_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(shell_module)
            self.stdout.write(self.style.SUCCESS(f"{shell_path} を実行しました。"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"エラーが発生しました: {e}"))
