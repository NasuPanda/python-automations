from dataclasses import dataclass
import itertools

from libs.excel.dataclasses.cell import Cell, CellDict
from utils.exceptions import TooManyRowError, ExcelRowNotFoundError

@dataclass
class Row:
    """Excelのrow(列)。
    """
    title_cell: Cell
    cells: list[Cell]
    row_index: int
    current_column_index: int

    def __init__(self, title: str, row_index: int, start_index_of_column: int) -> None:
        """インスタンスの初期化。title_cellの初期化が必要なので明示的に定義する。

        Parameters
        ----------
        title : str
            title_cellのvalue.
        row_index : int
            列のアドレス。
        start_index_of_column : int
            行方向の開始アドレス。
        """
        self.row_index = row_index
        self.current_column_index = start_index_of_column
        self.cells = []
        self.__init_title_cell(title)

    def __init_title_cell(self, title: str):
        """title_cellを初期化する。

        Parameters
        ----------
        title : str
            title_cellのvalue.
        """
        self.title_cell = Cell(
            value=title, row=self.row_index, column=self.current_column_index
        )
        # インクリメントしておく
        self.current_column_index += 1

    def add_cell(self, value: int | float | str | None):
        """self.cellsにCellインスタンスを追加する。
        NOTE: アドレスは現在の値を参照して割り当てられる。

        Parameters
        ----------
        value : int | float | str | None
            Cellのvalue.
        """
        self.cells.append(
            Cell(
                value=value,
                row=self.row_index,
                column=self.current_column_index
            )
        )
        # インクリメントしておく
        self.current_column_index += 1

    @property
    def get_title_cell(self) -> CellDict:
        """タイトルを指すセル。
        NOTE: openpyxlのメソッドで直接使用できる形式とする

        Returns
        -------
        CellDict
            データを指すセルの情報を持つ辞書。
        """
        return self.title_cell.member_dict

    @property
    def get_data_cells(self) -> list[CellDict]:
        """データを指すセルの配列。
        NOTE: openpyxlのメソッドで直接使用できる形式とする

        Returns
        -------
        list[CellDict]
            データを指すセルの情報を持つ辞書の配列。
        """
        return [cell.member_dict for cell in self.cells]

    @property
    def title(self) -> str:
        return self.title_cell.value  # type: ignore


class RowGroup:
    """Rowのグループ。

                    | a  | b  | c  |
                    |----|---------|
        group   |1  | a1 | b1 | c1 |  => データ
        name    |2  | a2 | b2 | c2 |
    """
    def __init__(self, name: str, start_index_of_column: int, row_range: tuple[int, int]) -> None:
        """インスタンスの初期化。

        Parameters
        ----------
        name : str
            グループ名。
        start_index_of_row : int
            列方向の開始インデックス。
        row_range : tuple[int, int]
            行方向の範囲。
        """
        self.name_cell: Cell = Cell(value=name, row=row_range, column=start_index_of_column)
        self.rows: list[Row] = []
        self.row_range: tuple[int, int] = row_range
        self.current_index_of_row: int = row_range[0]
        # RowsのtitleはRowGroupの開始+1の位置
        self.column_index_of_row_titles: int = start_index_of_column + 1

    def add_row(self, title: str):
        """カラムを追加する。

        Parameters
        ----------
        title : str
            カラムのタイトル。

        Raises
        ------
        TooManyRowError
            カラムが設定値よりも多くなる場合。
        """
        if self.current_index_of_row > self.row_range[1]:
            raise TooManyRowError("rowが設定値よりも多いです")

        self.rows.append(
            Row(
                title=title,
                row_index=self.current_index_of_row,
                start_index_of_column=self.column_index_of_row_titles
            )
        )
        self.current_index_of_row += 1

    def find_row_by(self, title=None, index=None):
        try:
            if title:
                row = [row for row in self.rows if row.title == title][0]
            elif index is not None:
                row = [row for row in self.rows if row.row_index == index][0]
            else:
                raise ExcelRowNotFoundError
        except (IndexError, ExcelRowNotFoundError) as e:
            print(e)
            print("指定されたRowが存在しません")
            raise ExcelRowNotFoundError(f"invalid arguments title:{title}, index:{index}")

        return row

    def add_cell_to_row(
        self,
        value: int | float | str | None,
        title=None, row_index=None
    ):
        """セルを指定したカラムに追加する。

        Parameters
        ----------
        value : int | float | str | None
            セルが持つ値。
        title : str, optional
            対象のカラムタイトル, by default None
        row_index : int, optional
            対象のカラムインデックス, by default None

        Raises
        ------
        ExcelRowNotFoundError
            カラムが見つからなかった場合。
        """
        row = self.find_row_by(title=title, index=row_index)
        row.add_cell(value)

    @property
    def get_cells(self) -> list[CellDict]:
        """Rows配下に持つ全てのセルを取得する。
        NOTE: 対象はcolumn.title_cell, column.data_cells

        Returns
        -------
        list[CellDict]
            Rows配下に存在する全てのセル。
        """
        row_title_cells = [row.get_title_cell for row in self.rows]
        data_cells_2dim = [row.get_data_cells for row in self.rows]

        data_cells_2dim.append(row_title_cells)
        # itertoolsを使うことで[[1,2], [2,3], ...]のような配列を1次元に直す事ができる
        return list(itertools.chain.from_iterable(data_cells_2dim))

    @property
    def get_name_cell(self) -> CellDict:
        """グループ名を指すセル。
        NOTE: openpyxlのメソッドで直接使用できる形式とする

        Returns
        -------
        list[CellDict]
            グループ名を指すセルの情報を持つ辞書。
        """
        return self.name_cell.member_dict
