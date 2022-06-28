from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener


class InputDeviceMonitor():
    """Monitor input device.
    """
    def __init__(self) -> None:
        self.input_key_count = 0
        self.click_count = 0
        self.mouse_move_count = 0
        self.keyboard_listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release)
        self.mouse_listener = MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)

    def start(self):
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop(self):
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def reset_count(self):
        self.input_key_count = 0
        self.click_count = 0
        self.mouse_move_count = 0

    def judge_count(self):
        return self.input_key_count or self.click_count or self.mouse_move_count

    def on_press(self, key):
        self.input_key_count += 1

    def on_release(self, key):
        return

    def on_move(self, x, y):
        self.mouse_move_count += 1

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.click_count += 1

    def on_scroll(self, x, y, dx, dy):
        self.mouse_move_count += 1
