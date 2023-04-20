import pandas as pd


class CSVReader:
    """
    References
        - [pandasでUnicodeDecodeError が出たときにやることまとめ - 私の備忘録がないわね...私の...](https://kamakuraviel.hatenablog.com/entry/2020/05/27/201155)
        - [Python Pandas 特定の文字列を指定してこれを欠損値として扱いたい。](https://teratail.com/questions/216283)
        - [pandas.DataFrameの行・列を指定して削除するdrop | note.nkmk.me](https://note.nkmk.me/python-pandas-drop/)
    """

    def __init__(
        self,
        filepath: str,
        header_index: int = 0,
        na_values: list[str] | None = None,
        excluded_columns: list[str] | None = None,
        encoding: str | None = None,
    ) -> None:
        """インスタンスの初期化。

        Args:
            filepath (str): csvファイルのパス。
        """
        usecols = lambda x: x not in excluded_columns if excluded_columns else None

        self.df: pd.DataFrame = pd.read_csv(
            filepath,
            header=header_index,
            na_values=na_values,  # type: ignore
            usecols=usecols,  # type: ignore
            encoding=encoding,
        )
        self.columns = self.df.columns.values.tolist()

    @classmethod
    def find_row_by_flag(cls, filepath: str, flag: str, encoding: str | None = None) -> int | None:
        """対象の文字列が存在する列を探す。

        Args:
            filepath (str): csvファイルパス。
            flag (str): 対象の文字列。

        Returns:
            int | None: 対象の文字列が存在する列(0スタート)。存在しなければNoneを返す
        """
        with open(filepath, encoding=encoding) as f:
            for row_index, line in enumerate(f):
                if flag in line:
                    return row_index

    def exists_column(self, column_name: str) -> bool:
        """カラムが存在するかどうか。

        Args:
            column_name (str): 対象のカラム。

        Returns:
            bool: カラムが存在するかどうかを表す真偽値。
        """
        return column_name in self.columns

    def get_column_values(self, column: str, includes_header: bool = False) -> list[int | float] | None:
        """特定のカラムが持つ値をリストとして取得する。

        Args:
            column (str): 対象のカラム。
            includes_header (bool, optional): 返り値のリストにカラム名を含むかどうか。デフォルトは `False` 。

        Returns:
            list[int | float] | None: 特定のカラムが持つ値のリスト。
        """
        if not self.exists_column(column):
            return

        column_values = self.df[column].tolist()
        if includes_header:
            # 返り値の先頭にヘッダを付与する
            column_values.insert(0, column)
        return column_values

    def rename_column(self, before: str, after: str) -> None:
        """カラムの名前を変更する。(破壊的)

        Args:
            before (str):変更前の名称。
            after (str): 変更後の名称。
        """
        self.df.rename(columns={before: after}, inplace=True)

    def drop_column(self, labels: str | list[str]) -> None:
        self.df.drop(labels=labels, axis=1, inplace=True)

    def drop_row_by_index(self, index: int | list[int]) -> None:
        self.df.drop(labels=index, axis=0, inplace=True)
