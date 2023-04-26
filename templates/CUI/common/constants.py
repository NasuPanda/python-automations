from typing import NamedTuple

DATA_FILE_EXTENSION = ".csv"
SETTING_FILE_EXTENSION = ".xlsx"
# Format of datetime: YYMMDD-HHMM
DATETIME_FORMAT = "%y%m%d_%H%M"
# Time zone diff btw JST and UTC
DIFF_JST_FROM_UTC = 9


"""CLI"""
class CliColors(NamedTuple):
    section:str = "cyan"
    notice:str = "green"
    alert:str = "red"

CLI_COLORS = CliColors()
