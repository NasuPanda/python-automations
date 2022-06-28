import arrow


class TimeHelper():
    """
    This class is a helper that offers methods to creating, shifting, and formatting times.

    NOTE:
        This class dependent on arrow (Python library).
        reference: https://arrow.readthedocs.io/en/latest

    Class variables
    ----------
    FORMATS: dict[str, str]
        The formats used for formatting arrow object.
    LOCAL: "Asia/Tokyo"
        The timezone info used for convert arrow object.

    Example usage
    ----------
        current = TimeHelper.current()
        # example: next day, at N (Today), N hours from now...
        finish = TimeHelper.shift_hours(current, 8)
        time_helper = TimeHelper(start=current, shift_step_min=15)

        # Finish if current == finish
        while (
            TimeHelper.get_hour_and_min(TimeHelper.current()) !=
            TimeHelper.get_hour_and_min(finish)
        ):
            next_shift = time_helper.next_shift()
            while (
                TimeHelper.get_hour_and_min(TimeHelper.current()) !=
                TimeHelper.get_hour_and_min(next_shift))
            ):
                # Do something
    """

    FORMATS = {
        "short": "MM-DD HH:mm",
        "long": "YYYY-MM-DD HH:mm:ss ZZ"
    }
    LOCAL = "Asia/Tokyo"

    def __init__(self, start: arrow.arrow.Arrow, shift_step_min: int) -> None:
        """Initialize an instance.

        Parameters
        ----------
        start : arrow.arrow.Arrow
            Start time. (for initialize time_shifter)
        shift_step_min : int
            Shift step. (minute)
        """
        self.time_shifter = self.iter_time_shifter(start, shift_step_min)

    def next_shift(self) -> arrow.arrow.Arrow:
        """Get next shift.

        Returns
        -------
        arrow.arrow.Arrow
            Next time step.
        """
        return self.time_shifter.__next__()

    @classmethod
    def shift_minutes(cls, current: arrow.arrow.Arrow, min: int) -> arrow.arrow.Arrow:
        """Get shifted time. (minute)

        Parameters
        ----------
        current : arrow.arrow.Arrow
            Current time.
        min : int
            Shift step. (minute)
            If negative, shifts negative.

        Returns
        -------
        arrow.arrow.Arrow
            Shifted time.
        """
        return current.shift(minutes=min)

    @classmethod
    def shift_hours(cls, current: arrow.arrow.Arrow, hour: int) -> arrow.arrow.Arrow:
        """Get shifted time. (hour)

        Parameters
        ----------
        current : arrow.arrow.Arrow
            Current time.
        min : int
            Shift step. (hour)
            If negative, shifts negative.

        Returns
        -------
        arrow.arrow.Arrow
            Shifted time.
        """
        return current.shift(hours=hour)

    @classmethod
    def format(cls, time: arrow.arrow.Arrow, format="short") -> str:
        """Format time.

        Parameters
        ----------
        time : arrow.arrow.Arrow
            Target time object.
        format : str, optional
            Format to use (defined cls.FORMATS) , by default "short"

        Returns
        -------
        str
            Formatted time.
        """
        return time.format(cls.FORMATS[format])

    @classmethod
    def get_hour_and_min(cls, time: arrow.arrow.Arrow) -> tuple[int, int]:
        """Get hour and minute from Arrow object.

        Parameters
        ----------
        time : arrow.arrow.Arrow
            Target time object.

        Returns
        -------
        tuple[int, int]
            Hour and minute.
        """
        return time.hour, time.minute

    @classmethod
    def current(cls) -> arrow.arrow.Arrow:
        """Get current time. (local time zone)

        Returns
        -------
        arrow.arrow.Arrow
            Current time.
        """
        return arrow.utcnow().to(cls.LOCAL)

    @classmethod
    def iter_time_shifter(cls, start: arrow.arrow.Arrow, shift_step_min: int) -> arrow.arrow.Arrow:
        """Time shift generator.

        Parameters
        ----------
        start : arrow.arrow.Arrow
            Start time.
        shift_step_min : int
            Shift step. (minute)

        Yields
        ------
        arrow.arrow.Arrow
            Time shift generator.
        """
        current = start
        while True:
            current = cls.shift_minutes(current, shift_step_min)
            yield current
