from libs.monitors.file import FileSystemMonitor
import os


def mkdir(filepath):
    os.makedirs(filepath)


def mkfiles(dir: str, files: list[str]):
    for f in files:
        with open(os.path.join(dir, f), "w"):
            pass


dir_1 = "./test/filesystem/1"
files_1_1 = ["1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt", "7.txt", "8.txt", "9.txt", "10.txt"]
files_1_2 = ["1.csv", "2.csv", "3.csv", "4.csv", "5.csv", "6.csv", "7.csv", "8.csv", "9.csv", "10.csv"]
dir_2 = "./test/filesystem/2"
files_2 = ["1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt", "7.txt", "8.txt", "9.txt", "10.txt"]


filesystem_monitor = FileSystemMonitor("./test/filesystem", 11, 20)
filesystem_monitor.update_monitored_folder_and_has_process_been_executed(5)
print("false", filesystem_monitor.has_process_been_executed)

mkdir(dir_1)

filesystem_monitor.update_monitored_folder_and_has_process_been_executed(5)
print("true", filesystem_monitor.has_process_been_executed)

mkfiles(dir_1, files_1_1)

filesystem_monitor.update_monitored_folder_and_has_process_been_executed(5)
print("true(閾値を超えないため)", filesystem_monitor.has_process_been_executed)

mkfiles(dir_1, files_1_2)

filesystem_monitor.update_monitored_folder_and_has_process_been_executed(5)
print("false(閾値を超えるため終了)", filesystem_monitor.has_process_been_executed)

mkdir(dir_2)

filesystem_monitor.update_monitored_folder_and_has_process_been_executed(5)
print("true", filesystem_monitor.has_process_been_executed)
filesystem_monitor.update_monitored_folder_and_has_process_been_executed(5)
print("true", filesystem_monitor.has_process_been_executed)
filesystem_monitor.update_monitored_folder_and_has_process_been_executed(5)
print("true", filesystem_monitor.has_process_been_executed)
filesystem_monitor.update_monitored_folder_and_has_process_been_executed(5)
print("false(監視限界時間超え)", filesystem_monitor.has_process_been_executed)

mkfiles(dir_2, files_2)

filesystem_monitor.update_monitored_folder_and_has_process_been_executed(5)
print("false(監視限界時間超え)", filesystem_monitor.has_process_been_executed)
