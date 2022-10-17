import PySimpleGUI as sg

from src.common.constants import BASE_HLINE_COLORS, TIME_AXIS_INDICATOR_TEXTS, ComponentKeys


FONT = "Monospace"


def _common_input_styles(key: str) -> dict:
    return {"default_text": "", "key": key, "size": (10, 1)}


def _common_margin_component(width: int = 1, height: int = 1) -> sg.Text:
    margin_styles = {
        "text": "",
        "size": (width, height),
    }

    return sg.Text(**margin_styles)


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


def select_csv_header_frame() -> sg.Frame:
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


def log_frame() -> sg.Frame:
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


def adjust_graph_range_frame() -> sg.Frame:
    x_axis_text_styles = {"text": "X軸"}
    y_axis_text_styles = {"text": "Y軸"}
    min_range_text_styles = {"text": "Min"}
    max_range_text_styles = {"text": "Max"}
    range_text_styles = {"text": "～"}
    # pad: left, right, top, bottom
    pad_l, pad_r, pad_t, pad_b = 100, 0, 20, 10
    update_range_button_styles = {
        "button_text": "更新",
        "key": ComponentKeys.graph_range_update,
        "pad": ((pad_l, pad_r), (pad_t, pad_b)),
        "font": f"{FONT} 15",
    }
    __, btn_bg_color = sg.theme_button_color()
    reset_range_button_styles = {
        "button_text": "リセット",
        "key": ComponentKeys.graph_range_reset,
        "pad": ((pad_l, pad_r), (pad_t, pad_b)),
        "font": f"{FONT} 15",
        "button_color": ("red", btn_bg_color),
    }

    adjust_graph_range_frame_styles = {
        "title": "グラフレンジ調整",
        "layout": [
            [
                sg.T(**x_axis_text_styles),
                sg.T(**min_range_text_styles),
                sg.Input(**_common_input_styles(ComponentKeys.graph_range["x"]["min"])),
                sg.T(**range_text_styles),
                sg.T(**max_range_text_styles),
                sg.Input(**_common_input_styles(ComponentKeys.graph_range["x"]["max"])),
            ],
            [
                sg.T(**y_axis_text_styles),
                sg.T(**min_range_text_styles),
                sg.Input(**_common_input_styles(ComponentKeys.graph_range["y"]["min"])),
                sg.T(**range_text_styles),
                sg.T(**max_range_text_styles),
                sg.Input(**_common_input_styles(ComponentKeys.graph_range["y"]["max"])),
            ],
            [sg.Button(**update_range_button_styles), sg.Button(**reset_range_button_styles)],
        ],
    }

    return sg.Frame(**adjust_graph_range_frame_styles)


def x_axis_indicator_components() -> tuple[sg.Text, sg.Text]:
    x_axis_indicator_text_styles = {"text": "X軸 :"}
    x_axis_indicator_styles = {
        "text": TIME_AXIS_INDICATOR_TEXTS["n"],
        "key": ComponentKeys.time_axis_indicator_text,
    }

    return sg.Text(**x_axis_indicator_text_styles), sg.Text(**x_axis_indicator_styles)


def base_hline_frame() -> sg.Frame:

    baseline1_text_styles = {"text": "規格線(Y軸)-1", "text_color": BASE_HLINE_COLORS["1"]}
    baseline2_text_styles = {"text": "規格線(Y軸)-2", "text_color": BASE_HLINE_COLORS["2"]}
    # pad: left, right, top, bottom
    pad_l, pad_r, pad_t, pad_b = 100, 0, 20, 10
    update_baselines_button_styles = {
        "button_text": "更新",
        "key": ComponentKeys.baselines_update,
        "pad": ((pad_l, pad_r), (pad_t, pad_b)),
        "font": f"{FONT} 15",
    }

    base_hline_frame_styles = {
        "title": "規格線",
        "layout": [
            [
                sg.T(**baseline1_text_styles),
                sg.Input(**_common_input_styles(ComponentKeys.base_hline_input["1"])),
            ],
            [
                sg.T(**baseline2_text_styles),
                sg.Input(**_common_input_styles(ComponentKeys.base_hline_input["2"])),
            ],
            [sg.Button(**update_baselines_button_styles)],
        ],
    }

    return sg.Frame(**base_hline_frame_styles)


def layout(tree_data: sg.TreeData) -> list:
    col_1 = [
        [*folder_browse_components()],
        [explorer_tree_component(tree_data)],
        [_common_margin_component(1, 1)],
        [select_csv_header_frame()],
        [_common_margin_component(1, 1)],
        [log_frame()],
    ]
    col_2 = [
        [graph_canvas_component()],
        [adjust_graph_range_frame(), *x_axis_indicator_components(), base_hline_frame()],
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
        "font": f"{FONT} 12",
        "location": (0, 0),
        "size": (1800, 1000),
    }

    return sg.Window(**window_styles)


def popup_get_folder() -> str:
    return sg.popup_get_folder("最初に開くフォルダ", title="Input initial folder")
