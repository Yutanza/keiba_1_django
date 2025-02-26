# forms.py
from django import forms

class UploadForm(forms.Form):
    target_year = forms.IntegerField(
        label="対象年",
        min_value=1900,
        max_value=2100,
        required=True
    )
    html_update_days_threshold = forms.IntegerField(
        label="何日前までを更新対象とするか",
        min_value=0,
        required=True
    )
