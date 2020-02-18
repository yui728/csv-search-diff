from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings
from django.urls import reverse
import urllib
import csv
import _csv
import pandas as pd
import logging
from . import forms
from . import utility as util


class TopView(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        context = {
            'form': forms.CsvInputForm()
        }
        return render(request, 'pages/index.html', context)

    def post(self, request, *args, **kwargs):
        data = {
            'csv1_no_header': request.session['csv1_no_header'],
            'csv2_no_header': request.session['csv2_no_header']
        }
        request.session.flush()
        context = {
            'form': forms.CsvInputForm(data)
        }
        return render(request, 'pages/index.html', context)


class SettingDiffColumnView(View):

    __logger = logging.getLogger(__name__)

    def get(self, request, *args, **kwargs):
        # print('SettingDiffColumnView GET')
        if request.session.get('csv1') and request.session.get('csv2'):
            request.session.set_expiry(settings.SESSION_MAX_SECOND)
            csv1 = pd.read_json(request.session['csv1'])
            csv2 = pd.read_json(request.session['csv2'])
            formset = forms.create_setting_diff_column_formset(csv1, csv2)
            back_form = forms.CsvInputForm(request.session)
            context = {
                'formset': formset,
                'back_form': back_form,
                'back_url': reverse('apps:index'),
                'csv1': csv1,
                'csv2': csv2
            }
            return render(request, 'pages/setting-diff-column.html', context)
        else:
            return redirect('/')

    def post(self, request, *args, **kwargs):
        # self.__logger.debug(f"POST: {request.POST}, FILES: {request.FILES}")
        input_form = forms.CsvInputForm(request.POST, request.FILES)
        if input_form.is_valid():
            # self.__logger.debug("SettingDiffColumnView.post form.is_valid()")
            cleaned_data = input_form.clean()
            csv1: pd.DataFrame = self.__csv_to_dataframe(cleaned_data['csv1'], cleaned_data['csv1_no_header'])
            csv2: pd.DataFrame = self.__csv_to_dataframe(cleaned_data['csv2'], cleaned_data['csv2_no_header'])

            request.session['csv1'] = csv1.to_json()
            request.session['csv2'] = csv2.to_json()
            request.session['csv1_no_header'] = input_form.cleaned_data['csv1_no_header']
            request.session['csv2_no_header'] = input_form.cleaned_data['csv2_no_header']
            request.session.set_expiry(settings.SESSION_MAX_SECOND)

            formset = forms.create_setting_diff_column_formset(csv1, csv2)
            context = {
                'formset': formset,
                'back_form': input_form,
                'back_url': reverse('apps:index'),
                'csv1': csv1,
                'csv2': csv2
            }
            return render(request, 'pages/setting-diff-column.html', context)
        else:
            # self.__logger.debug("SettingDiffColumnView.post form.is_valid() is false")
            # self.__logger.debug(f"form-error {form.errors}")
            context = {
                'form': input_form
            }
            return render(request, 'pages/index.html', context)

    def __csv_to_dataframe(self, file_data: UploadedFile, is_no_header: bool) -> pd.DataFrame:
        with file_data.open(mode='rt') as f:
            lines = f.readlines()
            encode = self.__get_upload_csv_encode(lines)
            lines_data = [str(line, encoding=encode) for line in lines]
            reader = csv.reader(lines_data)
            # self.__logger.debug(f"reader = {reader}")
            # self.__logger.debug(f"reader.dialect = {reader.dialect}")
            # self.__logger.debug(f"reader.line_num = {reader.line_num}")
            header = []
            header_format = "列{header}"
            if is_no_header:
                row = next(reader)
                for i in range(len(row)):
                    header.append(header_format.format(header=(i+1)))
                reader = csv.reader(lines_data)
            else:
                header = next(reader)
            # self.__logger.debug(f"header = {header}")
            # self.__logger.debug(f"reader = {reader}")
            # self.__logger.debug(f"reader.line_num = {reader.line_num}")
            result = pd.DataFrame(data=reader, index=None, columns=header)
        self.__logger.debug(f"result = {result}")
        return result

    def __get_upload_csv_encode(self, file_data: list) -> str:
        for encode in settings.CSV_FILE_ENCODE_LIST:
            try:
                lines = [str(line, encoding=encode) for line in file_data]
                # self.__logger.debug(f"{__name__}: lines = {lines}m encode={encode}")
                csv.reader(lines)
            except UnicodeDecodeError as e:
                self.__logger.debug(f"{__name__}: error = {e}")
                continue
            except _csv.Error as e:
                self.__logger.debug(f"{__name__}: error = {e}")
                continue
            return encode


class SettingKeyColumnView(View):
    def get(self, request, *args, **kwargs):
        if self.__session_check(request.session):
            pass
        else:
            return redirect('/')

    def post(self, request, *args, **kwargs):
        csv1: pd.DataFrame = pd.read_json(request.session['csv1'])
        csv2: pd.DataFrame = pd.read_json(request.session['csv2'])
        check_diff_formset = forms.create_setting_diff_column_formset(
            csv1,
            csv2,
            request.POST
        )

        if check_diff_formset.is_valid():
            key_column_setting_formset = forms.create_setting_key_column_formset(
                csv1,
                csv2,
                check_diff_formset.total_form_count()
            )

            csv1_diff_cols = [
                csv1.columns[int(data.get('csv1_diff_col'))] for data in check_diff_formset.cleaned_data
            ]

            csv2_diff_cols = [
                csv2.columns[int(data.get('csv2_diff_col'))] for data in check_diff_formset.cleaned_data
            ]

            diff_column_details = util.ColumnDetailMessageUtility.create_diff_columns_detail(
                csv1_diff_cols,
                csv2_diff_cols
            )

            context = {
                'csv1': csv1,
                'csv2': csv2,
                'formset': key_column_setting_formset,
                'diff_column_list': diff_column_details
            }
            return render(request, 'pages/setting-key-column.html', context)
        else:
            return redirect(reverse('apps:setting_diff_column'))

    def __session_check(self, session):
        return session.get('csv1') \
               and session.get('csv2') \
               and session.get('csv1_diff_col') \
               and session.get('csv2_diff_col')


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

