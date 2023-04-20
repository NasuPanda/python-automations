import psutil


class SystemPerformanceMonitor():
    """System performance Monitor.

    - To monitor performance like CPU usage, memory...
    - CPU usage is in percent.

    NOTE:
        This class dependent on psutil.
        reference: https://psutil.readthedocs.io/en/latest

    Instance variables
    ----------
    max_cpu_usage: int
        Max CPU usage.
    cpu_usages_to_get_ave: list[float]
        CPU usage array to get an average of cpu usage.
    max_memory_usage: int
        Max memory usage.
    memory_usages_to_get_ave: list[float]
        Memory usage array to get an average of memory usage.
    """
    def __init__(self) -> None:
        """Initialize an instance.
        """
        # CPU usage [%]
        self.max_cpu_usage: float = 0.0
        self.cpu_usages_to_get_ave: list[float] = []
        # memory usage [%]
        self.max_memory_usage: float = 0.0
        self.memory_usages_to_get_ave: list[float] = []

    def cpu_usage_average(self) -> float:
        """Return a cpu usage (%) average value.

        Returns
        -------
        float
            CPU usage (%) average.
        """
        return float(
            sum(self.cpu_usages_to_get_ave) / len(self.cpu_usages_to_get_ave)
        )

    def memory_usage_average(self) -> float:
        """Return a memory usage (%) average value.

        Returns
        -------
        float
            memory usage (%) average.
        """
        return float(
            sum(self.memory_usages_to_get_ave) / len(self.memory_usages_to_get_ave)
        )

    def reset(self):
        """Reset instance variable for monitoring CPU usage.
        """
        self.cpu_usages_to_get_ave = []
        self.max_cpu_usage = 0.0
        self.memory_usages_to_get_ave = []
        self.max_memory_usage = 0.0

    def add_current_cpu_usage_to_cpu_usages(self):
        """Add current CPU usage to cpu usages to get average.
        """
        self.cpu_usages_to_get_ave.append(self.__current_cpu_usage_as_percentage())

    def update_max_cpu_usage_if_needed(self):
        """Update max CPU usage if current max CPU usage < current cpu usage.
        """
        current_cpu_usage = self.__current_cpu_usage_as_percentage()
        if self.max_cpu_usage < current_cpu_usage:
            self.max_cpu_usage = current_cpu_usage

    def add_current_memory_usage_to_memory_usages(self):
        """Add current memory usage to memory usages to get average.
        """
        self.memory_usages_to_get_ave.append(self.__current_memory_usage_as_percentage())

    def update_max_memory_usage_if_needed(self):
        """Update max memory usage if current max memory usage < current memory usage.
        """
        current_memory_usage = self.__current_memory_usage_as_percentage()
        if self.max_memory_usage < current_memory_usage:
            self.max_memory_usage = current_memory_usage

    @classmethod
    def __current_cpu_usage_as_percentage(cls, interval: int | None = 1) -> float:
        """Return a float representing the current system-wide CPU usage as a percentage.

        Parameters
        ----------
        interval : int | None, optional
            Interval of cpu monitoring, by default 1

        Returns
        -------
        float
            Current system-wide CPU usage.
        """
        # NOTE: interval=Noneにすると、連続して呼び出した際に望まない挙動(0.0を返し続ける)をするので注意
        # 参考 : https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        return psutil.cpu_percent(interval)

    @classmethod
    def __current_memory_usage_as_percentage(cls) -> float:
        """Return a float representing the current system-wide memory usage as a percentage.

        Returns
        -------
        float
            Current system-wide memory usage.
        """
        # 参考 : https://psutil.readthedocs.io/en/latest/#psutil.virtual_memory
        return psutil.virtual_memory().percent
