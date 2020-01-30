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




