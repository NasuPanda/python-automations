import functools
import itertools
import threading
import time
from typing import Callable


class Spinner:
    def __init__(
        self,
        text: str = "Please wait...",
        etext: str = "",
        overwrite: bool = True,
    ) -> None:
        self.text = text
        self.end_text = etext
        self.overwrite = overwrite

    def start(self) -> None:
        self._stop_flag = False
        self._spinner_thread = threading.Thread(target=self._spinner)
        self._spinner_thread.setDaemon(True)
        self._spinner_thread.start()

    def stop(self, etext: str = "", overwrite: bool = True) -> None:
        if self._spinner_thread and self._spinner_thread.is_alive():
            self._stop_flag = True
            self._spinner_thread.join()

        text = etext or self.end_text
        overwrite = self.overwrite if not self.overwrite else overwrite

        if overwrite:
            if etext == "":
                print(f"\r\033[2K\033[G", end="")
            else:
                print(f"\r\033[2K\033[G{etext}")
        else:
            if etext == "":
                print(f"\033[1D\033[K\n", end="")
            else:
                print(f"\033[1D\033[K\n{etext}")

    def _spinner(self) -> None:
        chars = itertools.cycle(r"/-\|")
        while not self._stop_flag:
            print(f"\r{self.text} {next(chars)}", end="")
            time.sleep(0.2)

    def __enter__(self) -> None:
        self.start()

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.stop()

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapped
