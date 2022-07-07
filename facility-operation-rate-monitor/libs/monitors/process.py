import psutil

from config import config
from libs.exceptions import ReadOnlyError, ProcessTooManyError


class Process():
    def __init__(self, process: psutil.Process) -> None:
        self.process: psutil.Process = process
        self.__name: str = process.name()
        self.__pid: int = process.pid
        self.max_cpu_usage: float = 0.0

    @property
    def name(self) -> str:
        return self.__name

    @property
    def pid(self) -> int:
        return self.__pid

    @name.setter
    def name(self, __):
        raise ReadOnlyError("name is read-only property.")

    @pid.setter
    def pid(self, __):
        raise ReadOnlyError("pid is read-only property.")

    def cpu_usage(self, interval: int = 1) -> float:
        return self.process.cpu_percent(interval)

    def update_max_cpu_usage_if_needed(self):
        """Update max CPU usage if current max CPU usage < current cpu usage.
        """
        current_cpu_usage = self.cpu_usage()
        if self.max_cpu_usage < current_cpu_usage:
            self.max_cpu_usage = current_cpu_usage

    @classmethod
    def pid_exists(pid) -> bool:
        return psutil.pid_exists(pid)

    @classmethod
    def find_process_by_name(cls, process_name: str) -> psutil.Process | None:
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
        if monitored_process_names is None or cpu_usage_thresholds is None:
            print("not received")
            return

        self.is_process_running: bool = False
        self.monitored_processes: dict[str, Process | None] = {}
        self.monitored_process_names: list[str] = monitored_process_names
        self.cpu_usage_thresholds: dict[str, float] = {}

        for process_name, threshold in zip(monitored_process_names, cpu_usage_thresholds):
            p = Process.find_process_by_name(process_name)
            if p is None:
                print("not found: ", process_name)
                self.monitored_processes[process_name] = None
            else:
                print("found: ", process_name)
                proc = Process(p)
                self.monitored_processes[process_name] = proc
            self.cpu_usage_thresholds[process_name] = threshold

    def __process_instance(self, process_name: str) -> Process | None:
        return self.monitored_processes.get(process_name)

    def __update_process_instance(self, process_name: str, new_process_instance: Process):
        self.monitored_processes[process_name] = new_process_instance

    def update_process_instance_if_needed(self, process_instance: Process, current_process: psutil.Process):
        if process_instance and process_instance.pid != current_process.pid:
            print("pidが変わったので更新する")
            self.update_is_process_running_by_a_process(process_instance.name)
            new_process_instance = Process(current_process)
            self.__update_process_instance(process_instance.name, new_process_instance)
            return new_process_instance
        return process_instance

    def create_process_instance(self, process_name: str, process: psutil.Process):
        new_process_instance = Process(process)
        self.monitored_processes[process_name] = new_process_instance
        return new_process_instance

    def update_process_instance_and_cpu_usage_if_needed(self):
        if self.is_process_running:
            print("稼働フラグが立っている")
            return

        for process_name in self.monitored_process_names:
            current_process = self.find_process_by_name(process_name)

            # If process exist in current process list.
            if current_process:
                print("プロセスは存在する: ", process_name)
                # If has a Process instance, update process instance if needed, and update max cpu usage.
                if process_instance := self.__process_instance(process_name):
                    print("インスタンスは存在するので更新処理")
                    updated_process_instance = self.update_process_instance_if_needed(process_instance, current_process)
                    updated_process_instance.update_max_cpu_usage_if_needed()
                # If doesn't have a Process instance, create instance and update max cpu usage.
                else:
                    print("インスタンスは存在しないので作成する")
                    new_process_instance = self.create_process_instance(process_name, current_process)
                    new_process_instance.update_max_cpu_usage_if_needed()
            # If process doesn't exist current process list, do nothing.
            else:
                print("プロセスは存在しない", process_name)

        self.update_is_process_running_by_all_processes()

    def reset_is_process_running(self):
        self.is_process_running = False

    def update_is_process_running_by_a_process(self, process_name: str):
        process = self.monitored_processes[process_name]
        threshold = self.cpu_usage_thresholds[process_name]
        if process is None:
            return

        if process.max_cpu_usage >= threshold:
            print("しきい値を超えた", process_name, process.max_cpu_usage)
            self.is_process_running = True

    def update_is_process_running_by_all_processes(self):
        for process_name in self.monitored_process_names:
            self.update_is_process_running_by_a_process(process_name)

    @classmethod
    def find_process_by_name(cls, process_name: str) -> psutil.Process | None:
        return Process.find_process_by_name(process_name)
