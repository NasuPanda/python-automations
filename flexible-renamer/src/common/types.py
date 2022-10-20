from dataclasses import dataclass
from typing import Literal, TypedDict


@dataclass
class CellAddress:
    sheet_name: str
    address: str


@dataclass
class ColumnAddress:
    sheet_name: str
    column: str | int


@dataclass
class PartIndexes:
    before: int
    after: int

    def get_before(self) -> int:
        return self.before - 1

    def get_after(self) -> int:
        return self.after - 1
