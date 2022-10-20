from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Literal, TypeAlias


@dataclass
class CellAddress:
    sheet_name: str
    coordinate: str


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


@dataclass
class Config:
    setting_file_path: str
    # Excelから
    data_names: list[str]
    layouts: list[str]
    # 任意 or 入力
    src_folder_path: str
    # 任意
    target_extension: str
    delimiter: str
    dst_folder: str
    # 設定値を利用
    name_index: PartIndexes
    layout_index: PartIndexes


SheetKey: TypeAlias = int | str
ColumnKey: TypeAlias = int | str
CellValue: TypeAlias = int | float | Decimal | str | bytes | datetime | date | time | timedelta | None

SheetReadingDirection = Literal["row", "column"]
