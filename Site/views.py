
import os
from django.conf import settings
from keiba_1.settings import BASE_DIR
from django.shortcuts import render
from django.http import FileResponse, Http404
from django.views import View
    
class ListCSVFilesView(View):
    csv_dir=os.path.join(BASE_DIR,'module_csv/csv')
    """
    CSVファイルの一覧を表示するビュー
    """
    def get(self, request):
        # csv_dir = getattr(settings, 'CSV_ROOT', os.path.join(settings.BASE_DIR, 'csv_dir/csv/'))
        try:
            # CSVディレクトリ内のファイルを取得
            files = os.listdir(self.csv_dir) 
            # CSVファイルのみフィルタリング
            csv_files = [f for f in files if f.endswith('.csv')]
        except FileNotFoundError:
            csv_files = []
        
        context = {
            'csv_files': csv_files
        }
        return render(request, 'list_csv_files.html', context)
    
class DownloadCSVView(View):
    csv_dir=os.path.join(BASE_DIR,'module_csv/csv')
    """
    指定されたCSVファイルをダウンロードするビュー
    """
    def get(self, request, filename):
        # csv_dir = getattr(settings, 'CSV_ROOT', os.path.join(settings.BASE_DIR, 'csv_dir/csv'))
        
        # セキュリティ対策: ファイル名にディレクトリトラバーサルが含まれていないか確認
        if '..' in filename or '/' in filename or '\\' in filename:
            raise Http404("Invalid file path")
        
        file_path = os.path.join(self.csv_dir, filename)
        
        if not os.path.exists(file_path):
            raise Http404("File does not exist")
        
        # ファイルをレスポンスとして返す
        response = FileResponse(open(file_path, 'rb'), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


# Create your views here.
