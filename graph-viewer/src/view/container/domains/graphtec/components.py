from src.common import utils
from src.common.exception import GraphtecFlagNotFoundError
from src.data.domains.graphtec.store import GraphtecDataStore
from src.view.container.components import UserInterface
from src.common.constants import ComponentKeys, GraphtecMode


class GraphtecUserInterface(UserInterface):
    def __init__(self, initial_folder: str) -> None:
        super().__init__(initial_folder)
        self.data_store = GraphtecDataStore()

    def _update_time_axis_indicator(self, is_time_axis: bool) -> None:
        """X軸のインジケータを更新する

        Args:
            is_time_axis (bool): 横軸が時間軸か否か
        """
        indicator_text = (
            GraphtecMode.time_axis_indicator_text["y"] if is_time_axis else GraphtecMode.time_axis_indicator_text["n"]
        )
        self.window[ComponentKeys.time_axis_indicator_text].update(indicator_text)  # type: ignore

    def update_graph_canvas(self) -> None:
        """グラフを更新する

        See Also:
            - self.update_both_graph_range()
            - self._update_base_hlines()
            - self.graph.commit_change()
        """
        self.graph.clear()

        # NOTE 時間軸は無視する
        self._update_time_axis_indicator(True)
        [self.graph.plot(y_values=plot.data, label=plot.label) for plot in self.data_store.plots]

        # 毎回実行が必要なメソッド
        # NOTE: Graptecの場合は目盛り幅が潰れてしまうため別途セットする
        self.graph.auto_set_y_tick()
        self.update_both_graph_range()
        self._update_base_hlines()
        self.graph.commit_change()

    def on_click_tree(self) -> None:
        """csv_reader, csv_header_listbox, グラフ を更新する処理"""
        filepaths = [i for i in self._get_values(ComponentKeys.explorer_tree) if not utils.is_dir(i)]

        # 何も選ばれていない or ディレクトリだけ選ばれている場合
        if not filepaths:
            self.data_store.update_plots_by_filepaths([])
            return

        try:
            self.data_store.update_plots_by_filepaths(filepaths)
        # 存在しないcsvヘッダが選ばれた場合
        except GraphtecFlagNotFoundError:
            self._print_alert(f"{GraphtecMode.measured_value_flag}フラグが存在しません")
            self.reset_data_referring_to_tree()
            return
        except UnicodeDecodeError:
            self._print_alert("文字コードエラーが発生しました", "開発者に連絡して下さい")
            self.reset_data_referring_to_tree()
            return
        except ValueError:
            self._print_alert("存在しないcsvヘッダが指定されました", "ファイル間に異なるヘッダが含まれないか確認して下さい")
            self.reset_data_referring_to_tree()
            return
        self.update_csv_headers_listbox()
        self.update_graph_canvas()
