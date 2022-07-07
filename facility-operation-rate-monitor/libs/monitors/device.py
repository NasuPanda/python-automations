from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener


class InputDeviceMonitor():
    """Monitor input device.

    NOTE
    - This class dependent on pynput.
        - reference: https://pynput.readthedocs.io/en/latest

    - All callbacks stop the input device listener when called.
        - It's enough for the listener to be able to monitor only the existence of input.

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
    def existence_of_input(self) -> bool:
        """Returns Existence of input.

        Returns
        -------
        int
            Existence of input.
        """
        return bool(
            self.keystroke_count + self.click_count + self.mouse_movement_count
        )

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
        self.stop_listener()

    def on_release(self, key):
        """Callback on release key. Do nothing.
        """
        pass

    def on_move(self, x, y):
        """Callback on move mouse. Increments mouse movement count.
        """
        self.mouse_movement_count += 1
        self.stop_listener()

    def on_click(self, x, y, button, pressed):
        """Callback on click mouse. If pressed, increments click count.
        """
        if pressed:
            self.click_count += 1
            self.stop_listener()

    def on_scroll(self, x, y, dx, dy):
        """Callback on scroll mouse. Increments mouse movement count.
        """
        self.mouse_movement_count += 1
        self.stop_listener()

