"""型を定義するモジュール
"""
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Literal, TypeAlias

# Excel
SheetKey: TypeAlias = int | str
ColumnKey: TypeAlias = int | str
CellValue: TypeAlias = (
    int | float | Decimal | str | bytes | datetime | date | time | timedelta | None
)
SheetReadingDirection = Literal["row", "column"]


@dataclass
class References:
    min_column: int
    max_column: int
    min_row: int
    max_row: int

    @property
    def members_as_dict(self):
        # openpyxlのメソッドに合わせた形にしておく
        return {
            "min_col": self.min_column,
            "max_col": self.max_column,
            "min_row": self.min_row,
            "max_row": self.max_row,
        }


@dataclass
class Graph:
    title: str
    x_axis_title: str
    x_axis_max_value: float
    primary_y_axis_title: str
    secondary_y_axis_title: str
    primary_data_collection: list[References]
    secondary_data: References
    x_axis: References
    address: str
    width: int | float = 18  # default (15cm)
    height: int | float = 10  # default (7cm)
    legend: None | str = "b"
