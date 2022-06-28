import threading
from pynput import keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener


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
    # スレッドが終了するまで待機する。joinを呼ばれたスレッドが終了するまで呼び出し元のスレッドをブロックする。
    keyboard_listener.join()
    mouse_listener.join()


print("start")
monitoring_input_device()
print("finish")

"""
# TODO
# problem
    # listenerがスレッドをブロックしているため、他の処理(ex: 時間の判定)に移行できない
    # コールバック内でフラグ判定するにしても、コールバックは入力がなければ起動しないため入力があってから終了になってしまう
# solution?
    # 別スレッドを作成, 別スレッド内で判定してリスナーを止める。

    # 別スレッド内
        # while start == fin:
            # do something
            # ここでスレッドをkill
            # thread_1.stop
            # thread_2.stop

    # threading.Event()で行けそう?
    # あるいは、Synchronous event listening(指定秒数イベントを取得するスタイル) で指定秒数取得する、でも可。(whileで時間を監視, 0.1sや1.0sごとに入力を監視するイメージ)
"""
