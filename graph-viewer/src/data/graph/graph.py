import tkinter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


FIGURE_BG_COLOR = "azure"
SUBPLOT_POSITION = {"left": 0.05, "right": 0.6, "bottom": 0.1, "top": 0.95}


def draw_figure_to_canvas(canvas_component, figure) -> FigureCanvasTkAgg:
    """PySimpleGUI の cavas と matplotlib の figure を受け取り、描画する"""
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas_component)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


class Graph:
    def __init__(self, canvas_component: tkinter.Canvas, figure_size: tuple[int, int] = (12, 10)) -> None:
        self.fig, self.axes = plt.subplots(figsize=figure_size)
        self.fig.set_facecolor(FIGURE_BG_COLOR)
        self.fig.subplots_adjust(**SUBPLOT_POSITION)
        self.figure_canvas = draw_figure_to_canvas(canvas_component, self.fig)

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
        self.fig.subplots_adjust(**SUBPLOT_POSITION)

        # self.axes.legend(loc="upper left")
        self.axes.legend(bbox_to_anchor=(1.00, 1), borderaxespad=0)

    def commit_change(self) -> None:
        """グラフにプロットした結果を反映させる。"""
        self.figure_canvas.draw()
