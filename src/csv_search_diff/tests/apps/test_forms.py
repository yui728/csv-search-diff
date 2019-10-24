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
        """read utf-8 csv file"""
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
        self.logger.debug('errors: {}'.format(form.errors))
        self.assertTrue(form.is_valid())
        self.assertEquals(0, len(form.errors))

    # def test_form_03(self) -> None:
    #     """csv1_no_header, csv2_no_header is True"""
    #     with open(self.csvDir.joinpath('csv_without_header.csv')) as f:
    #         data = {
    #             'csv1': f,
    #             'csv1_no_header': True,
    #             'csv2': f,
    #             'csv2_no_header': True
    #         }
    #
    #     form = forms.CsvInputForm(data)
    #
    #     # self.logger.debug('errors: {}'.format(form.errors))
    #     self.assertTrue(form.is_valid())
    #     self.assertEquals(0, len(form.errors))
    #
    # def test_form_02(self) -> None:
    #     """read shift_jis csv file"""
    #     with open(self.csvDir.joinpath('csv_with_header_sjis.csv')) as f:
    #         data = {
    #             'csv1': f,
    #             'csv1_no_header': False,
    #             'csv2': f,
    #             'csv2_no_header': False
    #         }
    #
    #     form = forms.CsvInputForm(data)
    #
    #     # self.logger.debug('errors: {}'.format(form.errors))
    #     self.assertTrue(form.is_valid())
    #     self.assertEquals(0, len(form.errors))
    #
    # def test_form_04(self) -> None:
    #     """csv1 not set is returned Error"""
    #     with open(self.csvDir.joinpath('csv_with_header.csv')) as f:
    #         data = {
    #             'csv1': None,
    #             'csv1_no_header': True,
    #             'csv2': f,
    #             'csv2_no_header': False
    #         }
    #
    #     form = forms.CsvInputForm(data)
    #     # self.logger.debug('errors: {}'.format(form.errors))
    #     self.assertFalse(form.is_valid())
    #     self.assertTrue(len(form.errors) > 0)
    #     self.assertTrue(form.errors['csv1'])

