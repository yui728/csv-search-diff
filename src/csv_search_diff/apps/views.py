from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.views import View
import urllib
import csv
import pandas as pd


class TopView(View):
    def get(self, request, *args, **kwargs):
        return render(request, '/pages/index.html')

    def post(self, request, *args, **kwargs):
        return render(request, '/pages/setting-diff-column.html')


class SettingDiffColumnView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/')

    def post(self, request, *args, **kwargs):
        return render(request, '/pages/setting-key-column.html')


class SettingKeyColumnView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/')

    def post(self, request, *args, **kwargs):
        return render(request, '/pages/confirm.html')


class ConfirmView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/')

    def post(self, request, *args, **kwargs):
        return render(request, '/pages/result.html')


class ResultView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/')

    def post(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf8')
        filename = urllib.parse.quote(u'resutlt.csv'.encode('utf8'))
        response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
        writer = csv.writer(response)

    def get_result_dataframe(self) -> pd.DataFrame:
        csv1_key_col = ['ヘッダー4', 'ヘッダー5']
        csv2_key_col = ['ヘッダー4', 'ヘッダー5']
        csv1_diff_col = ['ヘッダー1', 'ヘッダー2']
        csv2_diff_col = ['ヘッダー1', 'ヘッダー2']
        csv1_key_vals = [
            ['1234', '5678', '9012', '3456', ''],
            ['abcde', 'abcdefg', 'abcdefgh', 'ABCD', '']
        ]
        csv2_key_vals = [
            ['1234', '5678', '9012', '', '3345'],
            ['abcde', 'abcdefg', 'abcdefgh', '', 'AABC']
        ]
        csv1_diff_vals = [
            ['XXX', 'YYY', 'ZZZ', 'AAA', ''],
            ['あああ', 'いいい', 'ううう', 'えええ', '']
        ]
        csv2_diff_vals = [
            ['XXX', 'YYY', 'XYZ', '', 'AAB'],
            ['あああ', 'いいい', 'あいう', '', 'ああい']
        ]
        csv1_exists = [
            '○', '○', '○', '○', ''
        ]
        csv2_exists = [
            '○', '○', '○', '', '○'
        ]
        value_match = [
            '○', '○', '', '', ''
        ]

        columns = []
        header_base = '{} {}:{}'
        exist_base = '{}に{}が存在'
        CSV1_NAME = 'CSV1'
        CSV2_NAME = 'CSV2'
        KEY_HEADER = 'キー項目'
        DIFF_HEADER = '比較項目'
        for col in csv1_key_col:
            columns.append(header_base.format(CSV1_NAME, KEY_HEADER, col))
        for col in csv2_key_col:
            columns.append(header_base.format(CSV2_NAME, KEY_HEADER, col))
        for col in csv1_diff_col:
            columns.append(header_base.format(CSV1_NAME, DIFF_HEADER, col))
        for col in csv2_diff_col:
            columns.append(header_base.format(CSV2_NAME, DIFF_HEADER, col))
        columns.append(exist_base.format(CSV1_NAME, KEY_HEADER))
        columns.append(exist_base.format(CSV2_NAME, KEY_HEADER))
        columns.append('値の一致')


        result = pd.DataFrame(
                              )
        return result


top_view = TopView.as_view()
setting_diff_column_view = SettingDiffColumnView.as_view()
setting_key_column_view = SettingKeyColumnView.as_view()
confirm_view = ConfirmView.as_view()
result_view = ResultView.as_view()

