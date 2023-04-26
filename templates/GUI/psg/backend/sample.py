"""動作サンプル
"""

from backend.excel import types
from backend.excel.accessor import ExcelAccessor
from common.constants import UserSettingKeys


def read_setting_from_excel(excel_filepath: str) -> types.UserSetting:
    excel = ExcelAccessor(excel_filepath)
    return types.UserSetting(
        key1=excel.read_cell_value_by_coordinate(UserSettingKeys.key1),
        key2=excel.read_cell_value_by_coordinate(UserSettingKeys.key2),
        key3=excel.read_cell_value_by_coordinate(UserSettingKeys.key3),
        key4=excel.read_cell_value_by_coordinate(UserSettingKeys.key4),
    )
