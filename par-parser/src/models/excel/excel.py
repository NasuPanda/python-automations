from dataclasses import dataclass

from src.models.excel.sheet import Sheet


@dataclass
class Excel:
    file_name: str
    sheets: list[Sheet]
