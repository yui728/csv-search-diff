from django.test.testcases import SimpleTestCase
from apps import utility
import pandas as pd


class CalcColumnCountUtilityTest(SimpleTestCase):
    """Testing Calculation-Column-Count Utility Class"""
    def test_get_max_diff_column_count_01(self) -> None:
        """比較項目の最大設定列数：CSV1の列数がCSV2の列数より多い場合、CSV1の列数-1の値を返す"""
        csv1: pd.DataFrame = pd.DataFrame(columns=['a', 'b', 'c'])
        csv2: pd.DataFrame = pd.DataFrame(columns=['A', 'B'])
        result = utility.CalcColumnCountUtility.get_max_diff_column_count(csv1=csv1, csv2=csv2)
        self.assertEquals(2, result)

    def test_get_max_diff_column_count_02(self) -> None:
        """比較項目の最大設定列数：CSV1の列数がCSV2の列数より少ない場合、CSV2の列数-1の値を返す"""
        csv1: pd.DataFrame = pd.DataFrame(columns=['a', 'b'])
        csv2: pd.DataFrame = pd.DataFrame(columns=['A', 'B', 'C', 'D'])
        result = utility.CalcColumnCountUtility.get_max_diff_column_count(csv1=csv1, csv2=csv2)
        self.assertEquals(3, result)

    def test_get_max_diff_column_count_03(self) -> None:
        """比較項目の最大設定列数：CSV1の列数とCSV2の列数が同じ場合、CSV1の列数-1の値を返す"""
        csv1: pd.DataFrame = pd.DataFrame(columns=['a', 'b'])
        csv2: pd.DataFrame = pd.DataFrame(columns=['A', 'B'])
        result = utility.CalcColumnCountUtility.get_max_diff_column_count(csv1=csv1, csv2=csv2)
        self.assertEquals(1, result)

    def test_get_max_key_column_count_01(self) -> None:
        """
        キー項目の最大設定列数：
        CSV1の列数がCSV2の列数より少なく、比較項目の設定列数が1の場合に
        CSV1の列数 - 1の値を返す
        """
        csv1: pd.DataFrame = pd.DataFrame(columns=range(5))
        csv2: pd.DataFrame = pd.DataFrame(columns=range(6))
        diff_column_count = 1
        result = utility.CalcColumnCountUtility.get_max_key_column_count(
            csv1,
            csv2,
            diff_column_count
        )
        self.assertEquals(4, result)
        pass

    def test_get_max_key_column_count_02(self) -> None:
        """
        キー項目の最大設定列数：
        CSV1の列数がCSV2の列数より多く、比較項目の設定列数が1の場合に
        CSV2の列数 - 1の値を返す
        """
        csv1: pd.DataFrame = pd.DataFrame(columns=range(20))
        csv2: pd.DataFrame = pd.DataFrame(columns=range(10))
        diff_column_count = 1
        result = utility.CalcColumnCountUtility.get_max_key_column_count(
            csv1,
            csv2,
            diff_column_count
        )
        self.assertEquals(9, result)
        pass

    def test_get_max_key_column_count_03(self) -> None:
        """
        キー項目の最大設定列数：
        CSV1の列数がCSV2の列数より少なく、比較項目の設定列数が2の場合に
        CSV1の列数 - 2の値を返す
        """
        csv1: pd.DataFrame = pd.DataFrame(columns=range(100))
        csv2: pd.DataFrame = pd.DataFrame(columns=range(101))
        diff_column_count = 2
        result = utility.CalcColumnCountUtility.get_max_key_column_count(
            csv1,
            csv2,
            diff_column_count
        )
        self.assertEquals(98, result)
        pass

    def test_get_max_key_column_count_04(self) -> None:
        """
        キー項目の最大設定列数：
        CSV1の列数がCSV2の列数より多く、比較項目の設定列数が2の場合に
        CSV2の列数 - 2の値を返す
        """
        csv1: pd.DataFrame = pd.DataFrame(columns=range(1001))
        csv2: pd.DataFrame = pd.DataFrame(columns=range(1000))
        diff_column_count = 2
        result = utility.CalcColumnCountUtility.get_max_key_column_count(
            csv1,
            csv2,
            diff_column_count
        )
        self.assertEquals(998, result)
        pass


class ColumnDetailMessageTestCase(SimpleTestCase):
    def test_create_diff_columns_detail_01(self) -> None:
        """比較項目詳細の生成：列名が半角英数字の場合"""
        csv1_cols = ['col1', 'col2']
        csv2_cols = ['col3', 'col4']
        result = utility.ColumnDetailMessageUtility.create_diff_columns_detail(csv1_cols, csv2_cols)
        self.assertEquals(2, len(result))
        self.assertEquals('CSV1のcol1とCSV2のcol3を比較する', result[0])
        self.assertEquals('CSV1のcol2とCSV2のcol4を比較する', result[1])

    def test_create_diff_columns_detail_02(self) -> None:
        """比較項目詳細の生成：列名が全角文字の場合"""
        csv1_cols = ['列1', '列2', '列3']
        csv2_cols = ['列3', '列4', '列5']
        result = utility.ColumnDetailMessageUtility.create_diff_columns_detail(csv1_cols, csv2_cols)
        self.assertEquals(3, len(result))
        self.assertEquals('CSV1の列1とCSV2の列3を比較する', result[0])
        self.assertEquals('CSV1の列2とCSV2の列4を比較する', result[1])
        self.assertEquals('CSV1の列3とCSV2の列5を比較する', result[2])

    def test_create_key_columns_detail_01(self) -> None:
        """キー項目詳細の生成：列名が半角英数字の場合"""
        csv1_cols = ['col1', 'col2']
        csv2_cols = ['col3', 'col4']
        result = utility.ColumnDetailMessageUtility.create_key_columns_detail(csv1_cols, csv2_cols)
        self.assertEquals(2, len(result))
        self.assertEquals('CSV1のcol1とCSV2のcol3をキーにする', result[0])
        self.assertEquals('CSV1のcol2とCSV2のcol4をキーにする', result[1])

    def test_create_key_columns_detail_02(self) -> None:
        """キー項目詳細の生成：列名が全角文字の場合"""
        csv1_cols = ['列1', '列2', '列3']
        csv2_cols = ['列3', '列4', '列5']
        result = utility.ColumnDetailMessageUtility.create_key_columns_detail(csv1_cols, csv2_cols)
        self.assertEquals(3, len(result))
        self.assertEquals('CSV1の列1とCSV2の列3をキーにする', result[0])
        self.assertEquals('CSV1の列2とCSV2の列4をキーにする', result[1])
        self.assertEquals('CSV1の列3とCSV2の列5をキーにする', result[2])

