"""ドメインに依存する処理を切り出すためのモジュール。
"""

import pathlib

import config
from src.models.parser import ParParser
from src.models.excel.accessor import VIExcelAccessor
from src.models.vi import VIData
from src.utils.helper import CSVReader
from src.utils import helper as Helper


class ExtractVIDataFromParEngine():
    """parファイルをparseしてVIデータを取り出す処理
    """
    def __init__(self, experiment_mode: str) -> None:
        """インスタンスの初期化

        Parameters
        ----------
        experiment_mode : str
            試験モード
        """
        self.default_voltage_range = config.VOLTAGE_DEFAULT_RANGE[experiment_mode]

    def perform(self, par_path: pathlib.Path, data_name: str) -> VIData:
        """処理の実行

        Parameters
        ----------
        par_path : pathlib.Path
            .parファイルのPathオブジェクト
        data_name : str
            データ名

        Returns
        -------
        VIData
            .parファイルから取り出したVIデータ。
        """
        csv_dst_path = self.par_to_csv(par_path)
        vi_data = self.extract_vi_data_from_csv_file(csv_dst_path, data_name)
        vi_data.update_resistance()
        return vi_data

    def par_to_csv(self, par_path: pathlib.Path) -> pathlib.Path:
        """.par => .csv

        Parameters
        ----------
        par_path : pathlib.Path
            .parファイルのPathオブジェクト

        Returns
        -------
        str
            パース後の.csvファイルのPathオブジェクト。
        """
        csv_dst_path = Helper.resolve_relative_path(f"{config.CSV_DST_PATH}/{par_path.stem}.csv")
        ParParser.parse_par_to_csv(str(par_path), str(csv_dst_path))
        return csv_dst_path  # type: ignore

    def extract_vi_data_from_csv_file(self, csv_path: str | pathlib.Path, data_name: str) -> VIData:
        """csv から VIデータを取り出す

        Parameters
        ----------
        csv_path : str | pathlib.Path
            CSVファイルのパス。
        data_name : str
            データ名。

        Returns
        -------
        VIData
            VIデータ。
        """
        reader = CSVReader(str(csv_path))

        vi_data = VIData(
            data_name=data_name,
            times=reader.get_column_values(reader.headers[config.PAR_TIME_COLUMN_INDEX]),
            currents=reader.get_column_values(reader.headers[config.PAR_CURRENT_COLUMN_INDEX]),
            voltages=reader.get_column_values(reader.headers[config.PAR_VOLTAGE_COLUMN_INDEX]),
            min_voltage=self.default_voltage_range[0],
            max_voltage=self.default_voltage_range[1],
            resistance=0
        )
        return vi_data


class WriteVIDataToExcelEngine():
    """VIデータをExcelに書き込む処理。
    """
    def __init__(self, to_excel_name: str) -> None:
        """インスタンスの初期化

        Parameters
        ----------
        to_excel_name : str
            出力先のExcelファイル名。
        """
        format_excel_path = config.EXCEL_FORMAT_PATH
        self.writer = VIExcelAccessor(format_excel_path, data_only=False)
        self.to_excel_path = Helper.resolve_relative_path(
            f"{config.EXCEL_DST_PATH}/{to_excel_name}",
            needs_cast_str=True
        )

    def perform(self, vi_data_array: list[VIData]):
        """処理の実行

        Parameters
        ----------
        vi_data_array : list[VIData]
            VIデータの配列
        """
        # 各要素に対して実行
        [self.perform_singly(vi_data) for vi_data in vi_data_array]

        # 最初のシートは削除しておく(template用シートのため)
        self.writer.remove_sheet(sheet_index=0)
        self.writer.save_as(str(self.to_excel_path))

    def perform_singly(self, vi_data: VIData):
        """処理の実行(1回)

        Parameters
        ----------
        vi_data : VIData
            VIデータ
        """
        self.writer.copy_worksheet(to_sheet_title=vi_data.data_name, from_sheet_index=0, change_active_sheet=True)

        # 電圧, 電流, 時間の書き込み
        keys = self.writer.DATA_START_ADDRESSES.keys()
        data_values = [vi_data.voltages, vi_data.currents, vi_data.times]
        for key, values in zip(keys, data_values):
            self.writer.write_values_in_axial_direction(
                values=values,
                start_index=self.writer.DATA_START_ADDRESSES[key]["row"],
                base_axis_index=self.writer.DATA_START_ADDRESSES[key]["column"],
                axis=0
            )
        # 開始電圧, 終了電圧の書き込み
        self.writer.write_cell(value=vi_data.min_voltage, address=self.writer.VALUE_CELL_ADDRESSES["min_voltage"])
        self.writer.write_cell(value=vi_data.max_voltage, address=self.writer.VALUE_CELL_ADDRESSES["max_voltage"])
        # グラフ追加
        self.writer.add_vi_scatter()
