import re
from typing import NamedTuple, TypedDict



"""Data"""
# Format of datetime: YYMMDD-HHMM
DATETIME_FORMAT = "%y%m%d_%H%M"
# Regex of image files
REGEX_IMAGE = '/*\.(jpg|jpeg|png|bmp)'
# Difference between JST and UTC
DIFF_JST_FROM_UTC = 9
# Invalid sheet title
INVALID_TITLE_REGEX = re.compile(r"[/\\*?:\[\]]")
# Graph scale candidates
GRAPH_SCALES: list[int | float] = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]

"""
Power Point
"""
class PptContentKeys(NamedTuple):
    image: str = "image"
    textbox: str = "textbox"
PPT_CONTENT_KEY = PptContentKeys()


"""
Excel
"""
CHANNELS = [
    "CH1",
    "CH2",
    "CH3",
    "CH4",
    "CH5",
    "CH6",
    "CH7",
    "CH8",
    "CH9",
    "CH10",
    "CH11",
    "CH12",
    "CH13",
    "CH14",
    "CH15",
    "CH16",
]


class SettingExcelLocations(TypedDict):
    """Places of column name of CSV in the setting Excel file."""

    CH1: str
    CH2: str
    CH3: str
    CH4: str
    CH5: str
    CH6: str
    CH7: str
    CH8: str
    CH9: str
    CH10: str
    CH11: str
    CH12: str
    CH13: str
    CH14: str
    CH15: str
    CH16: str


SETTING_EXCEL_LOCATIONS = SettingExcelLocations(
    CH1="B1",
    CH2="B2",
    CH3="B3",
    CH4="B4",
    CH5="D1",
    CH6="D2",
    CH7="D3",
    CH8="D4",
    CH9="F1",
    CH10="F2",
    CH11="F3",
    CH12="F4",
    CH13="H1",
    CH14="H2",
    CH15="H3",
    CH16="H4",
)


"""
NOTE: How to decide values

Example: Setting at column size 15, row size 18.
    SizeOfCell.width  = (25/ 3) multiply 15 = Approx. 125
    SizeOfCell.height = (47/36) multiply 18 = Approx. 23.5
"""


class SizeOfCell(NamedTuple):
    width: int | float = (25 / 3) * 15
    height: int | float = (47 / 36) * 18


class NumberOfCell(NamedTuple):
    column: int = 5
    row: int = 14


class SizeOfAttachedImage(NamedTuple):
    size_of_cell: SizeOfCell
    number_of_cell: NumberOfCell

    @property
    def width(self) -> float:
        return self.size_of_cell.width * self.number_of_cell.column

    @property
    def height(self) -> float:
        return self.size_of_cell.height * self.number_of_cell.row


SIZE_OF_ATTACHED_IMAGE = SizeOfAttachedImage(
    size_of_cell=SizeOfCell(), number_of_cell=NumberOfCell()
)
