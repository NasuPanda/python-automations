import psutil
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener


class InputDeviceMonitor():
    """Monitor input device.

    NOTE:
        This class dependent on pynput.
        reference: https://pynput.readthedocs.io/en/latest

    Instance variables
    ----------
    keystroke_count: int
        Input key count.
        Increments when fire on_press callback.
    click_count: int
        Click count.
        Increments when fire on_click callback.
    mouse_movement_count: int
        Mouse movement count.
        Increments when fire on_move ar on_scroll callback.
    mouse_listener: pynput.mouse.Listenr
        Mouse input event listener.
    keyboard_listener: pynput.keyboard.Listener
        Keyboard input event lister.
    """
    def __init__(self) -> None:
        """Initialize an instance.
        """
        self.click_count: int = 0
        self.keystroke_count: int = 0
        self.mouse_movement_count: int = 0

        self.mouse_listener: MouseListener = MouseListener(
            on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll
        )
        self.keyboard_listener: KeyboardListener = KeyboardListener(
            on_press=self.on_press, on_release=self.on_release
        )

    @property
    def total_input_count(self) -> int:
        """Returns total number of device input.

        Returns
        -------
        int
            total number of device input.
        """
        return self.keystroke_count + self.click_count + self.mouse_movement_count

    def start_listener(self):
        """Activate input event listener.
        """
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop_listener(self):
        """Stop input event listener.
        """
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def reset_count(self):
        """Reset instance variables for counting.
        """
        self.click_count = 0
        self.keystroke_count = 0
        self.mouse_movement_count = 0

    def on_press(self, key):
        """Callback on press key. Increments keystroke count.
        """
        self.keystroke_count += 1

    def on_release(self, key):
        """Callback on release key. Do nothing.
        """
        pass

    def on_move(self, x, y):
        """Callback on move mouse. Increments mouse movement count.
        """
        self.mouse_movement_count += 1

    def on_click(self, x, y, button, pressed):
        """Callback on click mouse. If pressed, increments click count.
        """
        if pressed:
            self.click_count += 1

    def on_scroll(self, x, y, dx, dy):
        """Callback on scroll mouse. Increments mouse movement count.
        """
        self.mouse_movement_count += 1


class HardwarePerformanceMonitor():
    """Hardware performance Monitor.

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
    """
    def __init__(self) -> None:
        """Initialize an instance.
        """
        # CPU usage [%]
        self.max_cpu_usage: float = 0.0
        self.cpu_usages_to_get_ave: list[float] = []

    @property
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

    def reset(self):
        """Reset instance variable for monitoring CPU usage.
        """
        self.cpu_usages_to_get_ave = []
        self.max_cpu_usage = 0.0

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
