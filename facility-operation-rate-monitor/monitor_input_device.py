import threading
from pynput import keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

from timehelper import TimeHelper


def on_press(key):
    print("Key pressed: {0}".format(key))
    # コールバックがFalseを返す or 特定の例外を発生させると監視を終了
    if key == keyboard.Key.esc:
        return False


def on_release(key):
    print("Key released: {0}".format(key))

def on_move(x, y):
    print("Mouse moved to ({0}, {1})".format(x, y))

def on_click(x, y, button, pressed):
    if pressed:
        print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
    else:
        print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


def monitoring_input_device():
    keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
    mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

    keyboard_listener.start()
    mouse_listener.start()

    # NOTE: join
    # keyboard_listener.join()
    # mouse_listener.join()

    # joinを呼び出したスレッドが終了するまで待機。
    # joinを呼び出したスレッドが終了するまで呼び出し元のスレッドをブロックする。
    # joinを呼ばない場合、次の処理に移ってしまう = 先にメインスレッドが終了してしまう。

    # joinを呼んでしまうとそこで処理がブロックされてしまうため、後の処理に回すことが出来ない。
    # が、joinの役割を考えるとjoinを呼び出さずともメインスレッドが終了しなければいいだけの話。

    # 今回の要件は指定時間までスレッドにより入力デバイスを監視すること。
    # つまり、スレッドを動かした後はWhileで時刻を監視、指定時間を過ぎたら終了・・・のようにすれば良いだけ。

    current = TimeHelper.current()
    finish = TimeHelper.shift_minutes(current, 3)
    time_helper = TimeHelper(start=current, shift_step_min=1)

    # finish if current == finish
    while (
        TimeHelper.get_hour_and_min(TimeHelper.current()) !=
        TimeHelper.get_hour_and_min(finish)
    ):
        next_shift = time_helper.next_shift()
        print("next shift", next_shift)
        while (
            TimeHelper.get_hour_and_min(TimeHelper.current()) !=
            TimeHelper.get_hour_and_min(next_shift)
        ):
            pass
        print("finish inner loop at", next_shift)
    print("finish outer loop")


print("start")
monitoring_input_device()
print("finish")
