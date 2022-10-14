"""TODO docs の記述
"""
import os
import tkinter
from typing import Any

import PySimpleGUI as sg

from src.common import utils
from src.common import types
from src.common.constants import (
    ALERT_COLOR,
    BASELINE_COLOR_1,
    BASELINE_COLOR_2,
    FILE_ICON,
    FOLDER_ICON,
    NOTICE_COLOR,
    TIME_AXIS_INDICATOR_TEXTS,
    ComponentKeys,
)
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
        initial_folder = components.popup_get_folder()
        if not utils.is_dir(initial_folder):
            raise FileNotFoundError("指定されたパスが見つかりません:", initial_folder)
        layout = components.layout(generate_tree_data("", initial_folder if initial_folder else os.getcwd()))
        self.window = components.window(layout)
        self.data_store = DataStore()
        self.graph = Graph(self._get_canvas(), (10, 8))

        self.events = {
            ComponentKeys.csv_headers_listbox: self.on_select_csv_header,
            ComponentKeys.explorer_tree: self.on_click_tree,
            ComponentKeys.folder_input: self.on_input_folder,
            ComponentKeys.graph_range_update: self.on_click_update_graph_range,
            ComponentKeys.graph_range_reset: self.on_click_reset_graph_range,
            ComponentKeys.baselines_update: self.on_click_update_baselines,
        }

    def start_event_loop(self) -> None:
        """イベントループを発生させる。"""
        while True:
            event, self.values = self.window.read()  # type: ignore

            if event is None:
                break

            else:
                self.events[event]()

    def _print_notice(self, *messages: str) -> None:
        [self.window[ComponentKeys.log].print(message, t=NOTICE_COLOR) for message in messages]  # type: ignore

    def _print_alert(self, *messages: str) -> None:
        [self.window[ComponentKeys.log].print(message, t=ALERT_COLOR) for message in messages]  # type: ignore

    def _get_canvas(self) -> tkinter.Canvas:
        """private Canvas を受け取る。"""
        return self.window[ComponentKeys.graph_canvas].TKCanvas  # type: ignore

    def _get_values(self, key: str) -> Any:
        """private 特定のキーのvaluesを取得する。"""
        try:
            return self.values[key]
        except AttributeError:
            print("read_window が実行されていません!")

    def get_csv_headers(self) -> list[str]:
        """private 選択されたcsvヘッダを返す。(リスト形式なので注意)

        Returns:
            list[str]: 選択された csvヘッダ のリスト。
        """
        return self.window[ComponentKeys.csv_headers_listbox].get()  # type: ignore

    def get_folder_input(self) -> str:
        """フォルダ入力を受け取る。"""
        return self.window[ComponentKeys.folder_input].get()

    def get_graph_range_values(self, axis: types.GraphAxis) -> tuple[float, float] | None:
        min = self._get_values(ComponentKeys.graph_range[axis]["min"])
        max = self._get_values(ComponentKeys.graph_range[axis]["max"])
        # 空白ならNone
        if min == "" or max == "":
            return None
        # バリデーションに成功したらfloatにキャストして返す
        if utils.validate_graph_min_max_range(min, max):
            return (float(min), float(max))
        # バリデーションに失敗したらエラー
        raise ValueError(f"{axis}軸のレンジに無効な値が含まれています: {min} ~ {max}")

    def get_base_hline1_value(self) -> float | None:
        # FIXME hline1, hline2 で分けない
        base_hline1_value = self._get_values(ComponentKeys.baseline1_input)

        if not base_hline1_value == "":
            if utils.validate_input_number(base_hline1_value):
                return float(base_hline1_value)
            else:
                self._print_alert("規格線1に無効な値が含まれています")

    def get_base_hline2_value(self) -> float | None:
        # FIXME hline1, hline2 で分けない
        base_hline2_value = self._get_values(ComponentKeys.baseline2_input)

        if not base_hline2_value == "":
            if utils.validate_input_number(base_hline2_value):
                return float(base_hline2_value)
            else:
                self._print_alert("規格線2に無効な値が含まれています")

    def _update_time_axis_indicator(self, is_time_axis: bool) -> None:
        indicator_text = TIME_AXIS_INDICATOR_TEXTS["y"] if is_time_axis else TIME_AXIS_INDICATOR_TEXTS["n"]
        self.window[ComponentKeys.time_axis_indicator_text].update(indicator_text)  # type: ignore

    def update_graph_canvas(self) -> None:
        """グラフを更新する。"""
        self.graph.clear()
        values_of_time_axis = self.data_store.values_of_csv_time_axis

        # x軸(時間軸)が存在する場合
        if values_of_time_axis:
            self._update_time_axis_indicator(True)

            for plot in self.data_store.plots:
                x_values, y_values = values_of_time_axis, plot.data
                try:
                    self.graph.plot(y_values=y_values, label=plot.label, x_values=x_values)
                except ValueError:
                    # ValueError: x and y must have same first dimension, but have shapes の対応
                    if len(x_values) > len(y_values):
                        # x(時間軸)の方が長い: y軸を0埋めする
                        y_values = y_values + [0] * (len(x_values) - len(y_values))
                        self.graph.plot(y_values=y_values, label=plot.label, x_values=x_values)
                        self._print_alert("x軸の方が長いため、y軸を0埋めしました")
                    else:
                        # yの方が長い: y軸を短くする
                        y_values = y_values[: len(x_values)]
                        self.graph.plot(y_values=y_values, label=plot.label, x_values=x_values)
                        self._print_alert("y軸の方が長いため、y軸をx軸に合わせました")
        # x軸(時間軸)が存在しない場合
        else:
            self._update_time_axis_indicator(False)
            [self.graph.plot(y_values=plot.data, label=plot.label) for plot in self.data_store.plots]

        # 毎回実行が必要なメソッド
        self.update_both_graph_range()
        self._update_base_hlines()
        self.graph.commit_change()

    def update_csv_headers_listbox(self) -> None:
        self.window[ComponentKeys.csv_headers_listbox].update(values=self.data_store.headers_of_csv_reader)

    def _update_x_range(self) -> None:
        try:
            x_range = self.get_graph_range_values("x")
        except ValueError:
            self._print_alert("X軸のレンジに無効な値が含まれています")
            return

        if x_range:
            self.graph.set_x_range(x_range)
        else:
            self.graph.auto_scale_x_range()

    def _update_y_range(self) -> None:
        try:
            y_range = self.get_graph_range_values("y")
        except ValueError:
            self._print_alert("Y軸のレンジに無効な値が含まれています")
            return

        if y_range:
            self.graph.set_y_range(y_range)
        else:
            self.graph.auto_scale_y_range()

    def reset_data_referring_to_tree(self) -> None:
        self.data_store.update_plots_by_headers([])
        self.data_store.update_plots_by_filepaths([])
        self.update_csv_headers_listbox()
        self.update_graph_canvas()

    def update_both_graph_range(self) -> None:
        self._update_x_range()
        self._update_y_range()
        self.graph.commit_change()

    def reset_both_graph_range(self) -> None:
        self.window[ComponentKeys.graph_x_axis_min_range_input].update("")  # type: ignore
        self.window[ComponentKeys.graph_x_axis_max_range_input].update("")  # type: ignore
        self.window[ComponentKeys.graph_y_axis_min_range_input].update("")  # type: ignore
        self.window[ComponentKeys.graph_y_axis_max_range_input].update("")  # type: ignore
        # NOTE: input の値をクリア ➞ update_graph_range()でグラフを更新する ことは出来ない
        # PySimpleGUI の仕様上、1回のイベントで更新できるコンポーネントは1つしか無いため
        self.graph.auto_scale_x_range()
        self.graph.auto_scale_y_range()
        self.graph.commit_change()

    def _update_base_hlines(self) -> None:
        if hline1_value := self.get_base_hline1_value():
            self.graph.plot_hline(hline1_value, BASELINE_COLOR_1)
        if hline2_value := self.get_base_hline2_value():
            self.graph.plot_hline(hline2_value, BASELINE_COLOR_2)
        self.graph.commit_change()

    def on_click_tree(self) -> None:
        """csv_reader, csv_header_listbox, グラフ を更新する処理。"""
        filepaths = [i for i in self._get_values(ComponentKeys.explorer_tree) if not utils.is_dir(i)]

        # 何も選ばれていない or ディレクトリだけ選ばれている場合
        if not filepaths:
            self.data_store.update_plots_by_filepaths([])
            return

        # 存在しないcsvヘッダが選ばれた場合
        try:
            self.data_store.update_plots_by_filepaths(filepaths)
        except ValueError:
            self._print_alert("存在しないcsvヘッダが指定されました", "データを確認してください")
            self.reset_data_referring_to_tree()
            return
        self.update_csv_headers_listbox()
        self.update_graph_canvas()

    def on_select_csv_header(self) -> None:
        """グラフを更新する処理。"""
        csv_headers = self.get_csv_headers()
        if not csv_headers:
            self.data_store.update_plots_by_headers([])
            return

        # 存在しないcsvヘッダが選ばれた場合
        try:
            self.data_store.update_plots_by_headers(csv_headers)
        except ValueError:
            self._print_alert("存在しないcsvヘッダが指定されました", "データを確認してください")
            self.reset_data_referring_to_tree()
            return
        self.update_graph_canvas()

    def on_input_folder(self) -> None:
        """ツリーを更新する処理。"""
        tree_data = generate_tree_data("", self.get_folder_input())
        self.window[ComponentKeys.explorer_tree].update(values=tree_data)
        self.reset_data_referring_to_tree()
        self._print_notice("フォルダの読み込みが完了しました")

    def on_click_update_graph_range(self) -> None:
        self.update_both_graph_range()
        self._print_notice("グラフのレンジを更新しました")

    def on_click_reset_graph_range(self) -> None:
        self.reset_both_graph_range()
        self._print_notice("グラフのレンジをリセットしました")

    def on_click_update_baselines(self) -> None:
        # hline の描画だけ呼び出すと無限に描画されてしまう
        # clear を挟むために _update_graph_canvas を呼ぶようにする
        self.update_graph_canvas()
        self._print_notice("規格線を更新しました")
