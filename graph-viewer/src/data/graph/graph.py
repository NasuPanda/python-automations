import tkinter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_figure_to_canvas(canvas_component, figure) -> FigureCanvasTkAgg:
    """PySimpleGUI の cavas と matplotlib の figure を受け取り、描画する"""
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas_component)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


class Graph:
    def __init__(self, canvas_component: tkinter.Canvas, figure_size: tuple[int, int] = (7, 5)) -> None:
        embed_figure = plt.figure(figsize=figure_size)
        self.axes = embed_figure.add_subplot(111)
        self.figure_canvas = draw_figure_to_canvas(canvas_component, embed_figure)

    def clear(self) -> None:
        """グラフをクリアする。"""
        self.axes.cla()
        self.figure_canvas.draw()

    def plot(self, data: list, label: str) -> None:
        """グラフにデータをプロットする。

        Args:
            data (any): axes.plot が受け付けるデータ。
        """
        # FIXME x, y ともに受け取る仕様にする？
        # time[s] を強制的に x軸で固定する、とか。
        self.axes.plot(data, label=label)
        self.axes.legend()

    def commit_change(self) -> None:
        """グラフにプロットした結果を反映させる。"""
        self.figure_canvas.draw()
