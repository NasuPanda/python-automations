import csv
import pathlib

from config import config
from libs import timehelper


class LogRow():
    def __init__(self, has_received_input: bool, has_process_been_executed: bool, active_window_title: str) -> None:
        """Initialize an instance.

        Parameters
        ----------
        has_received_input : bool
            A flag indicating man-hour status.
        has_process_been_executed : bool
            A flag indicating machine time status.
            If process has been executed, this flag is True.
        """
        self.date_column: str = self.__date_column()
        self.time_column: str = self.__time_column()
        self.man_hour_column: int = self.__man_hour_column(has_received_input)
        self.machine_time_column: int = self.__machine_time_column(has_process_been_executed)
        self.active_window_title: str = active_window_title

    @property
    def data_row_as_dict(self):
        """Returns csv log data row as a dictionary format.

        Returns
        -------
        dict[str, str | int]
            CSV data row tailored to CSVDictWriter.
        """
        return {
            config.CSV_COLUMNS["date"]: self.date_column,
            config.CSV_COLUMNS["time"]: self.time_column,
            config.CSV_COLUMNS["man-hour"]: self.man_hour_column,
            config.CSV_COLUMNS["machine_time"]: self.machine_time_column,
            config.CSV_COLUMNS["active_window_title"]: self.active_window_title,
        }

    def __date_column(self) -> str:
        """Date column in csv log.

        Returns
        -------
        str
            Date column value.
        """
        return timehelper.format(timehelper.current(), "normal")


    def __time_column(self) -> str:
        """Time column in csv log.

        Returns
        -------
        str
            Time column value.
        """
        return timehelper.format(timehelper.current(), "short_time")

    def __man_hour_column(self, has_received_input: bool) -> int:
        """Man-hour status column in csv log.

        Parameters
        ----------
        has_received_input: bool
            A flag indicating man-hour status.

        Returns
        -------
        int
            Man-hour status column value.
            running: 1, sleeping: 0.
        """
        return int(has_received_input)

    def __machine_time_column(self, has_process_been_executed: bool):
        """Machine time status column in csv log.
        NOTE: If man-hour column is 1(running status), this colum is absolutely 0.

        Parameters
        ----------
        has_process_been_executed : bool
            A flag indicating machine time status.

        Returns
        -------
        int
            Machine time status column value.
            running: 1, sleeping: 0.
        """
        if self.man_hour_column:
            return 0
        return int(has_process_been_executed)


class Logger():
    def __init__(self, log_filepath: str = config.LOG_FILE_PATH) -> None:
        """Initialize an instance.

        Parameters
        ----------
        log_filepath : str, optional
            Log file path, by default config.LOG_FILE_PATH
        """
        self.log_filepath: str = log_filepath
        self.headers: list = list(config.CSV_COLUMNS.values())

    def write_log(self, has_received_input: bool, has_process_been_executed: bool, active_window_title: str):
        """Write log to log file.

        Parameters
        ----------
        has_received_input : bool
            A flag indicating man-hour status.
        has_process_been_executed : bool
            A flag indicating machine time status.
            If process has been executed, this flag is True.
        """
        self.__create_log_file_if_needed()
        log = self.__create_log_row(has_received_input, has_process_been_executed, active_window_title)

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
    def __create_log_row(cls, has_received_input: bool, has_process_been_executed: bool, active_window_title: str) -> LogRow:
        """Create log row.

        Parameters
        ----------
        has_received_input : bool
            A flag indicating man-hour status.
        has_process_been_executed : bool
            A flag indicating machine time status.
            If process has been executed, this flag is True.

        Returns
        -------
        LogRow
            Created LogRow instance.
        """
        return LogRow(has_received_input, has_process_been_executed, active_window_title)
