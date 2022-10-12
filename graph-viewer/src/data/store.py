import tkinter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.data.reader import CSVReader
from src.data.graph import Graph


def draw_figure_to_canvas(canvas_component, figure) -> FigureCanvasTkAgg:
    """PySimpleGUI の cavas と matplotlib の figure を受け取り、描画する"""
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas_component)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


class DataStore:
    def __init__(self) -> None:
        self.csv_readers: dict[str, CSVReader] = {}

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
