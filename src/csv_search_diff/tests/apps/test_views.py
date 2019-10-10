from django.test import TestCase
from pathlib import Path
from django.urls import reverse


class AppsViewTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.inputFileDir = Path(__file__).resolve().parent.parent.joinpath('csv')

    def test_top_get(self):
        """index Page get-access"""
        response = self.client.get(reverse('apps:index'))
        self.assertTemplateUsed(response, 'pages/index.html')

    def test_top_post(self):
        """index Page post-access"""
        response = self.client.post(reverse('apps:index'))
        self.assertRedirects(response, '/')

    def test_setting_diff_columns_get(self):
        """setting diff columns page get-access"""
        response = self.client.get('/setting_diff_column')
        self.assertRedirects(response, '/')

    def test_setting_diff_columns_post(self):
        """setting diff columns page post-access"""
        with open(self.inputFileDir.joinpath('csv_with_header.csv')) as f:
            response = self.client.post(reverse('apps:setting_diff_column'), {'csv1': f, 'csv2': f})
            self.assertTemplateUsed(response, 'pages/setting-diff-column.html')

    def test_setting_key_columns_get(self):
        """setting key columns page get-access"""
        response = self.client.get('/setting_key_column')
        self.assertRedirects(response, '/')

    def test_setting_key_columns_post(self):
        """setting key columns page post-access"""
        response = self.client.post(
            reverse('apps:setting_key_column'),
            {'csv1_diff_col': ['col3', 'col4'], 'csv2_diff_col': ['col3', 'col4']}
        )
        self.assertTemplateUsed(response, 'pages/setting-key-column.html')

    def test_confirm_get(self):
        """search diff confirm page get-access"""
        response = self.client.get('/confirm')
        self.assertRedirects(response, '/')

    def test_confirm_post(self):
        """search diff confirm page post-access"""
        response = self.client.post(
            reverse('apps:confirm'),
            {'csv1_key_col': ['col1', 'col2'], 'csv2_key_col': ['col1', 'col2']}
        )
        self.assertTemplateUsed(response, 'pages/confirm.html')

    def test_result_get(self):
        """search diff result page get-access"""
        response = self.client.get('/result')
        self.assertRedirects(response, '/')

    def test_result_post(self):
        """search diff result page post-access"""
        response = self.client.post(reverse('apps:result'))
        self.assertTemplateUsed(response, 'pages/result.html')

    def test_download_result_get(self):
        """search diff result csv-download get-access"""
        response = self.get('/download_result_csv')
        self.assertRedirects(response, '/')

    def test_download_result_post(self):
        """search diff result csv-download post-access"""
        response = self.client.post(reverse('apps:download_result_csv'))
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=result.csv"
        )



