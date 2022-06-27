from typing import TypedDict

import pathlib

import win32com.client
import openpyxl as xl
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

import config
from src.models.excel.graph import Graph


class ExcelAccessor():
    """Excelに対する読み書き操作をするクラス。

    NOTE:
    openpyxlのrow, column index は 1からスタートする。

    NOTE:
    数式の評価が必要な場合, load時のdata_only=Trueのみでは不十分。
    Excelクライアントにより開いた時に初めて式が評価, 値が保存されるため。
    win32com.clientを用いて openpyxl.save → Excelクライアントで開いてから保存することで対処可能。
    """
    def __init__(self, excel_path: str | pathlib.Path, data_only=False) -> None:
        # data_onlyがTrueだと数式を読む事が出来る
        self.wb: Workbook = xl.load_workbook(excel_path, data_only=data_only)
        self.ws: Worksheet = self.wb.worksheets[0]
        self.excel_path: str = str(pathlib.Path(excel_path).resolve())

    @property
    def sheet_size(self):
        return len(self.wb.worksheets)

    @property
    def current_sheet_title(self):
        return self.ws.title

    def reload(self, data_only=False):
        self.wb: Workbook = xl.load_workbook(self.excel_path, data_only=data_only)

    def save_as(self, excel_path: str, needs_evaluate=False):
        if not excel_path[-5:] == ".xlsx":
            excel_path += ".xlsx"

        self.wb.save(excel_path)

        if needs_evaluate:
            self.__evaluate(excel_path)

    def overwrite(self, needs_evaluate=False):
        self.wb.save(self.excel_path)

        if needs_evaluate:
            self.__evaluate(self.excel_path)

    def __evaluate(self, excel_path: str):
        # NOTE: 数式の評価が必要な場合は上書き保存する
        app = win32com.client.Dispatch("Excel.Application")
        app.Visible = False
        app.DisplayAlerts = False
        # 相対パスを解釈してくれないのでresolve()しておく
        wb = app.Workbooks.Open(str(pathlib.Path(excel_path).resolve()))
        wb.Save()
        app.Quit()

    def change_active_worksheet(self, sheet_title=None, sheet_index=None):
        if sheet_title:
            self.ws = self.wb[sheet_title]
        # if sheet_index は sheet_indexが 0 の時にfalseになるため注意
        if sheet_index is not None:
            self.ws = self.wb.worksheets[sheet_index]

    def add_sheet(self, sheet_title: str):
        self.wb.create_sheet(title=sheet_title)
        return sheet_title

    def copy_worksheet(
        self,
        to_sheet_title: str,
        from_sheet_title=None,
        from_sheet_index=None,
        change_active_sheet=False,
    ):
        if from_sheet_title:
            ws = self.wb[from_sheet_title]  # type: ignore
        elif from_sheet_index is not None:
            ws = self.wb.worksheets[from_sheet_index]
        to_ws = self.wb.copy_worksheet(ws)
        to_ws.title = to_sheet_title

        if change_active_sheet:
            self.ws = to_ws

    def add_scatter(self, graph_src: Graph):
        """散布図を追加する。
        references: https://www.shibutan-bloomers.com/python_libraly_openpyxl-11/3439/

        Parameters
        ----------
        graph_src : Graph
            Graph(独自定義のdataclass)クラスのインスタンス。
        """
        chart = ScatterChart()
        chart.width = graph_src.width
        chart.height = graph_src.height
        chart.title = graph_src.title
        chart.x_axis.title = graph_src.x_axis_title
        chart.y_axis.title = graph_src.y_axis_title
        if graph_src.legend is None:
            chart.legend = None
        else:
            chart.legend.position = graph_src.legend

        # データの参照を定義, Chartオブジェクトへ追加
        x_values = Reference(self.ws, **graph_src.x_references.members_as_dict())
        y_values = Reference(self.ws, **graph_src.y_references.members_as_dict())
        series = Series(x_values, y_values)
        chart.series.append(series)

        self.ws.add_chart(chart, graph_src.address)

    def read_cell_value(self, row=1, column=1, address=None):
        if address:
            return self.ws[address].value
        return self.ws.cell(row=row, column=column).value

    def write_cell(self, value: int | float | str, row=1, column=1, address=None):
        if address:
            self.ws[address].value = value
        else:
            self.ws.cell(row=row, column=column, value=value)

    def write_values_in_axial_direction(
        self,
        values: list[int | float | str],
        start_index: int,
        base_axis_index: int,
        axis=0
    ):
        """指定軸方向に値を書き込む
        NOTE: axis: 0 => 横軸, 1 => 縦軸
        """
        # 横方向: to fix row, increment column
        if axis == 0:
            for i, value in enumerate(values):
                self.ws.cell(
                    row=base_axis_index,
                    column=start_index + i,
                    value=value
                )
        # 縦方向: increment row, to fix column
        if axis == 1:
            for i, value in enumerate(values):
                self.ws.cell(
                    row=start_index + i,
                    column=base_axis_index,
                    value=value
                )

    def remove_sheet(self, sheet_index=None, sheet_title=None):
        if sheet_title:
            ws = self.wb[sheet_title]  # type: ignore
        elif sheet_index is not None:
            ws = self.wb.worksheets[sheet_index]
        self.wb.remove(ws)


class IndexAddresses(TypedDict):
    row: int
    column: int


class VIExcelAccessor(ExcelAccessor):
    # NOTE: 辞書として定義しているため ** を使って展開することでそのままメソッドに渡せる
    VALUE_CELL_ADDRESSES = config.EXCEL_VALUE_CELL_ADDRESSES
    DATA_START_ADDRESSES = config.EXCEL_DATA_START_ADDRESSES
    GRAPH = config.EXCEL_VI_GRAPH_CONFIG

    def __init__(self, excel_path: str | pathlib.Path, data_only=True) -> None:
        super().__init__(excel_path, data_only)

    def add_vi_scatter(self):
        self.add_scatter(self.GRAPH)
