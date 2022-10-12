import PySimpleGUI as sg

from src.constants import FONT, ComponentKeys


def folder_browse_component() -> tuple[sg.Input, sg.Button]:
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
        "size": (500, 500),
    }

    return sg.Canvas(**graph_canvas)


def layout(tree_data: sg.TreeData) -> list:
    col_1 = [[*folder_browse_component()], [csv_header_listbox_component()], [explorer_tree_component(tree_data)]]
    col_2 = [[graph_canvas_component()]]

    return [
        [sg.Column(col_1), sg.Column(col_2)],
    ]


def window(layout: list) -> sg.Window:
    window_styles = {
        "title": "CSV Graph Viewer",
        "layout": layout,
        "finalize": True,
        "element_justification": "center",
        "font": f"{FONT} 12",
        "resizable": False,
    }

    return sg.Window(**window_styles)
