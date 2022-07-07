from time import sleep
from libs.monitors.process import ProcessesMonitor

# 対象のプロセスを起動して開始
# config.ymlのしきい値を上げておくこと
monitor = ProcessesMonitor()
monitor.update_process_instance_and_has_process_been_executed()
print("finish 1")

# スリープ中にプロセスを落とす
sleep(20)
print("start 2")
monitor.update_process_instance_and_has_process_been_executed()
print("finish 2")


# スリープ中に対象のプロセスを再起動する
# 正しく動作していればpidの変更を検知してインスタンスが更新される
sleep(20)
print("start 3")
monitor.update_process_instance_and_has_process_been_executed()
print("finish 3")
