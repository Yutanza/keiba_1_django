from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

# 対象のアプリケーション名を指定
app = apps.get_app_config('App_1')

for model in app.get_models():
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        # 既に登録済みの場合は無視する
        pass

