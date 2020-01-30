import pandas as pd

class CalcColumnCountUtility:
    @classmethod
    def get_max_diff_column_count(cls, csv1: pd.DataFrame, csv2: pd.DataFrame):
        return (len(csv1.columns) - 1) if len(csv1.columns) >= len(csv2.columns) else (len(csv2.columns) - 1)

    @classmethod
    def get_max_key_column_count(cls, csv1: pd.DataFrame, csv2: pd.DataFrame, diff_column_count: int):
        max_column_count = (len(csv1.columns)) if len(csv1.columns) <= len(csv2.columns) else (len(csv2.columns))
        return max_column_count - diff_column_count
