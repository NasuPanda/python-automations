import PySimpleGUI as sg

from src.common.constants import FONT, ComponentKeys


def folder_browse_components() -> tuple[sg.Input, sg.Button]:
    folder_input_styles = {
        "default_text": "",
        "enable_events": True,
        "readonly": True,
        "key": ComponentKeys.get_folder_popup_folder_input,
    }
    folder_browse_styles = {
        "button_text": "フォルダを選択",
    }
    return sg.Input(**folder_input_styles), sg.FolderBrowse(**folder_browse_styles)


def submit_button_component() -> sg.Button:
    # pad: left, right, top, bottom
    pad_l, pad_r, pad_t, pad_b = 100, 0, 20, 10
    styles = {
        "button_text": "OK",
        "key": ComponentKeys.get_folder_popup_submit,
        "pad": ((pad_l, pad_r), (pad_t, pad_b)),
        "font": f"{FONT} 15",
    }
    return sg.Button(**styles)


def layout() -> list:
    return [
        [*folder_browse_components()],
        [submit_button_component()],
    ]


def popup_get_folder() -> sg.Window:
    windows_styles = {
        "title": "Popup get folder",
        "layout": layout(),
        "element_justification": "center",
        "font": f"{FONT} 15",
        "location": (300, 300),
    }
    return sg.Window(**windows_styles)
