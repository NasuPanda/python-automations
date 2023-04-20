import pandas as pd

from utils.exceptions import InitializeError


class LogReader():
    """Log Reader class.
    """
    def __init__(
        self,
        df: pd.DataFrame | None = None,
        csv_path: str | None = None,
        date_column: str | int = "日付"
    ) -> None:
        """Initialize an instance.
        NOTE
        - Optional arguments df or csv_path is required.
        - Read data as a time-series data.

        Parameters
        ----------
        df : pd.DataFrame | None, optional
            pd.DataFrame instance, by default None
        csv_path : str | None, optional
            CSV path, by default None
        date_column : str | int, optional
            date column name or index, by default "日付"

        Raises
        ------
        InitializeError
            Failure to initialize an instance.
        """
        if df:
            # Set datetime column to index
            df[date_column] = pd.to_datetime(df[date_column])
            df.set_index(date_column, inplace=True)
            df = df
        elif csv_path:
            self.df: pd.DataFrame = pd.read_csv(csv_path, index_col=date_column, parse_dates=True)
        else:
            raise InitializeError("Does't receive valid arguments")
        self.headers: list[str] = self.df.columns.values.tolist()

    def extract_df_by_time_series(self, location: str) -> pd.DataFrame | pd.Series | None:
        """Extracts data frame by time-series location.

        Parameters
        ----------
        location : str
            time-series location.

        Returns
        -------
        pd.DataFrame | pd.Series | None
            Extracted data frame. If doesn't exist, returns None.
        """
        try:
            return self.df.loc[location]
        except KeyError:
            return

    def extract_series_by_header(self, column: str) -> pd.Series | None:
        """Find pd.Series has specific column. If nothing is find, returns None.

        Parameters
        ----------
        column : str
            Column name to be found.

        Returns
        -------
        pd.Series | None
            Found series. If nothing is find, returns None.
        """
        try:
            return self.df[column]
        except KeyError:
            return
