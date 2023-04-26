from dataclasses import dataclass
from typing import Literal, TypeAlias

#
# 型エイリアス
#
ValueType: TypeAlias = int | str


class Cell:
    """疑似Excelセル"""

    def __init__(self, location: str, value: ValueType) -> None:
        self.location = location
        self.value = value


class Sheet:
    """疑似Excelシート"""

    def __init__(self, title: str) -> None:
        self.title = title
        self.cells: list[Cell] = []

    def read_cell(self, index: int) -> ValueType:
        cell = self.cells[index]
        return cell.value


#
# リテラル
#
Direction = Literal["row", "column"]


#
# dataclass
#
@dataclass
class User:
    name: str
    id: int


user = User(name="username", id=1000)
