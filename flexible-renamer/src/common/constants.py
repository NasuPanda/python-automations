from dataclasses import dataclass

from src.common import types

# GUI
FONT = "Monospace"


@dataclass
class ComponentKeys:
    input_setting_file = "-INPUT_SETTING-"
    input_folder = "-INPUT_FOLDER-"
    multiline_preview = "-RESULT_PREVIEW-"
    save_checkbox = "-SAVE_SETTING_CHECKBOX-"
    save_filename = "-SAVE_SETTING_FILENAME-"
    submit = "-SUBMIT-"


@dataclass(frozen=True)
class RequireSettingExcelAddress:
    names = types.ColumnAddress(sheet_name="必須_データ名", column="A")
    layouts = types.ColumnAddress(sheet_name="必須_撮影箇所", column="A")


@dataclass(frozen=True)
class OptionalSettingExcelAddress:
    src_path = types.CellAddress(sheet_name="任意", coordinate="B1")
    target_extension = types.CellAddress(sheet_name="任意", coordinate="B2")
    delimiter = types.CellAddress(sheet_name="任意", coordinate="B3")


@dataclass
class DefaultSettings:
    name_index = types.PartIndexes(before=2, after=1)
    layout_index = types.PartIndexes(before=1, after=2)
    target_extension = ".png"
    delimiter = "_"
