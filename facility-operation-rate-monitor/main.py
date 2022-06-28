from libs.monitor import InputDeviceMonitor
from libs.timehelper import TimeHelper


monitor = InputDeviceMonitor()
monitor.start()
current = TimeHelper.current()
finish = TimeHelper.shift_minutes(current, 3)
time_helper = TimeHelper(start=current, shift_step_min=1)

print("開始時刻: ", TimeHelper.format(current))
print("終了予定: ", TimeHelper.format(finish))

# Finish if current == finish
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

    monitor.reset_count()

monitor.stop()
print("終了: ", TimeHelper.format(finish))
print("finish")
