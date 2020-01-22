from . import testing
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import chromedriver_binary
from selenium.common.exceptions import TimeoutException


class CsvSettingsStaticLiveServerTestCaseForChrome(testing.CsvSettingsStaticLiverServerTestCase):
    screenshot_manager = None
    SERVER_RESPONSE_WAIT_SEC = 10
    MAX_TIMEOUT_RETRY = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument('-headless')
        cls.selenium = webdriver.Chrome(chrome_options=options)
        cls.selenium.implicitly_wait(10)
        cls.screenshot_manager = testing.ScreenShotManager()
        cls.screenshot_manager.clear_screenshot_of_class()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


class IndexTestCase(CsvSettingsStaticLiveServerTestCaseForChrome):
    def test_access_01(self):
        """トップページの初期表示確認"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        self.assertEqual('CSVを比較する', self.selenium.title)
        self.screenshot_manager.save_screenshot(self.selenium)
        self.assertTrue(self.selenium.find_element_by_css_selector('input[name="csv1"]'))
        self.assertTrue(self.selenium.find_element_by_css_selector('input[name="csv2"]'))
        self.assertTrue(self.selenium.find_element_by_css_selector('input[name="csv1_no_header"]'))
        self.assertTrue(self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]'))
        self.assertTrue(self.selenium.find_element_by_css_selector('button[type="submit"]'))
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_submit_01(self):
        """ヘッダーあり指定でファイルをPOSTする"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_file_input_element.send_keys(str(csv_file_path))
        csv2_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_file_input_element.send_keys(str(csv_file_path))
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()
        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_submit_02(self):
        """ヘッダーなし指定でファイルをPOSTする"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv1_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_file_input_element.send_keys(str(csv_file_path))
        csv2_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_file_input_element.send_keys(str(csv_file_path))

        # ヘッダーなしにチェックする
        self.selenium.find_element_by_css_selector('input[name="csv1_no_header"]').click()
        self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]').click()

        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()
        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_submit_03(self):
        """CSV1を未設定で「次へ」ボタンを押すとCSV1にフォーカスする"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv2_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_file_input_element.send_keys(str(csv_file_path))
        self.screenshot_manager.save_screenshot(self.selenium)

        self.selenium.find_element_by_css_selector('button[type="submit"]').click()
        active_element = self.selenium.find_element_by_css_selector(':focus')
        self.assertEqual('csv1', active_element.get_attribute('name'))
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_submit_04(self):
        """CSV2を未設定で「次へ」ボタンを押すとCSV2にフォーカスする"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_file_input_element = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_file_input_element.send_keys(str(csv_file_path))
        self.screenshot_manager.save_screenshot(self.selenium)

        self.selenium.find_element_by_css_selector('button[type="submit"]').click()
        active_element = self.selenium.find_element_by_css_selector(':focus')
        self.assertEqual('csv2', active_element.get_attribute('name'))
        self.screenshot_manager.save_screenshot(self.selenium)


class SettingDiffColumnTestCase(CsvSettingsStaticLiveServerTestCaseForChrome):

    def __assert_csv_table(self, table: WebElement, expects: dict) -> None:
        self.assertTrue(table)
        expect_header = expects['header'] if 'header' in expects.keys() else []
        expect_body = expects['body'] if 'body' in expects.keys() else []

        self.assertTrue(table.find_elements_by_css_selector('thead > tr > th'))
        headers = table.find_elements_by_css_selector('thead > tr > th')
        self.assertTrue(table.find_element_by_tag_name('tbody'))
        body = table.find_element_by_tag_name('tbody')

        if expect_header:
            for (i, header) in enumerate(headers):
                self.assertEqual(expect_header[i], header.text)
        else:
            self.__logger.info(f'{__name__}: header is no check.')

        if expect_body:
            for (i, row) in enumerate(body.find_elements_by_tag_name('tr')):
                expect_tr = expect_body[i]
                for (j, td) in enumerate(row.find_elements_by_tag_name('td')):
                    self.assertEqual(expect_tr[j], td.text)
        else:
            self.__logger.info(f'{__name__}: body is no check.')

    def test_table_view_check_for_csv1_with_header(self):
        """トップページからヘッダーありのCSVファイルをポストしたときにCSV1データのテーブルが表示されることを確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path))
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        tables = self.selenium.find_elements_by_tag_name('table')
        self.assertTrue(tables)
        self.assertTrue(2, len(tables))
        csv1_table = tables[0]
        self.assertTrue(csv1_table)
        csv1_table_header = csv1_table.find_elements_by_css_selector('thead th')
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
        expect = {
            'header': expect_headers,
            'body': expect_data
        }
        self.__assert_csv_table(csv1_table, expect)
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_table_view_check_for_csv2_with_header(self):
        """トップページからヘッダーありのCSVファイルをポストしたときにCSV2データのテーブルが表示されることを確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path))
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        tables = self.selenium.find_elements_by_tag_name('table')
        self.assertTrue(tables)
        self.assertTrue(2, len(tables))
        csv2_table = tables[1]
        self.assertTrue(csv2_table)
        csv2_table_header = csv2_table.find_elements_by_css_selector('thead th')
        self.assertTrue(csv2_table_header)
        expect_headers = ['header1', 'header2', 'header3', 'header4']
        for (i, header_element) in enumerate(csv2_table_header):
            self.assertEqual(expect_headers[i], header_element.text)
        csv2_table_body = csv2_table.find_element_by_tag_name('tbody')
        self.assertTrue(csv2_table_body)
        expect_data = [
            ['AAA', '1000', '1.234', '文字列1'],
            ['BBB', '2000', '2.567', '文字列2'],
            ['CCC', '3000', '3.987', '文字列3'],
            ['DDD', '4000', '4.001', '文字列4']
        ]
        expect = {
            'header': expect_headers,
            'body': expect_data
        }
        self.__assert_csv_table(csv2_table, expect)
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_table_view_check_for_csv1_no_header(self):
        """トップページからヘッダーなしのCSVファイルをポストしたときにCSV1データのテーブルが表示されることを確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_no_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_with_header))
        self.selenium.find_element_by_css_selector('input[name="csv1_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        tables = self.selenium.find_elements_by_tag_name('table')
        self.assertTrue(tables)
        self.assertTrue(2, len(tables))
        csv1_table = tables[0]
        self.assertTrue(csv1_table)
        csv1_table_header = csv1_table.find_elements_by_css_selector('thead th')
        self.assertTrue(csv1_table_header)
        expect_headers = ['列1', '列2', '列3', '列4']
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
        expect = {
            'header': expect_headers,
            'body': expect_data
        }
        self.__assert_csv_table(csv1_table, expect)
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_table_view_check_for_csv2_no_header(self):
        """トップページからヘッダーなしのCSVファイルをポストしたときにCSV2データのテーブルが表示されることを確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_with_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_no_header))
        self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        tables = self.selenium.find_elements_by_tag_name('table')
        self.assertTrue(tables)
        self.assertTrue(2, len(tables))
        csv2_table = tables[1]
        self.assertTrue(csv2_table)
        csv2_table_header = csv2_table.find_elements_by_css_selector('thead th')
        self.assertTrue(csv2_table_header)
        expect_headers = ['列1', '列2', '列3', '列4']
        for (i, header_element) in enumerate(csv2_table_header):
            self.assertEqual(expect_headers[i], header_element.text)
        csv2_table_body = csv2_table.find_element_by_tag_name('tbody')
        self.assertTrue(csv2_table_body)
        expect_data = [
            ['AAA', '1000', '1.234', '文字列1'],
            ['BBB', '2000', '2.567', '文字列2'],
            ['CCC', '3000', '3.987', '文字列3'],
            ['DDD', '4000', '4.001', '文字列4']
        ]
        expect = {
            'header': expect_headers,
            'body': expect_data
        }
        self.__assert_csv_table(csv2_table, expect)
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_csv1_diff_column_select_check_with_header(self):
        """CSV1をヘッダーありでアップロードしたときのCSV1の比較項目選択の表示を確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_with_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_no_header))
        self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        diff_column_rows = self.selenium.find_elements_by_css_selector('div.diff-cols')
        self.assertTrue(diff_column_rows)
        self.assertEqual(1, len(diff_column_rows))

        expect_columns = ['header1', 'header2', 'header3', 'header4']
        diff_column_row = diff_column_rows[0]
        diff_column_selects = diff_column_row.find_elements_by_tag_name('select')
        self.assertTrue(diff_column_selects)
        self.assertEqual(2, len(diff_column_selects))
        csv1_diff_column_select = diff_column_selects[0]
        self.assertTrue(csv1_diff_column_select)
        options = csv1_diff_column_select.find_elements_by_css_selector('options')
        for (i, opt) in enumerate(options):
            self.assertEqual(str(i), opt.get_attribute("value"))
            self.assertEqual(expect_columns[i], opt.text)
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_csv1_diff_column_select_check_no_header(self):
        """CSV1をヘッダーなしでアップロードしたときのCSV1の比較項目選択の表示を確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_no_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_with_header))
        self.selenium.find_element_by_css_selector('input[name="csv1_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        diff_column_rows = self.selenium.find_elements_by_css_selector('div.diff-cols')
        self.assertTrue(diff_column_rows)
        self.assertEqual(1, len(diff_column_rows))

        expect_columns = ['列1', '列2', '列3', '列4']
        diff_column_row = diff_column_rows[0]
        diff_column_selects = diff_column_row.find_elements_by_tag_name('select')
        self.assertTrue(diff_column_selects)
        self.assertEqual(2, len(diff_column_selects))
        csv1_diff_column_select = diff_column_selects[0]
        self.assertTrue(csv1_diff_column_select)
        options = csv1_diff_column_select.find_elements_by_css_selector('options')
        for (i, opt) in enumerate(options):
            self.assertEqual(str(i), opt.get_attribute("value"))
            self.assertEqual(expect_columns[i], opt.text)

        self.screenshot_manager.save_screenshot(self.selenium)

    def test_csv2_diff_column_select_check_with_header(self):
        """CSV2をヘッダーありでアップロードしたときのCSV2の比較項目選択の表示を確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_no_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_with_header))
        self.selenium.find_element_by_css_selector('input[name="csv1_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))

        diff_column_rows = self.selenium.find_elements_by_css_selector('div.diff-cols')
        self.assertTrue(diff_column_rows)
        self.assertEqual(1, len(diff_column_rows))

        expect_columns = ['header1', 'header2', 'header3', 'header4']
        diff_column_row = diff_column_rows[0]
        diff_column_selects = diff_column_row.find_elements_by_tag_name('select')
        self.assertTrue(diff_column_selects)
        self.assertEqual(2, len(diff_column_selects))
        csv2_diff_column_select = diff_column_selects[1]
        self.assertTrue(csv2_diff_column_select)
        options = csv2_diff_column_select.find_elements_by_css_selector('options')
        for (i, opt) in enumerate(options):
            self.assertEqual(str(i), opt.get_attribute("value"))
            self.assertEqual(expect_columns[i], opt.text)
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_csv2_diff_column_select_check_no_header(self):
        """CSV2をヘッダーなしでアップロードしたときのCSV2の比較項目選択の表示を確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_with_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_no_header))
        self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        diff_column_rows = self.selenium.find_elements_by_css_selector('div.diff-cols')
        self.assertTrue(diff_column_rows)
        self.assertEqual(1, len(diff_column_rows))

        expect_columns = ['header1', 'header2', 'header3', 'header4']
        diff_column_row = diff_column_rows[0]
        diff_column_selects = diff_column_row.find_elements_by_tag_name('select')
        self.assertTrue(diff_column_selects)
        self.assertEqual(2, len(diff_column_selects))
        csv2_diff_column_select = diff_column_selects[1]
        self.assertTrue(csv2_diff_column_select)
        options = csv2_diff_column_select.find_elements_by_css_selector('options')
        for (i, opt) in enumerate(options):
            self.assertEqual(str(i), opt.get_attribute("value"))
            self.assertEqual(expect_columns[i], opt.text)
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_diff_column_description(self):
        """比較項目列を両方選択済にしたときに詳細が表示されることを確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_with_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_no_header))
        self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        diff_column_rows = self.selenium.find_elements_by_css_selector('div.diff-cols')
        self.assertTrue(diff_column_rows)
        self.assertEqual(1, len(diff_column_rows))
        diff_column_row = diff_column_rows[0]
        diff_column_selects = diff_column_row.find_elements_by_tag_name('select')
        self.assertTrue(diff_column_selects)
        self.assertEqual(2, len(diff_column_selects))
        csv1_diff_column_select = diff_column_selects[0]
        self.assertTrue(csv1_diff_column_select)
        csv2_diff_column_select = diff_column_selects[1]
        self.assertTrue(csv2_diff_column_select)
        description_area = diff_column_row.find_element_by_tag_name('p')
        self.assertTrue(description_area)

        # 選択肢の設定
        csv1_diff_column_select.find_element_by_css_selector('option:nth-of-type(2)').click()
        csv2_diff_column_select.find_element_by_css_selector('option:nth-of-type(2)').click()
        message = "CSV1のheader2とCSV2の列2を比較する"
        self.assertEqual(message, description_area.text)
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_add_diff_row_button(self):
        """比較項目を追加するボタンをクリックすると比較項目の行が追加されることを確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_with_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_no_header))
        self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        add_diff_column_row_button = self.selenium.find_element_by_id('add_diff_row')
        self.assertTrue(add_diff_column_row_button)
        add_diff_column_row_button.click()
        self.screenshot_manager.save_screenshot(self.selenium)

        diff_cols = self.selenium.find_elements_by_css_selector('div.diff-cols')
        self.assertEqual(2, len(diff_cols))
        second_diff_col = diff_cols[1]
        select_elements = second_diff_col.find_elements_by_tag_name('select')
        self.assertEqual(2, len(select_elements))
        self.assertEqual("", select_elements[0].get_attribute("value"))
        self.assertEqual("", select_elements[1].get_attribute("value"))
        description_element = second_diff_col.find_element_by_tag_name("p")
        self.assertEqual("", description_element.text)

    def test_delete_diff_row_button_for_tow_row(self):
        """比較項目行が2行以上ある時に比較項目を削除するボタンをクリックすると末尾の比較項目の行が削除されることを確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_with_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_no_header))
        self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        add_diff_column_row_button = self.selenium.find_element_by_id('add_diff_row')
        self.assertTrue(add_diff_column_row_button)
        add_diff_column_row_button.click()
        self.screenshot_manager.save_screenshot(self.selenium)
        diff_cols = self.selenium.find_elements_by_css_selector('div.diff-cols')
        self.assertEqual(2, len(diff_cols))

        delete_diff_row_button = self.selenium.find_element_by_id('delete_diff_row')
        self.assertTrue(delete_diff_row_button)
        delete_diff_row_button.click()
        self.screenshot_manager.save_screenshot(self.selenium)

        diff_cols = self.selenium.find_elements_by_css_selector('div.diff-cols')
        self.assertEqual(1, len(diff_cols))
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_delete_diff_row_burron_for_one_row(self):
        """比較項目行が1行の時に比較項目を削除するボタンをクリックすると比較項目の行が削除されないことを確認する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_with_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_no_header))
        self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        diff_cols = self.selenium.find_elements_by_css_selector('div.diff-cols')
        self.assertEqual(1, len(diff_cols))

        delete_diff_row_button = self.selenium.find_element_by_id('delete_diff_row')
        self.assertTrue(delete_diff_row_button)
        delete_diff_row_button.click()
        self.screenshot_manager.save_screenshot(self.selenium)

        diff_cols = self.selenium.find_elements_by_css_selector('div.diff-cols')
        self.assertEqual(1, len(diff_cols))
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_click_back_button(self) -> None:
        """「戻る」ボタンをクリックするとトップ画面に遷移する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_with_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_no_header))
        self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        next_button = self.selenium.find_element_by_css_selector("[name='page_back']")
        self.assertTrue(next_button)
        self.screenshot_manager.save_screenshot(self.selenium)
        next_button.click()
        # self.screenshot_manager.save_screenshot(self.selenium)
        alert = self.selenium.switch_to.alert
        # self.screenshot_manager.save_screenshot(self.selenium)
        # self.assertTrue(alert)
        # self.screenshot_manager.save_screenshot(self.selenium)

        alert.accept()
        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        i = 0
        while i < self.MAX_TIMEOUT_RETRY:
            try:
                self.logger.debug(f"until-back-url loop i = {i}")
                wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/')))
            except TimeoutException:
                i = i + 1
                continue
            else:
                self.logger.debug("until-back-url loop break")
                break

        # self.logger.debug(f"title = {self.selenium.title}")
        # print(f"title = {self.selenium.title}")
        # print(f"title = {self.selenium.find_element_by_tag_name('title').text}")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'title')))
        self.screenshot_manager.save_screenshot(self.selenium)
        self.assertEquals("CSVを比較する", self.selenium.title)
        self.screenshot_manager.save_screenshot(self.selenium)

    def test_click_next_button(self) -> None:
        """「次へ」ボタンをクリックするとキー項目設定画面に遷移する"""
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.screenshot_manager.save_screenshot(self.selenium)
        csv_file_path_no_header = self.csvInputDir.joinpath('csv_without_header.csv').resolve()
        csv_file_path_with_header = self.csvInputDir.joinpath('csv_with_header.csv').resolve()
        csv1_input = self.selenium.find_element_by_css_selector('input[name="csv1"]')
        csv1_input.send_keys(str(csv_file_path_with_header))
        csv2_input = self.selenium.find_element_by_css_selector('input[name="csv2"]')
        csv2_input.send_keys(str(csv_file_path_no_header))
        self.selenium.find_element_by_css_selector('input[name="csv2_no_header"]').click()
        self.screenshot_manager.save_screenshot(self.selenium)
        self.selenium.find_element_by_css_selector('button[type="submit"]').click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_diff_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)

        # 比較項目を設定する
        diff_column_rows = self.selenium.find_elements_by_css_selector('div.diff-cols')
        diff_column_row = diff_column_rows[0]
        diff_column_selects = diff_column_row.find_elements_by_tag_name('select')
        csv1_diff_column_select = diff_column_selects[0]
        csv2_diff_column_select = diff_column_selects[1]
        # 選択肢の設定
        csv1_diff_column_select.find_element_by_css_selector('option:nth-of-type(2)').click()
        csv2_diff_column_select.find_element_by_css_selector('option:nth-of-type(2)').click()

        next_button = self.selenium.find_element_by_id("submit_next")
        self.assertTrue(next_button)
        self.screenshot_manager.save_screenshot(self.selenium)
        next_button.click()

        wait = WebDriverWait(self.selenium, self.SERVER_RESPONSE_WAIT_SEC)
        wait.until(EC.url_changes('%s%s' % (self.live_server_url, '/setting_key_column/')))
        self.screenshot_manager.save_screenshot(self.selenium)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'title')))

        self.assertEquals("CSVを比較する：キー項目の設定", self.selenium.title)
        self.screenshot_manager.save_screenshot(self.selenium)

