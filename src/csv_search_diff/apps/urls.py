from django.urls import path
from . import views

app_name = 'apps'

urlpatterns = [
    path('', views.top_view, name='index'),
    path('setting_diff_column', views.setting_diff_column_view, name='setting_diff_column'),
    path('setting_key_column', views.setting_key_column_view, name='setting_key_column'),
    path('confirm', views.confirm_view, name='confirm'),
    path('result', views.result_view, name='result'),
    path('download_result_csv', views.result_csv_download_view, name='download_result_csv')
]