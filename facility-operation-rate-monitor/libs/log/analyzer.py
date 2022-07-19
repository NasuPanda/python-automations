import pandas as pd

from libs import timehelper


class LogAnalyzer():
    """Log analyzer class.
    """
    DATE_COLUMN = "日付"
    TIME_COLUMN = "時刻"
    MAN_HOUR_COLUMN = "実作業有無"
    MACHINE_TIME_COLUMN = "マシンタイム"

    @classmethod
    def perform(cls, df: pd.DataFrame) -> tuple[int, int]:
        """Calculate time delta whole df, and reflects time delta to instance variables.

        Parameters
        ----------
        df : pd.DataFrame
            pd.DataFrame instance.

        Returns
        -------
        tuple[int, int]
            man_hour_min, machine_time_min
        """
        df_length = len(df)
        man_hour_min = machine_time_min = 0

        # i, j = (0, 1), (1, 2), (2, 3), ...
        for i, j in zip(range(df_length), range(1, df_length)):
            # Calculate time delta (min)
            from_time_series, to_time_series = df.iloc[i], df.iloc[j]
            time_delta_min = timehelper.calculate_time_delta_as_min(
                cls.__time_str_to_dict(from_time_series[cls.TIME_COLUMN]),
                cls.__time_str_to_dict(to_time_series[cls.TIME_COLUMN])
            )
            # Reflects time_delta_min to instance variables according to flags.
            if to_time_series[cls.MAN_HOUR_COLUMN]:
                man_hour_min += time_delta_min
            elif to_time_series[cls.MACHINE_TIME_COLUMN]:
                machine_time_min += time_delta_min

        return man_hour_min, machine_time_min

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
