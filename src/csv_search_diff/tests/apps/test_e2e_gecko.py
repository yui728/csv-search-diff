from . import testing
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.remote import webelement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


class CsvSettingsStaticLiveServerTestCaseForGecko(testing.CsvSettingsStaticLiverServerTestCase):
    SERVER_RESPONSE_WAIT_SEC = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__logger = logging.getLogger(__name__)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument('-headless')
        cls.selenium = webdriver.Firefox(firefox_options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


class IndexTestCase(CsvSettingsStaticLiveServerTestCaseForGecko):
    def test_access_01(self):
        """トップページの初期表示確認"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEqual('CSVを比較する', self.selenium.title)
        self.assertTrue(self.selenium.find_element_by_css_selector('input[name="csv1"]'))
        self.assertTrue(self.selenium.find_element_by_css_selector('input[name="csv2"]'))
        self.assertTrue(self.selenium.find_element_by_css_selector('input[name="csv1_no_header"]'))
        self.assertTrue(self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]'))
        self.assertTrue(self.selenium.find_element_by_css_selector('input[type="submit"][value="次へ"]'))

    def test_submit_01(self):
        """ヘッダーあり指定でファイルをPOSTする"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        csv_file_path = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_file_input_element.send_keys(str(csv_file_path))
        csv2_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_file_input_element.send_keys(str(csv_file_path))

        self.selenium.find_element_by_css_selector('input[type="submit"][value="次へ"]').click()
        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_to_be('%s%s' % (self.live_server_url, '/setting_diff_column/')))

    def test_submit_02(self):
        """ヘッダーなし指定でファイルをPOSTする"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        csv_file_path = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv1_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_file_input_element.send_keys(str(csv_file_path))
        csv2_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_file_input_element.send_keys(str(csv_file_path))

        # ヘッダーなしにチェックする
        self.selenium.find_element_by_css_selector('input[name="csv1_no_header"]').click()
        self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]').click()

        self.selenium.find_element_by_css_selector('input[type="submit"][value="次へ"]').click()
        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_to_be('%s%s' % (self.live_server_url, '/setting_diff_column/')))

    def test_submit_03(self):
        """CSV1を未設定で「次へ」ボタンを押すとCSV1にフォーカスする"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        csv_file_path = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv2_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_file_input_element.send_keys(str(csv_file_path))

        self.selenium.find_element_by_css_selector('input[type="submit"][value="次へ"]').click()
        active_element = self.selenium.find_element_by_css_selector(':focus')
        self.assertEqual('csv1', active_element.get_attribute('name'))

    def test_submit_04(self):
        """CSV2を未設定で「次へ」ボタンを押すとCSV2にフォーカスする"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        csv_file_path = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_file_input_element.send_keys(str(csv_file_path))

        self.selenium.find_element_by_css_selector('input[type="submit"][value="次へ"]').click()
        active_element = self.selenium.find_element_by_css_selector(':focus')
        self.assertEqual('csv2', active_element.get_attribute('name'))


class SettingDiffColumnTestCaseForGecko(CsvSettingsStaticLiveServerTestCaseForGecko):

    def __assert_csv_table(self, table: WebElement, expects:dict) -> None:
        self.assertTrue(table)
        expect_header = expects['header'] if 'header' in expects.keys() else []
        expect_body = expects['body'] if 'body' in expects.keys() else []

        self.assertTrue(table.find_elements_by_css_selector('th > tr > td'))
        headers = table.find_elements_by_css_selector('th > tr > td')
        self.assertTrue(table.find_elements_by_tag_name('tbody'))
        body = table.find_elements_by_tag_name('tbody')

        if expect_header:
            for (i, header) in enumerate(headers):
                self.assertEqual(expect_header[i], header.text)
        else:
            self.__logger.info(f'{__name__}: header is no check.')

        if expect_body:
            for (i, row) in enumerate(body.find_elements_by_tagname('tr')):
                expect_tr = expect_body[i]
                for (j, td) in enumerate(row.find_eleents_by_tagname('td')):
                    self.assertEqual(expect_tr[j], td.text)

        else:
            logger.info(f'{__name__}: body is no check.')


    def test_access_01(self):
        """トップページからヘッダーありのCSVファイルをポストする"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        csv_file_path = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path))
        self.selenium.find_element_by_css_selector('input[type="submit"][value="次へ"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_to_be('%s%s' % (self.live_server_url, '/setting_diff_column/')))

        csv1_table = self.selenium.find_element_by_css_selector('table:nth-of-type(1)')
        self.assertTrue(csv1_table)
        csv1_table_header = csv1_table.find_elements_by_css_selector('th td')
        self.assertTrue(csv1_table_header)
        expect_headers = ['header1', 'header2', 'header3', 'header4']
        for (i, header_element) in enumerate(csv1_table_header):
            self.assertEqual(expect_headers[i], header_element.text)
        csv1_table_body = csv1_table.find_element_by_tag_name('tbody')
        self.assertTrue(csv1_table_body)
        expect_data = [
            ['AAA', '1000', '1.234', '文字列1'],
            ['BBB', '2000', '2.567', '文字列2'],
            ['CCC', '3000', '3.987', '文字列3'],
            ['DDD', '4000', '4.001', '文字列4']
        ]

        csv2_table = self.selenium.find_element_by_css_selector('table:nth-of-type(2)')