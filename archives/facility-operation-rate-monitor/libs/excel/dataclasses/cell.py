from typing import TypedDict
from dataclasses import dataclass

from libs.excel.dataclasses.address import IndexCellAddress


class CellDict(TypedDict):
    row: int | tuple[int, int]
    column: int | tuple[int, int]
    value: int | str | float | None


@dataclass
class Cell:
    """セル。

    value: セルの持つ値
    address: セルの場所。今回は数値指定にのみ対応するものとする。
    """
    value: int | str | float | None
    cell_address: IndexCellAddress

    def __init__(
        self,
        value: int | str | float | None,
        row: int | tuple[int, int],
        column: int | tuple[int, int]
    ) -> None:
        self.value = value
        self.cell_address = IndexCellAddress(row=row, column=column)

    @property
    def address(self):
        """セルのアドレスを取得。

        NOTE
        cell_addressはCellAddress抽象基底クラスを継承したクラスのインスタンス。
        そのため、必ずget_addressプロパティを持つ。
        """
        return self.cell_address.get_address

    @property
    def member_dict(self):
        """メンバを辞書として取得。
        NOTE: openpyxlのメソッドで直接使用できる形式とする。

        Returns
        -------
        _type_

        """
        return CellDict(
            row=self.cell_address.row,
            column=self.cell_address.column,
            value=self.value
        )
