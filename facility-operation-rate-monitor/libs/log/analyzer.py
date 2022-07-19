import pandas as pd

from libs import timehelper


class LogAnalyzer():
    """Log analyzer class.
    """
    DATE_COLUMN = "日付"
    TIME_COLUMN = "時刻"
    MAN_HOUR_COLUMN = "実作業有無"
    MACHINE_TIME_COLUMN = "マシンタイム"

    def __init__(self, df: pd.DataFrame) -> None:
        """Initialize an instance.

        Parameters
        ----------
        df : pd.DataFrame
            pd.DataFrame instance.

        See also
        ----------
        Gets df from log.reader.LogReader
        """
        self.df = df
        self.df_length = len(df)
        self.man_hour_min: int = 0
        self.machine_time_min: int = 0

    def perform(self) -> None:
        """Calculate time delta whole df, and reflects time delta to instance variables.
        """
        # i, j = (0, 1), (1, 2), (2, 3), ...
        for i, j in zip(range(self.df_length), range(1, self.df_length)):
            # Calculate time delta (min)
            from_time_series, to_time_series = self.df.iloc[i], self.df.iloc[j]
            time_delta_min = timehelper.calculate_time_delta_as_min(
                self.__time_str_to_dict(from_time_series[self.TIME_COLUMN]),
                self.__time_str_to_dict(to_time_series[self.TIME_COLUMN])
            )
            # Reflects time_delta_min to instance variables according to flags.
            if to_time_series[self.MAN_HOUR_COLUMN]:
                self.man_hour_min += time_delta_min
            elif to_time_series[self.machine_time_min]:
                self.machine_time_min += time_delta_min

    @classmethod
    def __time_str_to_dict(cls, time: str) -> dict[str, int]:
        """Time string to dictionary.

        Parameters
        ----------
        time : str
            Time strings.

            format: hh:mm
            ex: 08:00, 12:30, ...

        Returns
        -------
        dict[str, int]
            Time dict.

            format: {"hour": hour(int), "minute": minute(int)}
            ex: {"hour": 8, "minute": 0}
        """
        return {
            "hour": int(time[:2]),
            "minute": int(time[3:])
        }
