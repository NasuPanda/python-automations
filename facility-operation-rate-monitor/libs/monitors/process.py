import psutil

from config import config


class ProcessesMonitor():
    def __init__(self, monitored_processes: list[str] | None = config.MONITORED_PROCESSES) -> None:
        if monitored_processes is None:
            return


