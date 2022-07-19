"""This module is a helper that offers methods to creating, shifting, and formatting times.

NOTE:
    This module dependent on arrow (Python library).
    reference: https://arrow.readthedocs.io/en/latest

Constants
----------
FORMATS: dict[str, str]
    The formats used for formatting arrow object.
LOCAL: "Asia/Tokyo"
    The timezone info used for convert arrow object.
SAMPLE: arrow.arrow.Arrow
    Arrow instance used to calculate minutes and seconds.

Example usage
----------
    current = timehelper.current()
    # finish example: next day, at N (Today), N hours from now...
    finish = timehelper.shift_hours(current, 8)
    time_shifter = TimeShifter(start=current, shift_step_min=15)

    # Finish if current == finish
    while timehelper.is_faster_than(finish, timehelper.current()):
        next_shift = time_shifter.next_shift()
        while timehelper.is_faster_than(next_shift, timehelper.current()):
            # Do something
"""

import time
import arrow
from arrow.arrow import Arrow

from utils.exceptions import InvalidFormatError

FORMATS = {
    "default": "YYMMDD",
    "short": "YYMMDD",
    "normal": "YYYY-MM-DD",
    "long": "YYYY-MM-DD HH:mm:ss ZZ",
    "short_date": "MM/DD",
    "short_time": "HH:mm",
}
LOCAL = "Asia/Tokyo"
SAMPLE = arrow.get(2000, 1, 1)


def sleep(sleep_time_sec: int):
    """Delay execution for configured time.

    Parameters
    ----------
    sleep_time_sec : int
        sleep time (second).
    """
    time.sleep(sleep_time_sec)


def shift_minutes(current: Arrow, min: int) -> Arrow:
    """Return a shifted time. (minute)

    Parameters
    ----------
    current : Arrow
        Arrow object of current time.
    min : int
        Shift step. (minute)
        If negative, shifts negative.

    Returns
    -------
    Arrow
        Shifted time.
    """
    return current.shift(minutes=min)


def shift_hours(current: Arrow, hour: int) -> Arrow:
    """Return a shifted time. (hour)

    Parameters
    ----------
    current : Arrow
        Arrow object of current time.
    min : int
        Shift step. (hour)
        If negative, shifts negative.

    Returns
    -------
    Arrow
        Shifted time.
    """
    return current.shift(hours=hour)


def calculate_time_delta_as_sec(from_time: dict[str, int], to_time: dict[str, int]) -> int:
    """Returns time delta from from_time to to_time as a second.

    Parameters
    ----------
    from_time : dict[str, int]
        From time dict for kwargs.
    to_time : dict[str, int]
        To time dict kwargs.

    Returns
    -------
    int
        Time delta (second)
    """
    before = SAMPLE.replace(**from_time)
    after = SAMPLE.replace(**to_time)
    time_delta = after - before
    return time_delta.seconds


def calculate_time_delta_as_min(from_time: dict[str, int], to_time: dict[str, int]) -> int:
    """Returns time delta from from_time to to_time as a minute.

    Parameters
    ----------
    from_time : dict[str, int]
        From time dict for kwargs.
    to_time : dict[str, int]
        To time dict for kwargs.

    Returns
    -------
    float
        Time delta (minute)
    """
    return int(calculate_time_delta_as_sec(from_time, to_time) / 60)


def format(time: Arrow, format="default") -> str:
    """To string and format arrow object.

    Parameters
    ----------
    time : Arrow
        Arrow object.
    format : str, optional
        Format to use (defined FORMATS) , by default "default"

    Returns
    -------
    str
        String of formatted time.

    Raises
    ------
    InvalidFormatError
        When receives an invalid format.
    """
    format = FORMATS.get(format)
    if format is None:
        raise InvalidFormatError(f"{format} is invalid format. Expected: {FORMATS}")
    return time.format(format)


def get_hour_and_min_from_arrow(time: Arrow) -> tuple[int, int]:
    """Returns hour and minute from Arrow object.

    Parameters
    ----------
    time : Arrow
        Target time object.

    Returns
    -------
    tuple[int, int]
        Hour and minute.
    """
    return time.hour, time.minute


def is_faster_than(expected_to_be_fast: Arrow, expected_to_be_late: Arrow) -> bool:
    """Return boolean of whether expected_to_be_fast is faster than expected_to_be_late or not.

    Parameters
    ----------
    expected_fast : Arrow
        Arrow object expected to be fast.
    expected_late : Arrow
        Arrow object expected to be late.

    Returns
    -------
    bool
        Boolean of whether expected_to_be_fast is faster than expected_to_be_late or not
    """
    return expected_to_be_fast.timestamp() > expected_to_be_late.timestamp()


def current() -> Arrow:
    """Return an arrow object of current time.
    Note: Return a converted time to local time zone.

    Returns
    -------
    Arrow
        Arrow object of current time.
    """
    return arrow.utcnow().to(LOCAL)


def first_day_of_this_month() -> Arrow:
    """Return an arrow object of first day of this month.
    - Used method: https://arrow.readthedocs.io/en/latest/#ranges-spans

    Returns
    -------
    Arrow
        Arrow object of first day of this month.
    """
    return current().span("month")[0]


def last_day_of_this_month() -> Arrow:
    """Return an arrow object of last day of this month.
    - Used method: https://arrow.readthedocs.io/en/latest/#ranges-spans

    Returns
    -------
    Arrow
        Arrow object of last day of this month.
    """
    return current().span("month")[-1]


class TimeShifter():
    """This class is a time shifter.
    """
    def __init__(self, start: Arrow, shift_step_min: int) -> None:
        """Initialize an instance.

        Parameters
        ----------
        start : Arrow
            Start time. (for initialize time_shifter)
        shift_step_min : int
            Shift step. (minute)
        """
        self.time_shifter = self.iter_time_shifter(start, shift_step_min)

    def next_shift(self) -> Arrow:
        """Return a next shift.

        Returns
        -------
        Arrow
            Next time step.
        """
        return self.time_shifter.__next__()

    @classmethod
    def iter_time_shifter(cls, start: Arrow, shift_step_min: int) -> Arrow:
        """Time shift generator.

        Parameters
        ----------
        start : Arrow
            Start time.
        shift_step_min : int
            Shift step. (minute)

        Yields
        ------
        Arrow
            Time shift generator.
        """
        current = start
        while True:
            current = shift_minutes(current, shift_step_min)
            yield current
