import psutil

from config import config
from utils.exceptions import ReadOnlyError, ProcessTooManyError, InitializerError


class Process():
    def __init__(self, process: psutil.Process) -> None:
        """Initialize an instance.

        Parameters
        ----------
        process : psutil.Process
            psutil.Process instance.
        """
        self.process: psutil.Process = process
        self.__name: str = process.name()
        self.__pid: int = process.pid
        self.max_cpu_usage: float = 0.0

    @property
    def name(self) -> str:
        """Process name (read only).

        Returns
        -------
        str
            Process name.
        """
        return self.__name

    @property
    def pid(self) -> int:
        """Process id (read only).

        Returns
        -------
        int
            Process id.
        """
        return self.__pid

    @name.setter
    def name(self, __):
        """Read only property setter. Always raise error.

        Raises
        ------
        ReadOnlyError
            When attempting to change the value of a read-only property.
        """
        raise ReadOnlyError("name is read-only property.")

    @pid.setter
    def pid(self, __):
        """Read only property setter. Always raise error.

        Raises
        ------
        ReadOnlyError
            When attempting to change the value of a read-only property.
        """
        raise ReadOnlyError("pid is read-only property.")

    def cpu_usage(self, interval: int = 1) -> float:
        """Current CPU usage.
        reference: https://psutil.readthedocs.io/en/latest/#psutil.Process.cpu_percent

        Parameters
        ----------
        interval : int, optional
            Argument of Process.cpu_percent method, by default 1

        Returns
        -------
        float
            CPU usage. (%)
        """
        return self.process.cpu_percent(interval)

    def update_max_cpu_usage_if_needed(self):
        """Update max CPU usage if current max CPU usage < current cpu usage.
        """
        current_cpu_usage = self.cpu_usage()
        if self.max_cpu_usage < current_cpu_usage:
            self.max_cpu_usage = current_cpu_usage

    @classmethod
    def pid_exists(cls, pid: int) -> bool:
        """Check whether the given PID exists in the current process list.

        Parameters
        ----------
        pid : int
            Process id.

        Returns
        -------
        bool
            Boolean of whether the given PID exists in the current process list or not.
        """
        return psutil.pid_exists(pid)

    @classmethod
    def find_process_by_name(cls, process_name: str) -> psutil.Process | None:
        """Find process by name.

        Parameters
        ----------
        process_name : str
            Process name.

        Returns
        -------
        psutil.Process | None
            psutil.Process instance.

        Raises
        ------
        ProcessTooManyError
            When there are two or more process with same name.
        """
        # https://psutil.readthedocs.io/en/latest/#find-process-by-name
        processes = []
        for process in psutil.process_iter(['name']):
            if process.name() == process_name:
                processes.append(process)

        if len(processes) > 1:
            raise ProcessTooManyError(
                "Two or more processes were found. Only supported process with unique name."
            )
        if not processes:
            return
        return processes[0]


