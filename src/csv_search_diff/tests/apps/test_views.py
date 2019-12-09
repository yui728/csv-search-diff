from django.test import TestCase
from django.urls import reverse
import urllib
from . import test_settings
import logging
from pprint import pprint


class CsvSettingTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.inputFileDir = test_settings.CSV_DIR


class TopViewTest(CsvSettingTestCase):
    def test_top_get(self):
        """index Page get-access"""
        response = self.client.get(reverse('apps:index'))
        self.assertTemplateUsed(response, 'pages/index.html')
        self.assertContains(response, 'CSVを比較する')

    def test_top_post(self):
        """index Page post-access"""
        response = self.client.post(reverse('apps:index'))
        self.assertRedirects(response, '/')


class SettingDiffColumnViewTest(CsvSettingTestCase):
    def test_setting_diff_columns_get(self):
        """setting diff columns page get-access"""
        response = self.client.get('/setting_diff_column')
        self.assertRedirects(response, '/')

    def test_setting_diff_columns_post(self):
        """setting diff columns page post-access"""
        with open(self.inputFileDir.joinpath('csv_with_header.csv'), mode='rt') as f:
            with open(self.inputFileDir.joinpath('csv_with_header.csv'), mode='rt') as f2:
                response = self.client.post(
                    reverse('apps:setting_diff_column'),
                    {'csv1': f, 'csv2': f2, 'csv1_no_header': False, 'csv2_no_header': False})
                self.assertTemplateUsed(response,
                                        'pages/setting-diff-column.html')

    def test_csv_to_dataframe_01(self):
        """CSVからDataFrameに変換する（ヘッダーあり）"""
        with open(self.inputFileDir.joinpath('csv_with_header.csv'), mode='rt') as f:
            with open(self.inputFileDir.joinpath('csv_with_header.csv'), mode='rt') as f2:
                response = self.client.post(
                    reverse('apps:setting_diff_column'),
                    {'csv1': f,
                        'csv2': f2,
                        'csv1_no_header': False,
                        'csv2_no_header': False})
            self.assertTemplateUsed(response,
                                    'pages/setting-diff-column.html')
            self.assertTrue(self.client.session.get('csv1'))
            self.assertTrue(self.client.session.get('csv2'))
            csv1 = self.client.session.get('csv1')
            self.assertTrue('header1' in csv1)
            self.assertTrue('header2' in csv1)
            self.assertTrue('header3' in csv1)
            self.assertTrue('header4' in csv1)
            csv2 = self.client.session.get('csv2')
            self.assertTrue('header1' in csv2)
            self.assertTrue('header2' in csv2)
            self.assertTrue('header3' in csv2)
            self.assertTrue('header4' in csv2)

    def test_csv_to_dataframe_02(self):
        """CSVからDataFrameに変換する（ヘッダーなし）"""
        logger = logging.getLogger(__name__)
        with open(self.inputFileDir.joinpath('csv_without_header.csv')) as f:
            with open(self.inputFileDir.joinpath('csv_without_header.csv')) as f2:
                response = self.client.post(
                    reverse('apps:setting_diff_column'),
                    {
                        'csv1': f,
                        'csv2': f2,
                        'csv1_no_header': True,
                        'csv2_no_header': True
                    }
                )
        self.assertTemplateUsed(response,
                                'pages/setting-diff-column.html')
        self.assertTrue(self.client.session.get('csv1'))
        self.assertTrue(self.client.session.get('csv2'))
        csv1 = self.client.session.get('csv1')
        self.assertTrue('列1'.encode('unicode_escape') in csv1.encode('utf-8'))
        self.assertTrue('列2'.encode('unicode_escape') in csv1.encode('utf-8'))
        self.assertTrue('列3'.encode('unicode_escape') in csv1.encode('utf-8'))
        self.assertTrue('列4'.encode('unicode_escape') in csv1.encode('utf-8'))
        csv2 = self.client.session.get('csv2')
        self.assertTrue('列1'.encode('unicode_escape') in csv2.encode('utf-8'))
        self.assertTrue('列2'.encode('unicode_escape') in csv2.encode('utf-8'))
        self.assertTrue('列3'.encode('unicode_escape') in csv2.encode('utf-8'))
        self.assertTrue('列4'.encode('unicode_escape') in csv2.encode('utf-8'))


class SettingKeyColumnViewTest(CsvSettingTestCase):
    def test_setting_key_columns_get(self):
        """setting key columns page get-access"""
        response = self.client.get('/setting_key_column')
        self.assertRedirects(response, '/')

    def test_setting_key_columns_post(self):
        """setting key columns page post-access"""
        response = self.client.post(
            reverse('apps:setting_key_column'),
            {'csv1_diff_col': ['col3', 'col4'],
             'csv2_diff_col': ['col3', 'col4']}
        )
        self.assertTemplateUsed(response, 'pages/setting-key-column.html')


class ConfirmViewTest(CsvSettingTestCase):
    def test_confirm_get(self):
        """search diff confirm page get-access"""
        response = self.client.get('/confirm')
        self.assertRedirects(response, '/')

    def test_confirm_post(self):
        """search diff confirm page post-access"""
        response = self.client.post(
            reverse('apps:confirm'),
            {'csv1_key_col': ['col1', 'col2'],
             'csv2_key_col': ['col1', 'col2']}
        )
        self.assertTemplateUsed(response, 'pages/confirm.html')


class ResultViewTest(CsvSettingTestCase):
    def test_result_get(self):
        """search diff result page get-access"""
        response = self.client.get('/result')
        self.assertRedirects(response, '/')

    def test_result_post(self):
        """search diff result page post-access"""
        response = self.client.post(reverse('apps:result'))
        self.assertTemplateUsed(response, 'pages/result.html')


class ResultCsvDownloadViewTest(CsvSettingTestCase):
    def test_download_result_get(self):
        """search diff result csv-download get-access"""
        response = self.client.get('/download_result_csv')
        self.assertRedirects(response, '/')

    def test_download_result_post(self):
        """search diff result csv-download post-access"""
        response = self.client.post(reverse('apps:download_result_csv'))
        filename = urllib.parse.quote(u'result.csv'.encode('utf-8'))
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename*=UTF-8\'\'{}".format(filename)
        )





