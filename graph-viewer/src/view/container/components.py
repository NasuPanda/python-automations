import os
import tkinter
from typing import Any

import PySimpleGUI as sg

from src.constants import FILE_ICON, FOLDER_ICON, ComponentKeys
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
        self.data_store = DataStore(self._get_canvas())

        self.events = {
            ComponentKeys.csv_headers_listbox: self.on_select_csv_header,
            ComponentKeys.explorer_tree: self.on_click_tree,
            ComponentKeys.folder_input: self.on_input_folder,
        }

    def read_window(self) -> None:
        """イベントループを発生させる。"""
        while True:
            event, self.values = self.window.read()

            if event is None:
                break

            else:
                self.events[event]()

    def _get_canvas(self) -> tkinter.Canvas:
        """private Canvas を受け取る。"""
        return self.window[ComponentKeys.graph_canvas].TKCanvas  # type: ignore

    def _get_csv_headers(self) -> list[str]:
        """選択されたcsvヘッダを返す。(リスト形式なので注意)

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

    def _update_graph_canvas(self) -> None:
        """グラフを更新する。"""
        self.data_store.clear_graph()

        for csv_header in self._get_csv_headers():
            if csv_header:
                data_list = self.data_store.get_column_values_from_csv_readers(csv_header)
                [self.data_store.plot_graph(data) for data in data_list]

        self.data_store.update_graph()

    def on_click_tree(self) -> None:
        """csv_reader, csv_header_listbox, グラフ を更新する処理。"""
        tree_selected_values = self._get_values(ComponentKeys.explorer_tree)
        if not tree_selected_values:
            return

        # イベント発生時に選択されいてるファイルが減ることもあるので、 csv_readers をクリアしておく
        self.data_store.clear_csv_readers()
        # 選択されたのがファイルであれば csv_reader を更新する
        for filepath in tree_selected_values:
            if not os.path.isdir(filepath):
                reader = self.data_store.add_csv_reader(filepath)

        # reader が undefined の場合はキャッチし終了
        try:
            self.window[ComponentKeys.csv_headers_listbox].update(values=reader.columns)
        except NameError:
            return

        self._update_graph_canvas()

    def on_select_csv_header(self) -> None:
        """グラフを更新する処理。"""
        self._update_graph_canvas()

    def on_input_folder(self) -> None:
        """ツリーを更新する処理。"""
        tree_data = generate_tree_data("", self._get_folder_input())
        self.window[ComponentKeys.explorer_tree].update(values=tree_data)
