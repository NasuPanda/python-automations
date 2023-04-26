"""定数値設定用モジュール
"""
from dataclasses import dataclass

"""GUI"""


@dataclass
class UIEventKeys:
    """UIコンポーネントのイベント管理用キー"""

    setting_file_input = "-SETTING_FILE-"
    folder_input = "-FOLDER-"
    previewer = "-RENAME_PREVIEW-"
    exec_button = "-EXECUTE-"
    log = "-LOG-"


@dataclass
class LogTextColors:
    alert = "#F55050"
    notice = "#5DBB63"


@dataclass
class DefaultText:
    user_setting = "設定ファイル"
    folder = "ファイルが保存されたフォルダ"


APP_TITLE = "サンプルGUI"
APP_THEME_COLOR = "LightGray6"  # https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Theme_Color_Swatches.py
APP_FONT = "Monospace"
APP_PREVIEWER_HEIGHT = 10
APP_LOG_HEIGHT = 12
APP_INPUT_TEXT_COLOR = "#808A93"


"""Setting"""
TARGET_EXTENSION = ".csv"

"""Excel(UserSetting)"""


@dataclass
class UserSettingKeys:
    """ユーザ設定値
    """

    key1 = "A2"
    key2 = "B2"
    key3 = "C2"
    key4 = "D2"
