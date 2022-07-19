import itertools
from dataclasses import dataclass

from libs.excel.dataclasses.cell import Cell, CellDict
from utils.exceptions import ExcelColumnNotFoundError, TooManyColumnError


@dataclass
class Column:
    """Excelのcolumn(行)。
    """
    title_cell: Cell
    cells: list[Cell]
    column_index: int
    current_row_index: int

    def __init__(self, title: str, column_index: int, start_index_of_row: int) -> None:
        """インスタンスの初期化。title_cellの初期化が必要なので明示的に定義する。

        Parameters
        ----------
        title : str
            title_cellのvalue.
        column_index : int
            行のアドレス。
        start_index_of_row : int
            列方向の開始アドレス。
        """
        self.column_index = column_index
        self.current_row_index = start_index_of_row
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
            value=title, row=self.current_row_index, column=self.column_index
        )
        # インクリメントしておく
        self.current_row_index += 1

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
                row=self.current_row_index,
                column=self.column_index
            )
        )
        # インクリメントしておく
        self.current_row_index += 1

    @property
    def title_cell_member_dict(self) -> CellDict:
        """タイトルを指すセル。
        NOTE: openpyxlのメソッドで直接使用できる形式とする

        Returns
        -------
        CellDict
            データを指すセルの情報を持つ辞書。
        """
        return self.title_cell.member_dict

    @property
    def data_cells(self) -> list[CellDict]:
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
        """タイトルを取得する。

        Returns
        -------
        str
            タイトルを指す文字列。
        """
        return self.title_cell.value  # type: ignore


class ColumnGroup:
    """カラムのグループ。

            |  Group name  |  => グループ名
            | a  | b  | c  |  => columnのタイトル
        ----|--------------|
        1   | a1 | b1 | c1 |  => データ
        2   | a2 | b2 | c2 |

        上のようなデータの時、
        - Group name が self.name_cell.
        - a, b, c が self.columnsのタイトル, a1, b1, c1...がself.columnsのデータ。
        - start_index_of_rowの値が Group name セルの row アドレスになる。
        - start_index_of_row + 1の値が a, b, c セルの row アドレスになる。

        Instance Variables
        ----------
        name_cell: Cell
            グループ名を指すセル。
        columns: list[Column]
            所有するカラム。空の配列で初期化する。
        column_range: tuple[int, int]
            カラムの範囲。
        current_index_of_column: int
            現在のカラムのインデックス。
            NOTE: self.columnsにColumnを追加する度にインクリメントする。
            NOTE: column_rangeの範囲を超えた場合エラーが発生する。
        row_index_of_column_titles: int
            所有するカラムのタイトルの列方向のインデックス。
    """
    def __init__(self, name: str, start_index_of_row: int, column_range: tuple[int, int]) -> None:
        """インスタンスの初期化。

        Parameters
        ----------
        name : str
            グループ名。
        start_index_of_row : int
            列方向の開始インデックス。
        column_range : tuple[int, int]
            行方向の範囲。
            NOTE: 無効なレンジが与えられた時のことは考慮しない
        """
        self.name_cell: Cell = Cell(value=name, row=start_index_of_row, column=column_range)
        self.columns: list[Column] = []
        self.column_range: tuple[int, int] = column_range
        self.current_index_of_column: int = column_range[0]
        # ColumnsのtitleはColumnGroupの開始+1の位置
        self.row_index_of_column_titles: int = start_index_of_row + 1

    def add_column(self, title: str):
        """カラムを追加する。

        Parameters
        ----------
        title : str
            カラムのタイトル。

        Raises
        ------
        TooManyColumnError
            カラムが設定値よりも多くなる場合。
        """
        print(self.column_range)
        if self.current_index_of_column > self.column_range[1]:
            raise TooManyColumnError("columnが設定値よりも多いです")

        self.columns.append(
            Column(
                title=title,
                column_index=self.current_index_of_column,
                start_index_of_row=self.row_index_of_column_titles
            )
        )
        self.current_index_of_column += 1

    def find_column_by(self, title: str | None = None, index: int | None = None) -> Column:
        try:
            if title:
                column = [column for column in self.columns if column.title == title][0]
            elif index is not None:
                column = [column for column in self.columns if column.column_index == index][0]
            else:
                raise ExcelColumnNotFoundError
        except (IndexError, ExcelColumnNotFoundError) as e:
            print(e)
            print("指定されたカラムが存在しません")
            raise ExcelColumnNotFoundError(f"invalid arguments title:{title}, index:{index}")

        return column

    def add_cell_to_column(
        self,
        value: int | float | str | None,
        title: str | None = None,
        column_index: int | None = None
    ):
        """セルを指定したカラムに追加する。

        Parameters
        ----------
        value : int | float | str | None
            セルが持つ値。
        title : str, optional
            対象のカラムタイトル, by default None
        column_index : int, optional
            対象のカラムインデックス, by default None

        Raises
        ------
        ColumnNotFoundError
            カラムが見つからなかった場合。
        """
        column = self.find_column_by(title=title, index=column_index)
        column.add_cell(value)

    @property
    def all_cells(self) -> list[CellDict]:
        """Columns配下に持つ全てのセルを取得する。
        NOTE: 対象はcolumn.title_cell, column.data_cells

        Returns
        -------
        list[CellDict]
            Columns配下に存在する全てのセル。
        """
        name_cell = self.name_cell_member_dict
        column_title_cells = [column.title_cell_member_dict for column in self.columns]
        data_cells_2dim = [column.data_cells for column in self.columns]

        data_cells_2dim.append(column_title_cells)
        data_cells_2dim.append([name_cell])
        # itertoolsを使うことで[[1,2], [2,3], ...]のような配列を1次元に直す事ができる
        return list(itertools.chain.from_iterable(data_cells_2dim))

    @property
    def name_cell_member_dict(self) -> CellDict:
        """グループ名を指すセル。
        NOTE: openpyxlのメソッドで直接使用できる形式とする

        Returns
        -------
        list[CellDict]
            グループ名を指すセルの情報を持つ辞書。
        """
        return self.name_cell.member_dict

    @property
    def name(self) -> str:
        """グループ名。

        Returns
        -------
        str
            グループ名。
        """
        return self.name_cell_member_dict["value"]  # type: ignore
