"""型を定義するモジュール
"""
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Literal, TypeAlias, TypedDict

# Excel
SheetKey: TypeAlias = int | str
ColumnKey: TypeAlias = int | str
CellValue: TypeAlias = (
    int | float | Decimal | str | bytes | datetime | date | time | timedelta | None
)
SheetReadingDirection = Literal["row", "column"]

class UserSetting(TypedDict):
    """ユーザ設定値の型
    """

    key1: str
    key2: str
    key3: str
    key4: str
