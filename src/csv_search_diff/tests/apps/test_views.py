from django.test import TestCase
from pathlib import Path


class AppsViewTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.inputFileDir = Path(__file__).resolve().parent.parent.joinpath('csv')

    def test_top_get(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, '/pages/index.html')

    def test_top_post(self):
        with open(self.inputFileDir.joinpath('csv_with_header.csv')) as f:
            response = self.client.post('/', {'csv1': f, 'csv2': f})
            self.assertTemplateUsed(response, '/pages/setting-diff-column.html')

    def test_setting_diff_columns_get(self):
        response = self.client.get('/setting_diff_column')
        self.assertRedirects(response, '/')

    def test_setting_diff_columns_post(self):
        response = self.client.post(
            '/setting_diff_column',
            {'csv1_diff_col': ['col3', 'col4'], 'csv2_diff_col': ['col3', 'col4']}
        )
        self.assertTemplateUsed(response, '/pages/setting-key-column.html')

    def test_setting_key_columns_get(self):
        response = self.client.get('/setting_key_column')
        self.assertRedirects(response, '/')

    def test_setting_key_columns_post(self):
        response = self.client.post(
            '/setting_key_column',
            {'csv1_key_col': ['col1', 'col2'], 'csv2_key_col': ['col1', 'col2']}
        )
        self.assertTemplateUsed(response, '/pages/confirm.html')

    def test_confirm_get(self):
        response = self.client.get('/confirm')
        self.assertRedirects(response, '/')

    def test_confirm_post(self):
        response = self.client.post('/confirm')
        self.assertTemplateUsed(response, '/pages/result.html')

    def test_result_get(self):
        response = self.client.get('/result')
        self.assertRedirects(response, '/')

    def test_result_post(self):
        response = self.client.post('/result')
        self.assertEquals(
            response.get('Content-Disposition'),
            "attachment; filename=result.csv"
        )



