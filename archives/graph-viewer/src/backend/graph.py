"""TODO docs の記述
"""
import tkinter
from dataclasses import dataclass

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.common.constants import (
    PLOT_BASELINE_STYLE,
    PLOT_FIGURE_BG_COLOR,
    PLOT_PARAM_FONT,
    PLOT_PARAM_X_MARGIN,
    PLOT_PARAM_Y_MARGIN,
    PLOT_SUBPLOT_POSITION,
)


def draw_figure_to_canvas(canvas_component, figure) -> FigureCanvasTkAgg:
    """PySimpleGUI の cavas と matplotlib の figure を受け取り、描画する"""
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas_component)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


@dataclass
class Metadata:
    data: list
    label: str


class GraphPlotter:
    """
    References
        - https://www.haya-programming.com/entry/2018/10/11/030103
        - 凡例の位置 : https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
        - プロットの余白をグローバルに設定 : https://stackoverflow.com/questions/42668433/matplotlib-globally-set-margins
    """

    def __init__(self, canvas_component: tkinter.Canvas, figure_size: tuple[int, int] = (10, 8)) -> None:
        plt.rcParams["font.family"] = PLOT_PARAM_FONT
        plt.rcParams["axes.xmargin"] = PLOT_PARAM_X_MARGIN
        plt.rcParams["axes.ymargin"] = PLOT_PARAM_Y_MARGIN

        self.fig, self.axes = plt.subplots(figsize=figure_size)
        self.fig.set_facecolor(PLOT_FIGURE_BG_COLOR)
        self.fig.subplots_adjust(**PLOT_SUBPLOT_POSITION)
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

        self.fig.subplots_adjust(**PLOT_SUBPLOT_POSITION)

        self.axes.legend(bbox_to_anchor=(1.00, 1), borderaxespad=0)

    def set_x_range(self, x_range: tuple[float, float]) -> None:
        self.axes.set_xlim([*x_range])  # type: ignore

    def set_y_range(self, y_range: tuple[float, float]) -> None:
        self.axes.set_ylim([*y_range])  # type: ignore

    def auto_scale_x_range(self) -> None:
        self.axes.relim()
        self.axes.autoscale(axis="x")

    def auto_scale_y_range(self) -> None:
        self.axes.relim()
        self.axes.autoscale(axis="y")

    def plot_hline(
        self,
        h_value: int | float,
        color: str = "blue",
        linestyle: str = PLOT_BASELINE_STYLE,
    ) -> None:
        x_min, x_max = self.axes.get_xlim()
        self.axes.hlines([h_value], x_min, x_max, color, linestyles=linestyle)
        self.has_hline = True

    def auto_set_y_tick(self, tick_interval: int = 20):
        min, max = self.axes.get_ylim()
        spacing = (min + max) / tick_interval
        self.axes.yaxis.set_major_locator(ticker.MultipleLocator(spacing))

    def commit_change(self) -> None:
        """グラフにプロットした結果を反映させる。"""
        self.figure_canvas.draw()
