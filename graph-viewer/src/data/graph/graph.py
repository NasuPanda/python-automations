import tkinter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FIGURE_BG_COLOR = "azure"
BASELINE_STYLE = "dashed"
SUBPLOT_POSITION = {"left": 0.05, "right": 0.6, "bottom": 0.1, "top": 0.95}


def draw_figure_to_canvas(canvas_component, figure) -> FigureCanvasTkAgg:
    """PySimpleGUI の cavas と matplotlib の figure を受け取り、描画する"""
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas_component)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


class Graph:
    """
    References
        - https://www.haya-programming.com/entry/2018/10/11/030103
        - https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
    """

    def __init__(self, canvas_component: tkinter.Canvas, figure_size: tuple[int, int] = (10, 8)) -> None:
        self.fig, self.axes = plt.subplots(figsize=figure_size)
        self.fig.set_facecolor(FIGURE_BG_COLOR)
        self.fig.subplots_adjust(**SUBPLOT_POSITION)
        self.figure_canvas = draw_figure_to_canvas(canvas_component, self.fig)

    def clear(self) -> None:
        """グラフをクリアする。"""
        self.axes.cla()
        self.figure_canvas.draw()

    def plot(self, y_values: list, label: str, x_values: list | None = None) -> None:
        """グラフにデータをプロットする。

        Args:
            data (any): axes.plot が受け付けるデータ。
        """
        if x_values:
            self.axes.plot(x_values, y_values, label=label)
        else:
            self.axes.plot(y_values, label=label)

        self.fig.subplots_adjust(**SUBPLOT_POSITION)

        self.axes.legend(bbox_to_anchor=(1.00, 1), borderaxespad=0)

    def set_x_range(self, x_range: tuple[float, float]) -> None:
        self.axes.set_xlim([*x_range])

    def set_y_range(self, y_range: tuple[float, float]) -> None:
        self.axes.set_ylim([*y_range])

    def plot_hline(
        self,
        h_value: int | float,
        color: str = "blue",
        linestyle: str = BASELINE_STYLE,
    ) -> None:
        x_min, x_max = self.axes.get_xlim()
        self.axes.hlines([h_value], x_min, x_max, color, linestyles=linestyle)

    def commit_change(self) -> None:
        """グラフにプロットした結果を反映させる。"""
        self.figure_canvas.draw()
