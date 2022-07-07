import csv
import pathlib

from config import config
from libs import timehelper


class LogRow():
    def __init__(self, *flags: bool) -> None:
        """Initialize an instance.

        Parameters
        ----------
        flags: bool
            Flags indicating facility operation status.
        """
        self.date_column: str = self.__date_column()
        self.time_column: str = self.__time_column()
        self.facility_operation_status_column: int = self.__facility_operation_status_column(*flags)

    @property
    def data_row_as_dict(self) -> dict[str, str | int]:
        """Returns csv log data row as a dictionary format.

        Returns
        -------
        dict[str, str | int]
            CSV data row tailored to CSVDictWriter.
        """
        return {
            config.CSV_COLUMNS["date"]: self.date_column,
            config.CSV_COLUMNS["time"]: self.time_column,
            config.CSV_COLUMNS["facility_operation_status"]: self.facility_operation_status_column,
        }

    def __date_column(self) -> str:
        """Date column in csv log.

        Returns
        -------
        str
            Date column value.
        """
        return timehelper.format(timehelper.current(), "short_date")

    def __time_column(self) -> str:
        """Time column in csv log.

        Returns
        -------
        str
            Time column value.
        """
        return timehelper.format(timehelper.current(), "short_time")

    def __facility_operation_status_column(self, *flags: bool) -> int:
        """Facility operation status column in csv log.

        Parameters
        ----------
        flags: bool
            Flags indicating facility operation status.

        Returns
        -------
        int
            Facility operation status column value.
            running: 1, sleeping: 0.
        """
        if any(flags):
            return 1
        return 0


class Logger():
    def __init__(self, log_filepath: str = config.LOG_FILE_PATH) -> None:
        """Initialize an instance.

        Parameters
        ----------
        log_filepath : str, optional
            Log file path, by default config.LOG_FILE_PATH
        """
        self.log_filepath: str = log_filepath
        self.headers: list[str] = list(config.CSV_COLUMNS.values())

    def write_log(self, *flags: bool):
        """Write log to log file.

        Parameters
        ----------
        flags: bool
            Flags indicating facility operation status.
        """
        self.__create_log_file_if_needed()
        log = self.__create_log_row(*flags)

        with open(self.log_filepath, "a", encoding="utf_8_sig", newline="") as f:
            writer = csv.DictWriter(f, self.headers)
            writer.writerow(log.data_row_as_dict)

    def __create_log_file_if_needed(self):
        """Create log file if it doesn't exist.
        """
        if self.__exist_log_file():
            return
        with open(self.log_filepath, "w", encoding="utf_8_sig", newline="") as f:
            writer = csv.DictWriter(f, self.headers)
            writer.writeheader()

    def __exist_log_file(self) -> bool:
        """Returns a boolean of existence of log file.

        Returns
        -------
        bool
            Exists log file.
        """
        return pathlib.Path(self.log_filepath).exists()

    @classmethod
    def __create_log_row(cls, *flags: bool) -> LogRow:
        """Create log row.

        Parameters
        ----------
        flags: bool
            Flags indicating facility operation status.

        Returns
        -------
        LogRow
            Created LogRow instance.
        """
        return LogRow(*flags)
