import pandas as pd

class CalcColumnCountUtility:
    @classmethod
    def get_max_diff_column_count(cls, csv1: pd.DataFrame, csv2: pd.DataFrame):
        return (len(csv1.columns) - 1) if len(csv1.columns) >= len(csv2.columns) else (len(csv2.columns) - 1)

    @classmethod
    def get_max_key_column_count(cls, csv1: pd.DataFrame, csv2: pd.DataFrame, diff_column_count: int):
        max_column_count = (len(csv1.columns)) if len(csv1.columns) <= len(csv2.columns) else (len(csv2.columns))
        return max_column_count - diff_column_count


class ColumnDetailMessageUtility:
    @classmethod
    def create_diff_columns_detail(cls, csv1_cols: list, csv2_cols: list) -> list:
        result = []
        max_loop = len(csv1_cols) if len(csv1_cols) <= len(csv2_cols) else len(csv2_cols)
        for i in range(max_loop):
            result.append('CSV1の{}とCSV2の{}を比較する'.format(csv1_cols[i], csv2_cols[i]))
        return result

    @classmethod
    def create_key_columns_detail(cls, csv1_cols: list, csv2_cols: list) -> list:
        result = []
        max_loop = len(csv1_cols) if len(csv1_cols) <= len(csv2_cols) else len(csv2_cols)
        for i in range(max_loop):
            result.append('CSV1の{}とCSV2の{}をキーにする'.format(csv1_cols[i], csv2_cols[i]))
        return result
