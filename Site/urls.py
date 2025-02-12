from django.urls import path
from .views import ListCSVFilesView, DownloadCSVView

urlpatterns = [
    path('download/csv/', ListCSVFilesView.as_view(), name='list_csv_files'),
    path('download/csv/<str:filename>/', DownloadCSVView.as_view(), name='download_csv'),
]
