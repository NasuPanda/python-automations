from dataclasses import dataclass

from src.common import types
from src.common.constants import DefaultSettings


@dataclass
class Config:
    setting_file_path: str
    # Excelから
    data_names: list[str]
    layouts: list[str]
    # 任意 or 入力
    input_folder_path: str
    name_index: types.PartIndexes
    layout_index: types.PartIndexes
    # 任意
    target_extension: str
    delimiter: str


# TODO parser から読み込む感じに変更する
config = Config(
    setting_file_path="./設定.xlsx",
    data_names=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    layouts=["上", "下", "右", "左"],
    input_folder_path="./",
    name_index=DefaultSettings.name_index,
    layout_index=DefaultSettings.layout_index,
    target_extension=DefaultSettings.target_extension,
    delimiter=DefaultSettings.delimiter,
)
