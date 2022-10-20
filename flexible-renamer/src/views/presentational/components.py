import PySimpleGUI as sg

from src.common.constants import FONT, ComponentKeys, DefaultSettings


def _common_margin_component(width: int = 1, height: int = 1) -> sg.Text:
    margin_styles = {
        "text": "",
        "size": (width, height),
    }

    return sg.Text(**margin_styles)


def setting_file_frame() -> sg.Frame:
    input_styles = {
        "default_text": "",
        "enable_events": True,
        "readonly": True,
        "key": ComponentKeys.input_setting_file,
    }
    browse_styles = {"button_text": "ファイルを選択", "file_types": (("Excelファイル", "*.xlsx"),)}

    frame_styles = {
        "title": "設定ファイル入力",
        "layout": [[sg.Input(**input_styles), sg.FileBrowse(**browse_styles)]],
    }

    return sg.Frame(**frame_styles)


def _setting_folder_browse_components() -> tuple[sg.Input, sg.Button]:
    input_styles = {
        "default_text": "",
        "enable_events": True,
        "readonly": True,
        "key": ComponentKeys.input_folder,
    }
    browse_styles = {
        "button_text": "フォルダを選択",
    }
    return sg.Input(**input_styles), sg.FolderBrowse(**browse_styles)


def setting_frame() -> sg.Frame:
    frame_styles = {
        "title": "画像フォルダ入力",
        "layout": [
            [*_setting_folder_browse_components()],
        ],
    }
    return sg.Frame(**frame_styles)


def preview_frame() -> sg.Frame:
    multiline_styles = {
        "size": (70, 10),
        "key": ComponentKeys.multiline_preview,
        "disabled": True,
        "no_scrollbar": False,
    }
    frame_styles = {
        "title": "プレビュー",
        "layout": [
            [sg.Multiline(**multiline_styles)],
        ],
    }

    return sg.Frame(**frame_styles)


def submit_button_component() -> sg.Button:
    # pad: left, right, top, bottom
    pad_l, pad_r, pad_t, pad_b = 100, 0, 20, 10
    styles = {
        "button_text": "OK",
        "key": ComponentKeys.submit,
        "pad": ((pad_l, pad_r), (pad_t, pad_b)),
    }
    return sg.Button(**styles)


def window() -> sg.Window:
    layout = [
        [setting_file_frame()],
        [setting_frame()],
        [_common_margin_component(height=1)],
        [preview_frame()],
        [_common_margin_component(height=1)],
        [submit_button_component()],
    ]
    window_styles = {
        "title": "Flexible Renamer",
        "layout": layout,
        "finalize": True,
        "resizable": True,
        "element_justification": "left",
        "font": f"{FONT} 14",
        "location": (0, 0),
        "size": (1000, 800),
    }

    return sg.Window(**window_styles)


def popup_error(*messages: str) -> None:
    sg.popup_error(*messages, title="エラー")


def popup_ok(*messages: str) -> None:
    sg.popup_ok(*messages, title="通知")
