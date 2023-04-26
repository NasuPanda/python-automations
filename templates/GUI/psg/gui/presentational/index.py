"""UIをまとめてwindowを定義するモジュール
"""
import PySimpleGUI as sg

from common.constants import (
    APP_FONT,
    APP_INPUT_TEXT_COLOR,
    APP_THEME_COLOR,
    APP_TITLE,
    LogTextColors,
)
from gui.presentational import components

# テーマカラーの設定
sg.theme(APP_THEME_COLOR)
sg.DEFAULT_INPUT_TEXT_COLOR = APP_INPUT_TEXT_COLOR
sg.DEFAULT_ERROR_BUTTON_COLOR = LogTextColors.alert


def create_window() -> sg.Window:
    """ウィンドウの作成"""
    layout = [
        [
            *components.setting_file_browse_components(),
        ],
        [*components.folder_browse_components()],
        [components.margin_component(w=30, h=1), components.execute_button_component()],
        [components.preview_frame()],
        [components.log_frame()],
    ]
    window_styles = {
        "title": APP_TITLE,
        "layout": layout,
        "finalize": True,
        "resizable": True,
        "font": f"{APP_FONT} 12",
        # "location": (0, 0),
        # "size": (1800, 1000),
    }
    return sg.Window(**window_styles)
