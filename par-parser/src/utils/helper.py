"""軽い処理を書くモジュール
"""

import pandas as pd

from src.utils.exceptions import CSVException, ColumnNotFoundError


class CSVReader():
    """CSVを読み込むクラス。
    """
    def __init__(self, csv_path: str) -> None:
        """インスタンスの初期化。

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame
        """
        self.df = pd.read_csv(csv_path)

    @property
    def headers(self) -> list[str]:
        return self.df.columns.values.tolist()

    def extract_columns(self, *columns) -> pd.DataFrame:
        """DataFrameから特定のcolumnsを抽出する。

        Parameters
        ----------
        columns : str
            抽出したいカラム。

        Returns
        -------
        pd.DataFrame
            特定のカラムを持つDataFrame。

        Raises
        ------
        ColumnNotFoundError
            columnが見つからなかった時
        """
        try:
            return self.df[columns]
        except CSVException:
            raise ColumnNotFoundError("指定されたcolumnは存在しません。")

    def get_column_values(self, column) -> list[int | float]:
        """カラムの値をリストとして取得する。
        """
        return self.df[column].tolist()
