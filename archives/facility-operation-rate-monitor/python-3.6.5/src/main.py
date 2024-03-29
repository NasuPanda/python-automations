def record_current_process_pid():
    import psutil
    from config import config

    current_process_pid = psutil.Process().pid
    with open(config.CURRENT_PID_FILE, "w") as f:
        f.write(str(current_process_pid))


def main():
    from config import config
    from libs import timehelper
    from libs.logger import Logger
    from libs.monitors.active_window import ActiveWindowMonitor
    from libs.monitors.device import InputDeviceMonitor
    from libs.timehelper import TimeShifter

    # Record current process pid for kill current process from bat.
    record_current_process_pid()

    active_window_monitor = ActiveWindowMonitor(config.MONITORING_PROCESSES)
    current = timehelper.current()
    time_shifter = TimeShifter(start=current, shift_step_min=config.MONITOR_INTERVAL_MINUTES)
    logger = Logger()

    # for debug
    print("開始時刻: ", timehelper.format(current, "long"))

    while True:
        next_shift = time_shifter.next_shift()
        device_monitor = InputDeviceMonitor()
        device_monitor.start_listener()
        # for debug
        print("次の時間まで監視, 入力がなければ非稼働と判定", timehelper.format(next_shift, "long"))
        print(f"監視対象のアプリケーション: {active_window_monitor.monitoring_apps}")

        while timehelper.is_faster_than(next_shift, timehelper.current()):
            timehelper.sleep()

        # for debug
        print("1セクションの監視終了: ", timehelper.format(next_shift, "long"))
        print(
            f"クリック回数:{device_monitor.click_count} キー入力回数: {device_monitor.keystroke_count} マウス移動回数: {device_monitor.mouse_movement_count}"
        )

        device_input = "入力有" if device_monitor.has_received_input else "入力無"
        print(f"デバイス入力: {device_input}")
        process_status = "稼働" if active_window_monitor.exists_active_process() else "非稼働"
        print(f"アクティブなウィンドウのタイトル: {active_window_monitor.get_active_window_title()}")
        print(f"プロセスの稼働: {process_status}")

        logger.write_log(
            has_received_input=device_monitor.has_received_input,
            has_process_been_executed=active_window_monitor.exists_active_process(),
            active_window_title=active_window_monitor.get_active_window_title(),
        )

        device_monitor.stop_listener()


if __name__ == "__main__":
    main()
