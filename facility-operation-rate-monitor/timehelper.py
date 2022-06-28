import arrow


class TimeHelper():
    """
    This class is a helper that offers methods to creating, shifting, and formatting times.

    Example Usage:

        current = TimeHelper.current()
        # example: next day, at N (Today), N hours from now...
        finish = TimeHelper.shift_hours(current, 8)
        time_helper = TimeHelper(start=current, shift_step_min=15)

        # finish if current == finish
        while (
            TimeHelper.get_hour_and_min(TimeHelper.current()) !=
            TimeHelper.get_hour_and_min(finish)
        ):
            next_shift = time_helper.next_shift()
            while (
                TimeHelper.get_hour_and_min(TimeHelper.current()) !=
                TimeHelper.get_hour_and_min(next_shift))
            ):
                # do something
    """

    LOCAL = "Asia/Tokyo"

    def __init__(self, start: arrow.arrow.Arrow, shift_step_min: int) -> None:
        """initialize an instance.

        Parameters
        ----------
        start : arrow.arrow.Arrow
            start time. (for initialize time_shifter)
        shift_step_min : int
            shift step. (minute)
        """
        self.time_shifter = self.iter_time_shifter(start, shift_step_min)

    def next_shift(self) -> arrow.arrow.Arrow:
        """get next shift.

        Returns
        -------
        arrow.arrow.Arrow
            next time step.
        """
        return self.time_shifter.__next__()

    @classmethod
    def shift_minutes(cls, current: arrow.arrow.Arrow, min: int) -> arrow.arrow.Arrow:
        """get shifted time. (minute)

        Parameters
        ----------
        current : arrow.arrow.Arrow
            current time.
        min : int
            shift step. (minute)
            if negative, shifts negative.

        Returns
        -------
        arrow.arrow.Arrow
            shifted time.
        """
        return current.shift(minutes=min)

    @classmethod
    def shift_hours(cls, current: arrow.arrow.Arrow, hour: int) -> arrow.arrow.Arrow:
        """get shifted time. (hour)

        Parameters
        ----------
        current : arrow.arrow.Arrow
            current time.
        min : int
            shift step. (hour)
            if negative, shifts negative.

        Returns
        -------
        arrow.arrow.Arrow
            shifted time.
        """
        return current.shift(hours=hour)

    @classmethod
    def get_hour_and_min(cls, current: arrow.arrow.Arrow) -> tuple[int, int]:
        """get hour and minute from Arrow object.

        Parameters
        ----------
        current : arrow.arrow.Arrow
            current time.

        Returns
        -------
        tuple[int, int]
            hour and minute.
        """
        return current.hour, current.minute

    @classmethod
    def current(cls) -> arrow.arrow.Arrow:
        """get current time. (local)

        Returns
        -------
        arrow.arrow.Arrow
            current time.
        """
        return arrow.utcnow().to(cls.LOCAL)

    @classmethod
    def iter_time_shifter(cls, start: arrow.arrow.Arrow, shift_step_min: int) -> arrow.arrow.Arrow:
        """time shift generator.

        Parameters
        ----------
        start : arrow.arrow.Arrow
            start time.
        shift_step_min : int
            shift step. (minute)

        Yields
        ------
        arrow.arrow.Arrow
            time shift generator.
        """
        current = start
        while True:
            current = cls.shift_minutes(current, shift_step_min)
            yield current
