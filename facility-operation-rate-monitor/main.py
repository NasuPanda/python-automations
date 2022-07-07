from time import sleep
from libs.logger import Logger
from libs.monitors.device import InputDeviceMonitor
from libs.monitors.process import ProcessesMonitor
from libs import timehelper
from libs.timehelper import TimeShifter


process_monitor = ProcessesMonitor()
current = timehelper.current()
time_shifter = TimeShifter(start=current, shift_step_min=1)
logger = Logger()

print("開始時刻: ", timehelper.format(current, "long"))

while True:
    next_shift = time_shifter.next_shift()
    device_monitor = InputDeviceMonitor()
    device_monitor.start_listener()
    print("次の時間まで監視, 入力がなければ非稼働と判定", timehelper.format(next_shift, "long"))

    while timehelper.is_faster_than(next_shift, timehelper.current()):
        # パフォーマンスモニターの値を更新
        process_monitor.update_process_instance_and_has_process_been_executed()
        timehelper.sleep()

    print("*" * 50)
    print("1セクションの監視終了: ", timehelper.format(next_shift, "long"))
    print(f"クリック回数:{device_monitor.click_count} キー入力回数: {device_monitor.keystroke_count} マウス移動回数: {device_monitor.mouse_movement_count}")

    device_input = "入力有" if device_monitor.existence_of_input else "入力無"
    print(f"デバイス入力: {device_input}")
    process_status = "稼働" if process_monitor.has_process_been_executed else "非稼働"
    print(f"プロセスの稼働: {process_status}")

    logger.write_log(device_monitor.existence_of_input, process_monitor.has_process_been_executed)
    print("*" * 50)

    device_monitor.stop_listener()
    process_monitor.reset_has_process_been_executed()
