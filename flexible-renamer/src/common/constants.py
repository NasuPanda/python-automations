from dataclasses import dataclass

from src.common import types

# GUI
FONT = "Monospace"


@dataclass
class ComponentKeys:
    input_setting_file = "-INPUT_SETTING-"
    input_folder = "-INPUT_FOLDER-"
    multiline_preview = "-RESULT_PREVIEW-"
    name_part_index_combo = {"before": "-NAME_PART_COMBO_BEFORE-", "after": "-NAME_PART_COMBO_AFTER-"}
    layout_part_index_combo = {"before": "LAYOUT_PART_COMBO_BEFORE-", "after": "LAYOUT_PART_COMBO_AFTER-"}
    save_checkbox = "-SAVE_SETTING_CHECKBOX-"
    save_filename = "-SAVE_SETTING_FILENAME-"
    submit = "-SUBMIT-"


@dataclass(frozen=True)
class RequireSettingExcelAddress:
    names = types.ColumnAddress(sheet_name="必須_データ名", column="A")
    layouts = types.ColumnAddress(sheet_name="必須_撮影箇所", column="A")


@dataclass(frozen=True)
class OptionalSettingExcelAddress:
    path = types.CellAddress(sheet_name="任意", address="B1")
    # 名称
    name_index = types.CellAddress(sheet_name="任意", address="B2")
    # レイアウト
    layout_index = types.CellAddress(sheet_name="任意", address="B3")
    target_extension = types.CellAddress(sheet_name="任意", address="B4")
    delimiter = types.CellAddress(sheet_name="任意", address="B5")


@dataclass
class DefaultSettings:
    name_index = types.PartIndexes(before=2, after=1)
    layout_index = types.PartIndexes(before=1, after=2)
    target_extension = ".png"
    delimiter = "_"
