import PySimpleGUI as sg

from src.common.constants import ComponentKeys


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


def csv_header_listbox_component() -> sg.Listbox:
    csv_headers_listbox_styles = {
        "values": ["CSVファイルを選択してください"],
        "key": ComponentKeys.csv_headers_listbox,
        "enable_events": True,
        # 横, 縦の順
        "size": (70, 15),
        "auto_size_text": True,
        "select_mode": sg.LISTBOX_SELECT_MODE_MULTIPLE,
    }

    return sg.Listbox(**csv_headers_listbox_styles)


def explorer_tree_component(tree_data: sg.TreeData) -> sg.Tree:
    explorer_tree_styles = {
        "data": tree_data,
        "headings": [],
        "auto_size_columns": True,
        # num_row: max number of row
        "num_rows": 24,
        "col0_width": 56,
        "key": ComponentKeys.explorer_tree,
        "show_expanded": False,
        "enable_events": True,
    }
    return sg.Tree(**explorer_tree_styles)


def graph_canvas_component() -> sg.Canvas:
    graph_canvas = {
        "key": ComponentKeys.graph_canvas,
        # "size": (1, 1),
    }

    return sg.Canvas(**graph_canvas)


def adjust_graph_range_frame_component() -> sg.Frame:
    graph_x_axis_range_desc_styles = {"text": "X軸"}
    graph_y_axis_range_desc_styles = {"text": "Y軸"}
    graph_range_value_text = {"text": "～"}

    def graph_range_value_input_styles(key) -> dict:
        return {"default_text": "", "key": key, "size": (10, 1)}

    graph_range_value_update_styles = {"button_text": "更新", "key": ComponentKeys.graph_range_update}

    adjust_graph_range_frame_styles = {
        "title": "グラフレンジ調整",
        "layout": [
            [
                sg.T(**graph_x_axis_range_desc_styles),
                sg.Input(**graph_range_value_input_styles(ComponentKeys.graph_x_axis_min_range_input)),
                sg.T(**graph_range_value_text),
                sg.Input(**graph_range_value_input_styles(ComponentKeys.graph_x_axis_max_range_input)),
            ],
            [
                sg.T(**graph_y_axis_range_desc_styles),
                sg.Input(**graph_range_value_input_styles(ComponentKeys.graph_y_axis_min_range_input)),
                sg.T(**graph_range_value_text),
                sg.Input(**graph_range_value_input_styles(ComponentKeys.graph_y_axis_max_range_input)),
            ],
            [sg.Button(**graph_range_value_update_styles)],
        ],
    }

    return sg.Frame(**adjust_graph_range_frame_styles)


def time_axis_indicator_components() -> tuple[sg.T, sg.T]:
    time_axis_indicator_desc_text_style = {"text": "X軸 = 時間軸: "}
    time_axis_indicator_text_style = {
        "text": "No",
        "key": ComponentKeys.time_axis_indicator_text,
    }

    return sg.T(**time_axis_indicator_desc_text_style), sg.T(**time_axis_indicator_text_style)


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


def margin_component(height: int = 1) -> sg.T:
    margin_styles = {
        "text": "",
        "size": (1, height),
    }

    return sg.T(**margin_styles)


def layout(tree_data: sg.TreeData) -> list:
    col_1 = [
        [*folder_browse_components()],
        [explorer_tree_component(tree_data)],
        [margin_component(1)],
        [csv_header_listbox_component()],
        [margin_component(1)],
        [log_multiline_component()],
    ]
    col_2 = [
        [graph_canvas_component()],
        [adjust_graph_range_frame_component(), *time_axis_indicator_components()],
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


def popup_error(*display_text: str) -> None:
    sg.popup_error(*display_text, title="Error")
