import os
import tkinter
from typing import Any

import PySimpleGUI as sg

from src.common import types, utils
from src.common.constants import (
    BASE_HLINE_COLORS,
    BASE_HLINE_NUMBERS,
    FILE_ICON,
    FOLDER_ICON,
    LOG_TEXT_COLORS,
    TIME_AXIS_INDICATOR_TEXTS,
    ComponentKeys,
)
from src.data.graph import GraphPlotter
from src.data.store import DataStore
from src.view.presentational import components


def generate_tree_data(parent: str, folder_path: str) -> sg.TreeData:
    """フォルダから tree_data (for Tree element) を生成する"""
    tree_data = sg.TreeData()

    # https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Tree_Element.py#L26
    def add_files_in_folder(parent: str, folder_path: str) -> None:
        """再帰関数tree_dataにフォルダ、ファイルを追加する"""
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
    def __init__(self, initial_folder: str) -> None:
        if not utils.is_dir(initial_folder):
            raise FileNotFoundError("指定されたパスが見つかりません:", initial_folder)
        self.window = components.window(
            components.layout(generate_tree_data("", initial_folder if initial_folder else os.getcwd()))
        )
        self.data_store = DataStore()
        self.graph = GraphPlotter(self._get_canvas(), (10, 8))

        self.events = {
            ComponentKeys.csv_headers_listbox: self.on_select_csv_header,
            ComponentKeys.explorer_tree: self.on_click_tree,
            ComponentKeys.folder_input: self.on_input_folder,
            ComponentKeys.graph_range_update: self.on_click_update_graph_range,
            ComponentKeys.graph_range_reset: self.on_click_reset_graph_range,
            ComponentKeys.baselines_update: self.on_click_update_baselines,
        }

    def start_event_loop(self) -> None:
        """イベントループを発生させる"""
        while True:
            event, self.values = self.window.read()  # type: ignore

            if event is None:
                break

            else:
                self.events[event]()

    def close_window(self) -> None:
        """ウィンドを閉じる。"""
        self.window.close()

    def _print_notice(self, *messages: str) -> None:
        """通知をログに表示する

        Args:
            *messages (str): 表示するメッセージの配列
        """
        [self.window[ComponentKeys.log].print(message, t=LOG_TEXT_COLORS["notice"]) for message in messages]  # type: ignore

    def _print_alert(self, *messages: str) -> None:
        """警告をログに表示する

        Args:
            *messages (str): 表示するメッセージの配列
        """
        [self.window[ComponentKeys.log].print(message, t=LOG_TEXT_COLORS["alert"]) for message in messages]  # type: ignore

    def _get_canvas(self) -> tkinter.Canvas:
        """CanvasElement を受け取る"""
        return self.window[ComponentKeys.graph_canvas].TKCanvas  # type: ignore

    def _get_values(self, key: str) -> Any:
        """特定のkeyのvaluesを返す

        Args:
            key (str): コンポーネントのキー

        Returns:
            Any: 取得したvalues
        """
        try:
            return self.values[key]
        except AttributeError:
            print("read_window が実行されていません!")

    def get_selected_csv_headers(self) -> list[str]:
        """選択されたcsvヘッダを取得する

        Returns:
            list[str]: 選択されたcsvヘッダの配列
        """
        return self._get_values(ComponentKeys.csv_headers_listbox)

    def get_input_folder(self) -> str:
        """入力されたフォルダパスを取得する

        Returns:
            str: 入力されたフォルダパス
        """
        return self._get_values(ComponentKeys.folder_input)

    def get_graph_range_values(self, axis: types.GraphAxis) -> tuple[float, float] | None:
        """入力されたグラフの min ~ max レンジを取得する

        Args:
            axis (types.GraphAxis): 対象の軸(x / y)

        Raises:
            ValueError: 入力のバリデーションに失敗した場合

        Returns:
            tuple[float, float] | None: 入力されたグラフの min ~ max レンジ。入力がなければNoneを返す
        """
        min = self._get_values(ComponentKeys.graph_range[axis]["min"])
        max = self._get_values(ComponentKeys.graph_range[axis]["max"])
        # 空白ならNoneを返す
        if min == "" or max == "":
            return None
        # バリデーションに成功したらfloatにキャストして返す
        if utils.validate_graph_min_max_range(min, max):
            return (float(min), float(max))
        # バリデーションに失敗したらエラー
        raise ValueError(f"{axis}軸のレンジに無効な値が含まれています: {min} ~ {max}")

    def get_base_hline_value(self, hline_number: types.HlineNumber) -> float | None:
        """入力された水平線のY座標の値を取得する

        Args:
            hline_number (types.HlineNumber): 対象の規格線の番号

        Returns:
            float | None: 入力された水平線のY座標の値。入力場なければNoneを返す
        """
        hline_value = self._get_values(ComponentKeys.base_hline_input[hline_number])
        if not hline_value == "":
            if utils.validate_input_number(hline_value):
                return float(hline_value)
            else:
                self._print_alert(f"規格線{hline_number}に無効な値が含まれています")

    def _update_time_axis_indicator(self, is_time_axis: bool) -> None:
        """X軸のインジケータを更新する

        Args:
            is_time_axis (bool): 横軸が時間軸か否か
        """
        indicator_text = TIME_AXIS_INDICATOR_TEXTS["y"] if is_time_axis else TIME_AXIS_INDICATOR_TEXTS["n"]
        self.window[ComponentKeys.time_axis_indicator_text].update(indicator_text)  # type: ignore

    def update_graph_canvas(self) -> None:
        """グラフを更新する

        See Also:
            - self.update_both_graph_range()
            - self._update_base_hlines()
            - self.graph.commit_change()
        """
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
                    # X, Y軸プロットの長さが異なる場合、0埋めする
                    # matplotlib の ValueError: x and y must have same first dimension, but have shapes への対応
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
        """CSV選択リストを更新する"""
        self.window[ComponentKeys.csv_headers_listbox].update(values=self.data_store.headers_of_csv_reader)

    # FIXME update x, y を統合する
    def _update_x_range(self) -> None:
        """グラフのX軸のレンジを更新する"""
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
        """グラフのY軸のレンジを更新する"""
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
        """フォルダーツリーに関連するデータをリセットする"""
        self.data_store.update_plots_by_headers([])
        self.data_store.update_plots_by_filepaths([])
        self.update_csv_headers_listbox()
        self.update_graph_canvas()

    def update_both_graph_range(self) -> None:
        """X, Y軸共にレンジを更新する"""
        self._update_x_range()
        self._update_y_range()
        self.graph.commit_change()

    def reset_both_graph_range(self) -> None:
        """X, Y軸共にレンジをリセットする"""
        self.window[ComponentKeys.graph_range["x"]["min"]].update("")  # type: ignore
        self.window[ComponentKeys.graph_range["x"]["max"]].update("")  # type: ignore
        self.window[ComponentKeys.graph_range["y"]["min"]].update("")  # type: ignore
        self.window[ComponentKeys.graph_range["y"]["max"]].update("")  # type: ignore
        # NOTE: input の値をクリア ➞ update_graph_range()でグラフを更新 することは出来ない
        # PySimpleGUI の仕様上、1回のイベントで更新できるコンポーネントは1つしか無いため
        self.graph.auto_scale_x_range()
        self.graph.auto_scale_y_range()
        self.graph.commit_change()

    def _update_base_hlines(self) -> None:
        """水平線を更新する"""
        for hline_num in BASE_HLINE_NUMBERS:
            if hline1_value := self.get_base_hline_value(hline_num):
                self.graph.plot_hline(hline1_value, BASE_HLINE_COLORS[hline_num])
        self.graph.commit_change()

    def on_click_tree(self) -> None:
        """csv_reader, csv_header_listbox, グラフ を更新する処理"""
        filepaths = [i for i in self._get_values(ComponentKeys.explorer_tree) if not utils.is_dir(i)]

        # 何も選ばれていない or ディレクトリだけ選ばれている場合
        if not filepaths:
            self.data_store.update_plots_by_filepaths([])
            return

        try:
            # 存在しないcsvヘッダが選ばれた場合
            self.data_store.update_plots_by_filepaths(filepaths)
        except ValueError:
            self._print_alert("存在しないcsvヘッダが指定されました", "ファイル間に異なるヘッダが含まれないか確認して下さい")
            self.reset_data_referring_to_tree()
            return
        self.update_csv_headers_listbox()
        self.update_graph_canvas()

    def on_select_csv_header(self) -> None:
        """グラフを更新する処理"""
        csv_headers = self.get_selected_csv_headers()
        if not csv_headers:
            self.data_store.update_plots_by_headers([])
            return

        # 存在しないcsvヘッダが選ばれた場合
        try:
            self.data_store.update_plots_by_headers(csv_headers)
        except ValueError:
            self._print_alert("存在しないcsvヘッダが指定されました", "ファイル間に異なるヘッダが含まれないか確認して下さい")
            self.reset_data_referring_to_tree()
            return
        self.update_graph_canvas()

    def on_input_folder(self) -> None:
        """ツリーを更新する処理"""
        tree_data = generate_tree_data("", self.get_input_folder())
        self.window[ComponentKeys.explorer_tree].update(values=tree_data)
        self.reset_data_referring_to_tree()
        self._print_notice("フォルダの読み込みが完了しました")

    def on_click_update_graph_range(self) -> None:
        """グラフのレンジを更新する処理"""
        self.update_both_graph_range()
        self._print_notice("グラフのレンジを更新しました")

    def on_click_reset_graph_range(self) -> None:
        """グラフのレンジをリセットする処理"""
        self.reset_both_graph_range()
        self._print_notice("グラフのレンジをリセットしました")

    def on_click_update_baselines(self) -> None:
        """水平線を更新する処理"""
        # hline の描画だけ呼び出すと無限に描画されてしまう
        # clear を挟むために _update_graph_canvas を呼ぶようにする
        self.update_graph_canvas()
        self._print_notice("規格線を更新しました")
