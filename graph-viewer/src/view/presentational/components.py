"""TODO docs の記述
"""
import PySimpleGUI as sg

from src.common.constants import BASELINE_COLOR_1, BASELINE_COLOR_2, TIME_AXIS_INDICATOR_TEXTS, ComponentKeys


def _common_input_styles(key) -> dict:
    return {"default_text": "", "key": key, "size": (10, 1)}


def _common_margin_component(width: int = 1, height: int = 1) -> sg.T:
    margin_styles = {
        "text": "",
        "size": (width, height),
    }

    return sg.T(**margin_styles)


def folder_browse_components() -> tuple[sg.Input, sg.Button]:
    folder_input_styles = {
        "default_text": "",
        "enable_events": True,
        "readonly": True,
        "key": ComponentKeys.folder_input,
    }
    folder_browse_styles = {
        "button_text": "フォルダを選択",
    }
    return sg.Input(**folder_input_styles), sg.FolderBrowse(**folder_browse_styles)


def explorer_tree_component(tree_data: sg.TreeData) -> sg.Tree:
    explorer_tree_styles = {
        "data": tree_data,
        "key": ComponentKeys.explorer_tree,
        "headings": [],
        "auto_size_columns": True,
        # num_row: max number of row
        "num_rows": 24,
        "col0_width": 56,
        "show_expanded": False,
        "enable_events": True,
        "tooltip": "Ctrl + クリックで複数選択",
    }
    return sg.Tree(**explorer_tree_styles)


def csv_header_listbox_component() -> sg.Frame:
    csv_headers_listbox_styles = {
        "values": ["CSVファイルを選択してください"],
        "key": ComponentKeys.csv_headers_listbox,
        "enable_events": True,
        # 横, 縦の順
        "size": (70, 15),
        "auto_size_text": True,
        "select_mode": sg.LISTBOX_SELECT_MODE_MULTIPLE,
    }
    select_csv_headers_frame_styles = {
        "title": "グラフに表示する列",
        "layout": [
            [sg.Listbox(**csv_headers_listbox_styles)],
        ],
    }

    return sg.Frame(**select_csv_headers_frame_styles)


def log_multiline_component() -> sg.Multiline:
    log_styles = {
        "size": (70, 6),
        "key": ComponentKeys.log,
        "disabled": True,
        "no_scrollbar": True,
    }
    log_frame_styles = {
        "title": "ログ",
        "layout": [
            [sg.Multiline(**log_styles)],
        ],
    }

    return sg.Frame(**log_frame_styles)


def graph_canvas_component() -> sg.Canvas:
    graph_canvas = {
        "key": ComponentKeys.graph_canvas,
        # "size": (1, 1),
    }

    return sg.Canvas(**graph_canvas)


def adjust_graph_range_frame_component() -> sg.Frame:
    graph_x_axis_range_text = {"text": "X軸"}
    graph_y_axis_range_text = {"text": "Y軸"}
    graph_range_min_text = {"text": "Min"}
    graph_range_max_text = {"text": "Max"}
    graph_range_value_text = {"text": "～"}
    # pad: left, right, top, bottom
    pad_l, pad_r, pad_t, pad_b = 100, 0, 20, 10
    graph_range_value_update_styles = {
        "button_text": "更新",
        "key": ComponentKeys.graph_range_update,
        "pad": ((pad_l, pad_r), (pad_t, pad_b)),
        "font": "Monospace 15",
    }
    btn_text_color, btn_bg_color = sg.theme_button_color()
    graph_range_reset_button_styles = {
        "button_text": "リセット",
        "key": ComponentKeys.graph_range_reset,
        "pad": ((pad_l, pad_r), (pad_t, pad_b)),
        "font": "Monospace 15",
        "button_color": ("red", btn_bg_color),
    }

    adjust_graph_range_frame_styles = {
        "title": "グラフレンジ調整",
        "layout": [
            [
                sg.T(**graph_x_axis_range_text),
                sg.T(**graph_range_min_text),
                sg.Input(**_common_input_styles(ComponentKeys.graph_x_axis_min_range_input)),
                sg.T(**graph_range_value_text),
                sg.T(**graph_range_max_text),
                sg.Input(**_common_input_styles(ComponentKeys.graph_x_axis_max_range_input)),
            ],
            [
                sg.T(**graph_y_axis_range_text),
                sg.T(**graph_range_min_text),
                sg.Input(**_common_input_styles(ComponentKeys.graph_y_axis_min_range_input)),
                sg.T(**graph_range_value_text),
                sg.T(**graph_range_max_text),
                sg.Input(**_common_input_styles(ComponentKeys.graph_y_axis_max_range_input)),
            ],
            [sg.Button(**graph_range_value_update_styles), sg.Button(**graph_range_reset_button_styles)],
        ],
    }

    return sg.Frame(**adjust_graph_range_frame_styles)


def time_axis_indicator_components() -> tuple[sg.T, sg.T]:
    time_axis_indicator_desc_text_style = {"text": "X軸 :"}
    time_axis_indicator_text_style = {
        "text": TIME_AXIS_INDICATOR_TEXTS["n"],
        "key": ComponentKeys.time_axis_indicator_text,
    }

    return sg.T(**time_axis_indicator_desc_text_style), sg.T(**time_axis_indicator_text_style)


def base_hline_components() -> sg.Frame:

    baseline1_text_styles = {"text": "規格線(Y軸)-1", "text_color": BASELINE_COLOR_1}
    baseline2_text_styles = {"text": "規格線(Y軸)-2", "text_color": BASELINE_COLOR_2}
    # pad: left, right, top, bottom
    pad_l, pad_r, pad_t, pad_b = 100, 0, 20, 10
    baselines_update_styles = {
        "button_text": "更新",
        "key": ComponentKeys.baselines_update,
        "pad": ((pad_l, pad_r), (pad_t, pad_b)),
        "font": "Monospace 15",
    }

    baselines_frame_styles = {
        "title": "規格線",
        "layout": [
            [
                sg.T(**baseline1_text_styles),
                sg.Input(**_common_input_styles(ComponentKeys.baseline1_input)),
            ],
            [
                sg.T(**baseline2_text_styles),
                sg.Input(**_common_input_styles(ComponentKeys.baseline2_input)),
            ],
            [sg.Button(**baselines_update_styles)],
        ],
    }

    return sg.Frame(**baselines_frame_styles)


def layout(tree_data: sg.TreeData) -> list:
    col_1 = [
        [*folder_browse_components()],
        [explorer_tree_component(tree_data)],
        [_common_margin_component(1, 1)],
        [csv_header_listbox_component()],
        [_common_margin_component(1, 1)],
        [log_multiline_component()],
    ]
    col_2 = [
        [graph_canvas_component()],
        [adjust_graph_range_frame_component(), *time_axis_indicator_components(), base_hline_components()],
    ]

    return [
        [sg.Column(col_1), sg.Column(col_2)],
    ]


def window(layout: list) -> sg.Window:
    window_styles = {
        "title": "CSV Graph Viewer",
        "layout": layout,
        "finalize": True,
        "resizable": True,
        "element_justification": "center",
        "font": "Monospace 12",
        "location": (0, 0),
        "size": (1800, 1000),
    }

    return sg.Window(**window_styles)


def popup_get_folder() -> str:
    return sg.popup_get_folder("最初に開くフォルダ", title="Input initial folder")
