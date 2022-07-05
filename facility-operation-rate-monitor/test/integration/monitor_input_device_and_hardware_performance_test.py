from time import sleep
from libs.monitor import InputDeviceMonitor, HardwarePerformanceMonitor
from libs.timehelper import TimeHelper


monitor = InputDeviceMonitor()
performance_monitor = HardwarePerformanceMonitor()
monitor.start_listener()
current = TimeHelper.current()
finish = TimeHelper.shift_minutes(current, 3)
time_helper = TimeHelper(start=current, shift_step_min=1)

print("開始時刻: ", TimeHelper.format(current))
print("終了予定: ", TimeHelper.format(finish))

# Finish if current == finish
while TimeHelper.is_faster_than(finish, TimeHelper.current()):
    next_shift = time_helper.next_shift()
    print("次の時間まで監視, 入力がなければ非稼働と判定", TimeHelper.format(next_shift))

    while TimeHelper.is_faster_than(next_shift, TimeHelper.current()):
        # パフォーマンスモニターの値を更新
        performance_monitor.add_current_cpu_usage_to_cpu_usages()
        performance_monitor.add_current_memory_usage_to_memory_usages()

    print("1セクションの監視終了: ", TimeHelper.format(next_shift))
    print(f"カウント クリック回数:{monitor.click_count} キー入力回数: {monitor.keystroke_count} マウス移動回数: {monitor.mouse_movement_count}")

    judge = "入力有" if monitor.total_input_count else "入力無"
    print(f"判定: {judge}")
    print("CPU負荷の平均", performance_monitor.cpu_usage_average)
    print("メモリ使用量の平均", performance_monitor.memory_usage_average)

    monitor.reset_count()
    performance_monitor.reset()

monitor.stop_listener()
print("終了: ", TimeHelper.format(finish))
print("finish")
