import csv
import pathlib
from dataclasses import dataclass

from config import config
from libs import timehelper


@dataclass
class Log():
    def __init__(self) -> None:
        self.date_column: str = self.__data_column()
        self.time_column: str = self.__time_column()
        self.facility_operation_status_column: int = self.__facility_operation_status_column()

    @property
    def data_row_as_dict(self) -> dict[str, str | int]:
        return {
            config.CSV_COLUMNS["date"]: self.date_column,
            config.CSV_COLUMNS["time"]: self.time_column,
            config.CSV_COLUMNS["facility_operation_status"]: self.facility_operation_status_column,
        }

    def __data_column(self) -> str:
        return timehelper.format(timehelper.current(), "short_date")

    def __time_column(self) -> str:
        return timehelper.format(timehelper.current(), "short_time")

    def __facility_operation_status_column(self, *flags: bool) -> int:
        # TODO キーマウス等の入力を受け取り判定する
        # TODO プロセスの稼働状況を受け取り判定する
        return 0


class Logger():
    def __init__(self, log_filepath: str = config.LOG_FILE_PATH) -> None:
        self.log_filepath: str = log_filepath
        self.headers: list[str] = list(config.CSV_COLUMNS.values())

    def write_log(self):
        self.__create_log_file_if_needed()
        log = self.__new_log()

        with open(self.log_filepath, "a", encoding="utf8", newline="") as f:
            writer = csv.DictWriter(f, self.headers)
            writer.writerow(log.data_row_as_dict)

    def __new_log(self):
        return Log()

    def __create_log_file_if_needed(self):
        if self.__exist_log_file():
            return
        with open(self.log_filepath, "w", encoding="utf8", newline="") as f:
            writer = csv.DictWriter(f, self.headers)
            writer.writeheader()

    def __exist_log_file(self) -> bool:
        return pathlib.Path(self.log_filepath).exists()
