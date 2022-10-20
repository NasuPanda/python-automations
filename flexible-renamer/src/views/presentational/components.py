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
    browse_styles = {
        "button_text": "ファイルを選択",
    }

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


def _setting_name_part_index_combo_components(values: list[int] = []) -> tuple[sg.Text, sg.Combo, sg.Text, sg.Combo]:
    before_desc_styles = {"text": "サンプル名    変更前"}
    after_desc_styles = {"text": "変更後"}
    before_combo_styles = {
        "values": values,
        "default_value": DefaultSettings.name_index.before,
        "key": ComponentKeys.name_part_index_combo["before"],
    }
    after_combo_styles = {
        "values": values,
        "default_value": DefaultSettings.name_index.after,
        "key": ComponentKeys.name_part_index_combo["after"],
    }

    return (
        sg.Text(**before_desc_styles),
        sg.Combo(**before_combo_styles),
        sg.Text(**after_desc_styles),
        sg.Combo(**after_combo_styles),
    )


def _setting_layout_part_index_combo_components(values: list[int] = []) -> tuple[sg.Text, sg.Combo, sg.Text, sg.Combo]:
    before_desc_styles = {"text": "撮影箇所    変更前"}
    after_desc_styles = {"text": "変更後"}
    before_combo_styles = {
        "values": values,
        "default_value": DefaultSettings.layout_index.before,
        "key": ComponentKeys.layout_part_index_combo["before"],
    }
    after_combo_styles = {
        "values": values,
        "default_value": DefaultSettings.layout_index.after,
        "key": ComponentKeys.layout_part_index_combo["after"],
    }

    return (
        sg.Text(**before_desc_styles),
        sg.Combo(**before_combo_styles),
        sg.Text(**after_desc_styles),
        sg.Combo(**after_combo_styles),
    )


def setting_frame() -> sg.Frame:
    frame_styles = {
        "title": "設定",
        "layout": [
            [*_setting_folder_browse_components()],
            [*_setting_name_part_index_combo_components()],
            [*_setting_layout_part_index_combo_components()],
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


def save_setting_frame() -> sg.Frame:
    input_desc_styles = {"text": "ファイル名(拡張子不要)"}
    input_styles = {"default_text": "", "key": ComponentKeys.save_filename, "size": (20, 1)}
    checkbox_styles = {
        "text": "設定を保存する",
        "default": True,
    }

    frame_styles = {
        "title": "設定の保存",
        "layout": [
            [sg.Checkbox(**checkbox_styles)],
            [sg.Text(**input_desc_styles), sg.Input(**input_styles)],
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
        [_common_margin_component(height=2)],
        [setting_frame()],
        [preview_frame()],
        [_common_margin_component(height=1)],
        [save_setting_frame()],
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
