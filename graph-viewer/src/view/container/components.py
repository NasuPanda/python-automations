import os
import tkinter
from typing import Any

import PySimpleGUI as sg

from src.common.constants import FILE_ICON, FOLDER_ICON, ComponentKeys
from src.common import utils
from src.data.graph.graph import Graph
from src.data.store import DataStore
from src.view.presentational import components


def generate_tree_data(parent: str, folder_path: str) -> sg.TreeData:
    """フォルダから tree_data (for Tree element) を生成する。"""
    tree_data = sg.TreeData()

    # https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Tree_Element.py#L26
    def add_files_in_folder(parent: str, folder_path: str) -> None:
        """再帰関数。tree_dataにフォルダ、ファイルを追加する。"""
        files = os.listdir(folder_path)

        for f in files:
            fullname = os.path.join(folder_path, f)
            if os.path.isdir(fullname):
                tree_data.Insert(parent, fullname, f, values=[], icon=FOLDER_ICON)
                add_files_in_folder(fullname, fullname)
            else:
                # NOTE: csv 以外は表示しない
                if fullname[-4:] == ".csv":
                    tree_data.Insert(parent, fullname, f, values=[os.stat(fullname).st_size], icon=FILE_ICON)

    add_files_in_folder(parent, folder_path)

    return tree_data


class UserInterface:
    def __init__(self) -> None:
        layout = components.layout(generate_tree_data("", os.getcwd()))
        self.window = components.window(layout)
        self.data_store = DataStore()
        self.graph = Graph(self._get_canvas(), (10, 8))

        self.events = {
            ComponentKeys.csv_headers_listbox: self.on_select_csv_header,
            ComponentKeys.explorer_tree: self.on_click_tree,
            ComponentKeys.folder_input: self.on_input_folder,
            ComponentKeys.graph_range_update: self.on_click_update_graph_range,
        }

    def start_event_loop(self) -> None:
        """イベントループを発生させる。"""
        while True:
            event, self.values = self.window.read()

            if event is None:
                break

            else:
                self.events[event]()

    def _display_error(self, *display_text: str) -> None:
        components.popup_error(*display_text)

    def _get_canvas(self) -> tkinter.Canvas:
        """private Canvas を受け取る。"""
        return self.window[ComponentKeys.graph_canvas].TKCanvas  # type: ignore

    def _get_csv_headers(self) -> list[str]:
        """private 選択されたcsvヘッダを返す。(リスト形式なので注意)

        Returns:
            list[str]: 選択された csvヘッダ のリスト。
        """
        return self.window[ComponentKeys.csv_headers_listbox].get()  # type: ignore

    def _get_folder_input(self) -> str:
        """private フォルダ入力を受け取る。"""
        return self.window[ComponentKeys.folder_input].get()

    def _get_values(self, key: str) -> Any:
        """private 特定のキーのvaluesを取得する。"""
        try:
            return self.values[key]
        except AttributeError:
            print("read_window が実行されていません!")

    def _get_graph_x_range(self) -> tuple[float, float] | None:
        x_min = self._get_values(ComponentKeys.graph_x_axis_min_range_input)
        x_max = self._get_values(ComponentKeys.graph_x_axis_max_range_input)

        if x_min == "" or x_max == "":
            return None
        if utils.validate_input_min_max_range(x_min, x_max):
            return (float(x_min), float(x_max))
        self._display_error("X軸のレンジに無効な値が含まれています")

    def _get_graph_y_range(self) -> tuple[float, float] | None:
        y_min = self._get_values(ComponentKeys.graph_y_axis_min_range_input)
        y_max = self._get_values(ComponentKeys.graph_y_axis_max_range_input)

        if y_min == "" or y_max == "":
            return None
        if utils.validate_input_min_max_range(y_min, y_max):
            return (float(y_min), float(y_max))
        self._display_error("Y軸のレンジに無効な値が含まれています")

    def _update_graph_canvas(self) -> None:
        """グラフを更新する。"""
        self.graph.clear()
        values_of_time_axis = self.data_store.values_of_csv_time_axis

        if values_of_time_axis:
            # TODO 次のエラーの対策 ➞ ValueError: x and y must have same first dimension, but have shapes (10136,) and (13639,)
            # 配列の長さを短い方に合わせるとか。
            self._update_time_axis_indicator(True)
            [
                self.graph.plot(y_values=plot.data, label=plot.label, x_values=values_of_time_axis)
                for plot in self.data_store.plots
            ]
        else:
            self._update_time_axis_indicator(False)
            [self.graph.plot(y_values=plot.data, label=plot.label) for plot in self.data_store.plots]

        self.graph.commit_change()

    def _update_csv_headers_listbox(self) -> None:
        self.window[ComponentKeys.csv_headers_listbox].update(values=self.data_store.csv_headers)

    def _update_x_range(self) -> None:
        x_range = self._get_graph_x_range()

        if x_range:
            self.graph.set_x_range(x_range)
            self.graph.commit_change()

    def _update_y_range(self) -> None:
        y_range = self._get_graph_y_range()

        if y_range:
            self.graph.set_y_range(y_range)
            self.graph.commit_change()

    def _reset_data_referring_to_tree(self) -> None:
        self.data_store.update_plots_by_headers([])
        self.data_store.update_plots_by_filepaths([])
        self._update_csv_headers_listbox()
        self._update_graph_canvas()

    def _update_time_axis_indicator(self, is_time_axis: bool) -> None:
        indicator_text = "Yes" if is_time_axis else "No"
        self.window[ComponentKeys.time_axis_indicator_text].update(indicator_text)

    def on_click_tree(self) -> None:
        """csv_reader, csv_header_listbox, グラフ を更新する処理。"""
        filepaths = [i for i in self._get_values(ComponentKeys.explorer_tree) if not os.path.isdir(i)]

        # 何も選ばれていない or ディレクトリだけ選ばれている場合
        if not filepaths:
            self.data_store.update_plots_by_filepaths([])
            return

        self.data_store.update_plots_by_filepaths(filepaths)
        self._update_csv_headers_listbox()
        self._update_graph_canvas()

    def on_select_csv_header(self) -> None:
        """グラフを更新する処理。"""
        csv_headers = self._get_csv_headers()
        if not csv_headers:
            self.data_store.update_plots_by_headers([])
            return

        self.data_store.update_plots_by_headers(csv_headers)
        self._update_graph_canvas()

    def on_input_folder(self) -> None:
        """ツリーを更新する処理。"""
        tree_data = generate_tree_data("", self._get_folder_input())
        self.window[ComponentKeys.explorer_tree].update(values=tree_data)
        self._reset_data_referring_to_tree()

    def on_click_update_graph_range(self) -> None:
        self._update_x_range()
        self._update_y_range()
