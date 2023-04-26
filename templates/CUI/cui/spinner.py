import functools
import itertools
import threading
import time
from typing import Callable


class Spinner:
    """Spinner.

    ## Usages:
    ### 1. Calling start() and stop()
    ```python
    >> spinner = Spinner(text="Loading...", etxet="Loading... Done.")
    >> spinner.start()
    >> # Doing something...
    >> spinner.stop()
    ```

    ### 2. With statement
    ```python
    >> with Spinner("Loading...", "Loading... Done."):
    >>     # Doing something...
    ```

    ### 3. As a decorator
    ```python
    >> @Spinner("Loading...", "Loading... Done.")
    >> def func():
    >>     # doing something
    >> func()
    ```
    """

    # Class variable
    SPINNER_CHARACTERS = r"/-\|"
    SLEEP_TIME = 0.2

    def __init__(
        self,
        message: str = "Please wait...",
        end_message: str = "Please wait...DONE.",
        overwrite: bool = True,
    ) -> None:
        self.message = message
        self.end_message = end_message
        self.enable_overwrite = overwrite

    def start(self) -> None:
        self._is_stop = False
        self._spinner_thread = threading.Thread(target=self._spinner)
        self._spinner_thread.setDaemon(True)
        self._spinner_thread.start()

    def stop(self, end_message: str = "", enable_overwrite: bool = True) -> None:
        if self._spinner_thread and self._spinner_thread.is_alive():
            self._is_stop = True
            self._spinner_thread.join()

        end_message = end_message or self.end_message
        enable_overwrite = self.enable_overwrite if not self.enable_overwrite else enable_overwrite

        if enable_overwrite:
            if end_message == "":
                print(f"\r\033[2K\033[G", end="")
            else:
                print(f"\r\033[2K\033[G{end_message}")
        else:
            if end_message == "":
                print(f"\033[1D\033[K\n", end="")
            else:
                print(f"\033[1D\033[K\n{end_message}")

    def _spinner(self) -> None:
        chars = itertools.cycle(self.SPINNER_CHARACTERS)
        while not self._is_stop:
            print(f"\r{self.message} {next(chars)}", end="")
            time.sleep(self.SLEEP_TIME)

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
