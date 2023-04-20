from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Literal, TypeAlias


SheetKey: TypeAlias = int | str
ColumnKey: TypeAlias = int | str
CellValue: TypeAlias = int | float | Decimal | str | bytes | datetime | date | time | timedelta | None

SheetReadingDirection = Literal["row", "column"]
