import tkinter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.data.reader import CSVReader


def draw_figure_to_canvas(canvas_component, figure) -> FigureCanvasTkAgg:
    """PySimpleGUI の cavas と matplotlib の figure を受け取り、描画する"""
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas_component)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


class DataStore:
    def __init__(self, canvas_component: tkinter.Canvas, figure_size: tuple[int, int] = (7, 5)) -> None:
        embed_figure = plt.figure(figsize=figure_size)
        self.axes = embed_figure.add_subplot(111)
        self.figure_canvas = draw_figure_to_canvas(canvas_component, embed_figure)
        self.csv_readers: dict[str, CSVReader] = {}

    def clear_graph(self) -> None:
        """グラフをクリアする。"""
        self.axes.cla()
        self.figure_canvas.draw()

    def plot_graph(self, data) -> None:
        """グラフにデータをプロットする。

        Args:
            data (any): axes.plot が受け付けるデータ。
        """
        # FIXME x, y ともに受け取る仕様にする？
        # time[s] を強制的に x軸で固定する、とか。
        self.axes.plot(data)

    def update_graph(self) -> None:
        """グラフにプロットした結果を反映させる。"""
        self.figure_canvas.draw()

    def add_csv_reader(self, filepath: str) -> CSVReader:
        """csv_reader を追加する。"""
        reader = CSVReader(filepath)
        self.csv_readers[filepath] = reader
        return reader

    def get_headers_from_csv_reader(self, filepath: str) -> list[str]:
        """csv_reader から headers を取得する"""
        return self.csv_readers[filepath].columns

    def get_column_values_from_csv_reader(self, filepath: str, column_name: str) -> list[int | float] | None:
        """column の値を取得する"""
        return self.csv_readers[filepath].get_column_values(column_name)

    def get_column_values_from_csv_readers(self, column_name: str) -> list[list[int | float]]:
        """登録されている全ての csv_reader から column の値を取得する"""
        result = []
        [result.append(reader.get_column_values(column_name)) for reader in self.csv_readers.values()]
        return result

    def clear_csv_readers(self) -> None:
        """登録されている全ての csv_reader をクリアする。"""
        self.csv_readers = {}
