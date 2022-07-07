from libs.monitors.device import InputDeviceMonitor
from libs.monitors.system import SystemPerformanceMonitor
from libs import timehelper
from libs.timehelper import TimeShifter


monitor = InputDeviceMonitor()
performance_monitor = SystemPerformanceMonitor()
monitor.start_listener()
current = timehelper.current()
finish = timehelper.shift_minutes(current, 3)
time_shifter = TimeShifter(start=current, shift_step_min=1)

print("開始時刻: ", timehelper.format(current))
print("終了予定: ", timehelper.format(finish))

# Finish if current == finish
while timehelper.is_faster_than(finish, timehelper.current()):
    next_shift = time_shifter.next_shift()
    print("次の時間まで監視, 入力がなければ非稼働と判定", timehelper.format(next_shift))

    while timehelper.is_faster_than(next_shift, timehelper.current()):
        # パフォーマンスモニターの値を更新
        performance_monitor.add_current_cpu_usage_to_cpu_usages()
        performance_monitor.add_current_memory_usage_to_memory_usages()

    print("1セクションの監視終了: ", timehelper.format(next_shift))
    print(f"カウント クリック回数:{monitor.click_count} キー入力回数: {monitor.keystroke_count} マウス移動回数: {monitor.mouse_movement_count}")

    judge = "入力有" if monitor.existence_of_input else "入力無"
    print(f"判定: {judge}")
    print("CPU負荷の平均", performance_monitor.cpu_usage_average)
    print("メモリ使用量の平均", performance_monitor.memory_usage_average)

    monitor.reset_count()
    performance_monitor.reset()

monitor.stop_listener()
print("終了: ", timehelper.format(finish))
print("finish")
