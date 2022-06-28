import threading
from pynput import keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

from timehelper import TimeHelper

class InputDeviceMonitor():
    """入力デバイスを監視する。

    NOTE: join
    keyboard_listener.join()
    mouse_listener.join()

    joinを呼び出したスレッドが終了するまで待機。
    joinを呼び出したスレッドが終了するまで呼び出し元のスレッドをブロックする。
    joinを呼ばない場合、次の処理に移ってしまう = 先にメインスレッドが終了してしまう。

    joinを呼んでしまうとそこで処理がブロックされてしまうため、後の処理に回すことが出来ない。
    が、joinの役割を考えるとjoinを呼び出さずともメインスレッドが終了しなければいいだけの話。

    今回の要件は指定時間までスレッドにより入力デバイスを監視すること。
    つまり、スレッドを動かした後はWhileで時刻を監視、指定時間を過ぎたら終了・・・のようにすれば良いだけ。

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

    def reset(self):
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


monitor = InputDeviceMonitor()
monitor.start()
current = TimeHelper.current()
finish = TimeHelper.shift_minutes(current, 3)
time_helper = TimeHelper(start=current, shift_step_min=1)

print("開始時刻: ", TimeHelper.format(current))
print("終了予定: ", TimeHelper.format(finish))

# finish if current == finish
while (
    TimeHelper.get_hour_and_min(TimeHelper.current()) !=
    TimeHelper.get_hour_and_min(finish)
):
    next_shift = time_helper.next_shift()
    print("次の時間まで監視, 入力がなければ非稼働と判定", TimeHelper.format(next_shift))

    while (
        TimeHelper.get_hour_and_min(TimeHelper.current()) !=
        TimeHelper.get_hour_and_min(next_shift)
    ):
        pass
    print("1セクションの監視終了: ", TimeHelper.format(next_shift))
    print(f"カウント クリック回数:{monitor.click_count} キー入力回数: {monitor.input_key_count} マウス移動回数: {monitor.mouse_move_count}")
    judge = "入力有" if monitor.judge_count() else "入力無"
    print(f"判定: {judge}")

    monitor.reset()

print("終了: ", TimeHelper.format(finish))
print("finish")
