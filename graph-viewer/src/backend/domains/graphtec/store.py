from src.backend.domains.graphtec._csv import CSVReader
from src.backend.store import DataStore
from src.common.constants import GraphtecMode
from src.common.exception import GraphtecFlagNotFoundError


class GraphtecDataStore(DataStore):
    """
    対象のデータ
    CH20, , WV, TEMP, TC_K, 2000degC, Off, 2000, -200, ﾟC
    測定値
    番号, 日付 時間, ms, CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10, CH11, CH12, CH13, CH14, CH15, CH16, CH17, CH18, CH19, CH20, Alarm1, Alarm2, AlarmOut
    NO., Time, ms, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, A1234567890, A1234567890, A123456789
    1, 2022/9/27 9:55, 0, 137.05, 87.3, 80.55, 96.7, 93.75, 80.5,  BURNOUT,  BURNOUT,  BURNOUT,  BURNOUT, 24.7, 526.7, 512, 723.1, 605.1, 557.4,  BURNOUT,  BURNOUT,  BURNOUT,  BURNOUT, LLLLLLLLLL, LLLLLLLLLL, LLLLLLLLL
    2, 2022/9/27 9:55, 0, 137.35, 87.45, 80.65, 96.9, 93.95, 80.75,  BURNOUT,  BURNOUT,  BURNOUT,  BURNOUT, 24.6, 526.7, 512.2, 723.4, 605.6, 557.7,  BURNOUT,  BURNOUT,  BURNOUT,  BURNOUT, LLLLLLLLLL, LLLLLLLLLL, LLLLLLLLL
    """

    def __init__(self) -> None:
        super().__init__()
        self.csv_readers: dict[str, CSVReader] = {}
        self.measured_value_header_row: int | None = None

    def has_time_axis(self) -> bool:
        # csv が読み込まれていない or ヘッダが選択されていない
        if not self.headers_of_csv_reader or not self.selected_headers:
            return False

        # ヘッダーの中に `time` という文字列が含まれれば次に進む
        # NOTE : 大文字/小文字を区別しないように正規表現を使用
        for header in self.headers_of_csv_reader:
            try:
                GraphtecMode.time_axis_header_regex.findall(header)[0]
                break
            except IndexError:
                pass
        else:
            return False
        return True

    def _set_measured_value_header_row(self, filepath: str) -> None:
        if self.measured_value_header_row is None:
            self.measured_value_header_row = CSVReader.find_row_by_flag(
                filepath, GraphtecMode.measured_value_flag, encoding=GraphtecMode.csv_encoding
            )

    def _add_csv_reader(self, filepath: str) -> None:
        self._set_measured_value_header_row(filepath)
        if not self.measured_value_header_row:
            raise GraphtecFlagNotFoundError(f"{filepath} には {GraphtecMode.measured_value_flag} フラグが存在しません")
        reader = CSVReader(
            filepath,
            self.measured_value_header_row + 1,
            GraphtecMode.na_values,
            GraphtecMode.excluded_columns,
            GraphtecMode.csv_encoding,
        )
        reader.drop_row_by_index(GraphtecMode.excluded_rows)
        self.csv_readers[filepath] = reader
