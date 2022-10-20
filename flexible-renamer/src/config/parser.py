from src.common import exceptions, types
from src.common.constants import (DefaultSettings, OptionalSettingExcelAddress,
                                  RequireSettingExcelAddress)
from src.models.excel import ExcelAccessor


class ConfigParser:
    def __init__(self, filepath: str) -> None:
        self.reader = ExcelAccessor(filepath)

    def parse_config(
        self,
    ) -> types.Config:
        return types.Config(
            setting_file_path=self.reader.filepath,
            data_names=self.data_names(),
            layouts=self.layouts(),
            # NOTE ここで受け取れた場合はGUIの更新に使う
            src_folder_path=self.src_folder(),
            name_index=self.name_index(),
            layout_index=self.layout_index(),
            target_extension=self.target_extension(),
            delimiter=self.delimiter(),
            dst_folder=self.dst_folder(),
        )

    @classmethod
    def validate_number(cls, number: str | int) -> bool:
        try:
            int(number)
        except TypeError:
            return False
        return True

    def data_names(self) -> list[str]:
        self.reader.change_active_worksheet(RequireSettingExcelAddress.names.sheet_name)
        if data_names := self.reader.read_column_values(
            column=RequireSettingExcelAddress.names.column, begin_row=1, end_row=self.reader.max_row
        ):
            return data_names  # type: ignore
        else:
            raise exceptions.ConfigParseError("必須設定が入力されていない or 不正な値が入力されています")

    def layouts(self) -> list[str]:
        self.reader.change_active_worksheet(RequireSettingExcelAddress.layouts.sheet_name)
        if layouts := self.reader.read_column_values(
            column=RequireSettingExcelAddress.layouts.column, begin_row=1, end_row=self.reader.max_row
        ):
            return layouts  # type: ignore
        else:
            raise exceptions.ConfigParseError("必須設定が入力されていない or 不正な値が入力されています")

    def src_folder(self) -> str:
        self.reader.change_active_worksheet(OptionalSettingExcelAddress.src_path.sheet_name)
        if src_folder := self.reader.read_cell_value_by_coordinate(OptionalSettingExcelAddress.src_path.coordinate):
            return src_folder  # type: ignore
        return ""

    def name_index(self) -> types.PartIndexes:
        return DefaultSettings.name_index

    def layout_index(self) -> types.PartIndexes:
        return DefaultSettings.layout_index

    def target_extension(self) -> str:
        self.reader.change_active_worksheet(OptionalSettingExcelAddress.target_extension.sheet_name)
        if target_extension := self.reader.read_cell_value_by_coordinate(
            OptionalSettingExcelAddress.target_extension.coordinate
        ):
            return target_extension  # type: ignore
        return DefaultSettings.target_extension

    def delimiter(self) -> str:
        self.reader.change_active_worksheet(OptionalSettingExcelAddress.delimiter.sheet_name)
        if delimiter := self.reader.read_cell_value_by_coordinate(OptionalSettingExcelAddress.delimiter.coordinate):
            return delimiter  # type: ignore
        return DefaultSettings.delimiter

    def dst_folder(self) -> str:
        self.reader.change_active_worksheet(OptionalSettingExcelAddress.dst_folder.sheet_name)
        if dst_folder := self.reader.read_cell_value_by_coordinate(OptionalSettingExcelAddress.dst_folder.coordinate):
            return dst_folder  # type: ignore
        return DefaultSettings.dst_folder
