"""Presentational Components (ロジックを持たない) を定義するモジュール
"""
import PySimpleGUI as sg

from common.constants import (
    APP_FONT,
    APP_LOG_HEIGHT,
    APP_PREVIEWER_HEIGHT,
    DefaultText,
    UIEventKeys,
)


def margin_component(w=10, h=1) -> sg.Text:
    margin_styles = {"text": "", "size": (w, h)}
    return sg.Text(**margin_styles)


def setting_file_browse_components() -> tuple[sg.Input, sg.Button]:
    """設定ファイルを受け取るコンポーネント"""
    file_input_styles = {
        "default_text": DefaultText.user_setting,
        "enable_events": True,
        "disabled": True,
        "readonly": True,
        "disabled_readonly_text_color": sg.DEFAULT_INPUT_TEXT_COLOR,
        "key": UIEventKeys.setting_file_input,
    }
    file_browse_styles = {
        "button_text": "ファイル選択",
        "size": (15, 1),
        "file_types": (("Excel", ".xlsx"),),
    }
    return (
        sg.Input(**file_input_styles),
        sg.FileBrowse(**file_browse_styles),
    )


def folder_browse_components() -> tuple[sg.Input, sg.Button]:
    """フォルダを受け取るコンポーネント"""
    folder_input_styles = {
        "default_text": DefaultText.folder,
        "enable_events": True,
        "disabled": True,
        "readonly": True,
        "disabled_readonly_text_color": sg.DEFAULT_INPUT_TEXT_COLOR,
        "key": UIEventKeys.folder_input,
    }
    folder_browse_styles = {
        "button_text": "フォルダ選択",
        "size": (15, 1),
    }
    return (
        sg.Input(**folder_input_styles),
        sg.FolderBrowse(**folder_browse_styles),
    )


def execute_button_component() -> sg.Button:
    """実行ボタンコンポーネント"""
    execute_button_styles = {
        "button_text": "実行",
        "key": UIEventKeys.exec_button,
        "size": (13, 1),
        "font": f"{APP_FONT} 13 bold",
    }
    return sg.Button(**execute_button_styles)


def preview_frame() -> sg.Frame:
    """プレビュー確認用コンポーネント"""
    preview_multiline_styles = {
        "size": (90, APP_PREVIEWER_HEIGHT),
        "key": UIEventKeys.previewer,
        "disabled": True,
        "no_scrollbar": False,
    }
    frame_styles = {
        "title": "結果のプレビュー",
        "layout": [
            [sg.Multiline(**preview_multiline_styles)],
        ],
    }

    return sg.Frame(**frame_styles)


def log_frame() -> sg.Frame:
    """ログ表示用コンポーネント"""
    log_multiline_styles = {
        "size": (90, APP_LOG_HEIGHT),
        "key": UIEventKeys.log,
        "disabled": True,
        "no_scrollbar": False,
    }
    frame_styles = {"title": "ログ", "layout": [[sg.Multiline(**log_multiline_styles)]]}
    return sg.Frame(**frame_styles)