class ProcessesMonitor():
    def __init__(
        self,
        monitored_process_names: list[str] | None = config.MONITORED_PROCESSES,
        cpu_usage_thresholds: list[float] | None = config.CPU_USAGE_THRESHOLDS,
    ) -> None:
        """Initialize an instance.

        Parameters
        ----------
        monitored_process_names : list[str] | None, optional
            Monitored process names, by default config.MONITORED_PROCESSES
        cpu_thresholds : list[float] | None, optional
            Thresholds of cpu usage to judge that process has been executed, by default config.CPU_USAGE_THRESHOLDS
            FIXME: I don't like this variable name.

        Raises
        ------
        InitializerError
            When receives invalid arguments.
        """
        if monitored_process_names is None or cpu_usage_thresholds is None:
            raise InitializerError("ProcessMonitor initializer received invalid arguments.")

        self.has_process_been_executed: bool = False
        self.monitored_process_names: list[str] = monitored_process_names
        self.monitored_processes: dict[str, Process | None] = {}
        self.cpu_thresholds: dict[str, float] = {}

        # Append process name and threshold
        for process_name, threshold in zip(monitored_process_names, cpu_usage_thresholds):
            process = Process.find_process_by_name(process_name)
            if process is None:
                self.monitored_processes[process_name] = None
            else:
                process_instance = Process(process)
                self.monitored_processes[process_name] = process_instance
            self.cpu_thresholds[process_name] = threshold

    def __process_instance(self, process_name: str) -> Process | None:
        """Returns a Process instance belongs to self.

        Parameters
        ----------
        process_name : str
            Process name (dict key).

        Returns
        -------
        Process | None
            Fount Process instance or None.
        """
        return self.monitored_processes.get(process_name)

    def __set_process_instance(self, process_name: str, new_process_instance: Process):
        """Updates Process instance belongs to self.

        Parameters
        ----------
        process_name : str
            Process name (dict key).
        new_process_instance : Process
            Assigned Process instance.
        """
        self.monitored_processes[process_name] = new_process_instance

    def __update_process_instance_if_needed(self, process_instance: Process, current_process: psutil.Process) -> Process:
        """Update Process instance if needed.

        Parameters
        ----------
        process_instance : Process
            Current Process instance belongs to self.
        current_process : psutil.Process
            Current process.

        Returns
        -------
        Process
            Existing Process instance or updated Process instance.
        """
        # If pid is changed, update Process instance.
        if process_instance and process_instance.pid != current_process.pid:
            # Update has_process_been_executed before update instance.
            self.update_has_process_been_executed_by_a_process(process_instance.name)

            new_process_instance = Process(current_process)
            self.__set_process_instance(process_instance.name, new_process_instance)
            return new_process_instance
        return process_instance

    def __create_and_set_process_instance(self, process_name: str, process: psutil.Process) -> Process:
        """Create Process instance by psutil.Process instance and set instance.

        Parameters
        ----------
        process_name : str
            Process name.
        process : psutil.Process
            psutil.Process instance.

        Returns
        -------
        Process
            Created process instance.
        """
        new_process_instance = Process(process)
        self.__set_process_instance(process_name, new_process_instance)
        return new_process_instance

    def __init_monitored_process(self):
        """Initialize or reset self.monitored_process
        """
        d = {}
        for key in self.monitored_process_names:
            d[key] = None
        self.monitored_processes = d

    def update_process_instance_and_has_process_been_executed(self):
        """Update process instance and has_process_been_executed if needed.

        FIXME: Split this method.
        - If process exist in current process list
            - If has a Process instance, update process instance if needed, and update max_cpu_usage
            - If doesn't have a Process instance, create and set Process instance and update max_cpu_usage
        - If process doesn't exist, do noting.
        """
        if self.has_process_been_executed:
            return

        for process_name in self.monitored_process_names:
            current_process = self.find_process_by_name(process_name)

            # If process exist in current process list.
            if current_process:
                # Python3.8↑ can use walrus operator. Like this: if process_instance := ...
                # If has a Process instance, update process instance if needed, and update max cpu usage.
                process_instance = self.__process_instance(process_name)
                if process_instance:
                    updated_process_instance = self.__update_process_instance_if_needed(process_instance, current_process)
                    updated_process_instance.update_max_cpu_usage_if_needed()
                # If doesn't have a Process instance, create instance and update max cpu usage.
                else:
                    new_process_instance = self.__create_and_set_process_instance(process_name, current_process)
                    new_process_instance.update_max_cpu_usage_if_needed()
            # If process doesn't exist current process list, do nothing.

        # Update self.has_process_been_executed with updated Process instance.
        self.update_has_process_been_executed_by_all_processes()

    def reset_has_process_been_executed(self):
        """Reset has_process_been_executed.
        """
        self.has_process_been_executed = False
        self.__init_monitored_process()

    def update_has_process_been_executed_by_a_process(self, process_name: str):
        """Update has_process_been_executed by a process.

        Parameters
        ----------
        process_name : str
            Process name.
        """
        process = self.monitored_processes[process_name]
        threshold = self.cpu_thresholds[process_name]
        if process is None:
            return

        if process.max_cpu_usage >= threshold:
            self.has_process_been_executed = True

    def update_has_process_been_executed_by_all_processes(self):
        """Update has_process_been_executed by all processes.
        """
        for process_name in self.monitored_process_names:
            self.update_has_process_been_executed_by_a_process(process_name)

    @classmethod
    def find_process_by_name(cls, process_name: str) -> psutil.Process | None:
        """Find process by name.

        Parameters
        ----------
        process_name : str
            Process name.

        Returns
        -------
        psutil.Process | None
            Found Process or None.
        """
        return Process.find_process_by_name(process_name)
