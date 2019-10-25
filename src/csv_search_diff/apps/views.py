from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.views import View
import urllib
import csv
import pandas as pd
from django.urls import reverse
import logging
from . import forms


class TopView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': forms.CsvInputForm()
        }
        return render(request, 'pages/index.html', context)

    def post(self, request, *args, **kwargs):
        return redirect('/')


class SettingDiffColumnView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/')

    def post(self, request, *args, **kwargs):
        return render(request, 'pages/setting-diff-column.html')


class SettingKeyColumnView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/')

    def post(self, request, *args, **kwargs):
        return render(request, 'pages/setting-key-column.html')


class ConfirmView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/')

    def post(self, request, *args, **kwargs):
        return render(request, 'pages/confirm.html')


class ResultView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/')

    def post(self, request, *args, **kwargs):
        return render(request, 'pages/result.html')


class ResultCsvDownloadView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('apps:index'))

    def post(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)
        # logger.debug("start download_result_csv post method start")
        csv1 = pd.DataFrame({
            'ヘッダー1': ['1234', '5678', '9012', '3456', ''],
            'ヘッダー2': ['abcde', 'abcdefg', 'abcdefgh', 'ABCD', ''],
            'ヘッダー3': ['AAA', 'BBB', 'CCC', 'DDD', 'EEE'],
            'ヘッダー4': ['XXX', 'YYY', 'ZZZ', 'AAA', ''],
            'ヘッダー5': ['あああ', 'いいい', 'ううう', 'えええ', '']
        })
        csv2 = pd.DataFrame({
            'ヘッダー1': ['1234', '5678', '9012', '', '3345'],
            'ヘッダー2': ['abcde', 'abcdefg', 'abcdefgh', '', 'AABC'],
            'ヘッダー3': ['AAA', 'BBB', 'CCC', 'DDD', 'EEE'],
            'ヘッダー4': ['XXX', 'YYY', 'XYZ', '', 'AAB'],
            'ヘッダー5': ['あああ', 'いいい', 'あいう', '', 'ああい']
        })
        diff_columns = {
            'csv1': ['ヘッダー1', 'ヘッダー2'],
            'csv2': ['ヘッダー1', 'ヘッダー2']
        }
        key_columns = {
            'csv1': ['ヘッダー4', 'ヘッダー5'],
            'csv2': ['ヘッダー4', 'ヘッダー5']
        }
        df_creator = ResultDataFrameCreator(
            csv1,
            csv2,
            diff_columns,
            key_columns)
        # logger.debug("start get_result")
        result = df_creator.get_result()
        # logger.debug("end get_result={}".format(result))
        response = HttpResponse(content_type='text/csv; charset=utf8')
        filename = urllib.parse.quote(u'result.csv'.encode('utf8'))
        response['Content-Disposition']\
            = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
        writer = csv.writer(response)
        writer.writerow(result.columns)
        for row in result.values:
            writer.writerow(row)
        return response


class ResultDataFrameCreator:
    __csv1: pd.DataFrame
    __csv2: pd.DataFrame
    __csv1_diff_columns: list
    __csv2_diff_columns: list
    __csv1_key_columns: list
    __csv2_key_columns: list

    def __init__(
            self,
            csv1: pd.DataFrame,
            csv2: pd.DataFrame,
            diff_columns: dict,
            key_columns: dict):
        self.__csv1 = csv1
        self.__csv2 = csv2
        self.__csv1_diff_columns = diff_columns['csv1']
        self.__csv2_diff_columns = diff_columns['csv2']
        self.__csv1_key_columns = key_columns['csv1']
        self.__csv2_key_columns = key_columns['csv2']

    def get_result(self) -> pd.DataFrame:
        csv1_exists = [
            '○', '○', '○', '○', ''
        ]
        csv2_exists = [
            '○', '○', '○', '', '○'
        ]
        value_match = [
            '○', '○', '', '', ''
        ]

        data = {}
        header_base = '{} {}:{}'
        exist_base = '{}に{}が存在'
        csv1_name = 'CSV1'
        csv2_name = 'CSV2'
        key_header = 'キー項目'
        diff_header = '比較項目'
        for i, col in enumerate(self.__csv1_key_columns):
            col_name = header_base.format(csv1_name, key_header, col)
            data[col_name] = self.__csv1_key_columns[i]
        for i, col in enumerate(self.__csv2_key_columns):
            col_name = header_base.format(csv2_name, key_header, col)
            data[col_name] = self.__csv2_key_columns[i]
        for i, col in enumerate(self.__csv1_diff_columns):
            col_name = header_base.format(csv1_name, diff_header, col)
            data[col_name] = self.__csv1_diff_columns[i]
        for i, col in enumerate(self.__csv2_diff_columns):
            col_name = header_base.format(csv2_name, diff_header, col)
            data[col_name] = self.__csv2_diff_columns[i]
        data[exist_base.format(csv1_name, key_header)] = csv1_exists
        data[exist_base.format(csv2_name, key_header)] = csv2_exists
        data['値の一致'] = value_match

        result = pd.DataFrame(data=data)

        return result


top_view = TopView.as_view()
setting_diff_column_view = SettingDiffColumnView.as_view()
setting_key_column_view = SettingKeyColumnView.as_view()
confirm_view = ConfirmView.as_view()
result_view = ResultView.as_view()
result_csv_download_view = ResultCsvDownloadView.as_view()
