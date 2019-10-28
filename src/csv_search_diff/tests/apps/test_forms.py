from django.test.testcases import TestCase
from src.csv_search_diff.apps import forms
from . import test_settings
from logging import getLogger
from django.core.files.uploadedfile import SimpleUploadedFile


class CsvDirTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.csvDir = test_settings.CSV_DIR


class CsvInputFormTest(CsvDirTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.logger = getLogger(__name__)

    def test_form_01(self) -> None:
        """UTF-8エンコードのCSVファイルが読み込める"""
        with open(self.csvDir.joinpath('csv_with_header.csv'), 'r') as f:
            file_data = bytes(f.read(), encoding=f.encoding)
            files = {
                'csv1': SimpleUploadedFile(f.name, file_data),
                'csv2': SimpleUploadedFile(f.name, file_data)
            }

        data = {
            'csv1_no_header': False,
            'csv2_no_header': False
        }

        form = forms.CsvInputForm(data, files)
        # self.logger.debug('data = {}'.format(data))
        # self.logger.debug('files = {}'.format(files))
        # self.logger.debug('form = {}'.format(form))
        #
        # self.logger.debug('errors: {}'.format(form.errors))
        self.assertTrue(form.is_valid())
        self.assertEquals(0, len(form.errors))

    def test_form_03(self) -> None:
        """CSV1とCSV2のヘッダーなしチェックボックスをOFFにすることが可能"""
        with open(self.csvDir.joinpath('csv_without_header.csv')) as f:
            file_data = bytes(f.read(), encoding=f.encoding)
            files = {
                'csv1': SimpleUploadedFile(f.name, file_data),
                'csv2': SimpleUploadedFile(f.name, file_data)
            }

        data = {
            'csv1_no_header': True,
            'csv2_no_header': True
        }

        form = forms.CsvInputForm(data, files)

        # self.logger.debug('errors: {}'.format(form.errors))
        self.assertTrue(form.is_valid())
        self.assertEquals(0, len(form.errors))

    def test_form_02(self) -> None:
        """shift_jisエンコードのCSVファイルを読み込むことができる"""
        with open(self.csvDir.joinpath('csv_with_header_sjis.csv'), 'rb') as f:
            file_data = bytes(f.read())
            files = {
                'csv1': SimpleUploadedFile(f.name, file_data),
                'csv2': SimpleUploadedFile(f.name, file_data)
            }

        data = {
            'csv1_no_header': False,
            'csv2_no_header': False
        }

        form = forms.CsvInputForm(data, files)

        # self.logger.debug('errors: {}'.format(form.errors))
        self.assertTrue(form.is_valid())
        self.assertEquals(0, len(form.errors))

    def test_form_04(self) -> None:
        """CSV1が設定されていない場合はエラーになる"""
        with open(self.csvDir.joinpath('csv_with_header.csv')) as f:
            file_data = bytes(f.read(), encoding=f.encoding)
            files = {
                'csv1': None,
                'csv2': SimpleUploadedFile(f.name, file_data)
            }
            data = {
                'csv1_no_header': True,
                'csv2_no_header': False
            }

        form = forms.CsvInputForm(data, files)
        # self.logger.debug('errors: {}'.format(form.errors))
        self.assertFalse(form.is_valid())
        self.assertTrue(1, len(form.errors))
        self.assertTrue(form.errors['csv1'])

    def test_form_05(self) -> None:
        """CSV2が設定されていない場合はエラーになる"""
        with open(self.csvDir.joinpath('csv_with_header.csv')) as f:
            file_data = bytes(f.read(), encoding=f.encoding)
            files = {
                'csv1': SimpleUploadedFile(f.name, file_data),
                'csv2': None
            }
            data = {
                'csv1_no_header': True,
                'csv2_no_header': False
            }

        form = forms.CsvInputForm(data, files)
        # self.logger.debug('errors: {}'.format(form.errors))
        self.assertFalse(form.is_valid())
        self.assertTrue(1, len(form.errors))
        self.assertTrue(form.errors['csv2'])

    def test_form_06(self) -> None:
        """CSV1がCSVとして解釈できない場合はエラーとなる"""
        with open(self.csvDir.joinpath('blank.csv')) as f:
            files = {
                'csv1': SimpleUploadedFile(f.name, bytes(f.read(), encoding=f.encoding))
            }
        with open(self.csvDir.joinpath('csv_with_header.csv')) as f:
            files['csv2'] = SimpleUploadedFile(f.name, bytes(f.read(), encoding=f.encoding))

        data = {
            'csv1_no_header': False,
            'csv2_no_header': True
        }

        # self.logger.debug('files = {}'.format(files))

        form = forms.CsvInputForm(data, files)
        self.assertFalse(form.is_valid())
        # self.logger.debug('errors = {}'.format(form.errors))
        self.assertEquals(1, len(form.errors))
        self.assertTrue(form.errors['csv1'])

    def test_form_07(self) -> None:
        """CSV2がCSVとして解釈できない場合はエラーとなる"""
        with open(self.csvDir.joinpath('blank.csv')) as f:
            files = {
                'csv2': SimpleUploadedFile(f.name, bytes(f.read(), encoding=f.encoding))
            }
        with open(self.csvDir.joinpath('csv_with_header.csv')) as f:
            files['csv1'] = SimpleUploadedFile(f.name, bytes(f.read(), encoding=f.encoding))

        data = {
            'csv1_no_header': False,
            'csv2_no_header': True
        }

        form = forms.CsvInputForm(data, files)
        self.assertFalse(form.is_valid())
        # self.logger.debug('errors = {}'.format(form.errors))
        self.assertEquals(1, len(form.errors))
        self.assertTrue(form.errors['csv2'])

