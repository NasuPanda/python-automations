import os


class FileSystemMonitor:
    """
    references:
        - [Python Count Number of Files in a Directory [4 Ways] | PYnative](https://pynative.com/python-count-number-of-files-in-a-directory/)
    """

    def __init__(
        self, monitored_root_folder: str, threshold_of_number_of_files: int, max_monitoring_time: int
    ) -> None:
        # 監視対象のフォルダ
        if os.path.isdir(monitored_root_folder):
            self.monitored_root_folder = monitored_root_folder
        else:
            raise ValueError(f"folder name: {monitored_root_folder} doesn't exist")
        # N個以上のファイルが生成されたら
        self.threshold_number_of_files_in_monitored_folder = threshold_of_number_of_files
        # 監視限界
        self.max_monitoring_time = max_monitoring_time
        self.total_monitoring_time = 0
        # 監視対象フォルダ配下のフォルダ(このフォルダの数が変われば新しいフォルダが出来たということになる)
        self.current_number_of_folder_in_root_folder = self.__count_folder_in_monitored_root_folder()
        self.current_monitored_folder: str = ""

        self.has_process_been_executed: bool = False

    def __exist_current_monitored_folder(self) -> bool:
        return True if self.current_monitored_folder else False

    def __is_new_folder_created_in_monitored_root_folder(self) -> bool:
        # ルートフォルダ配下に新しいフォルダが作成されたかどうか
        current_count = self.__count_folder_in_monitored_root_folder()

        if self.current_number_of_folder_in_root_folder != current_count:
            self.current_number_of_folder_in_root_folder = current_count
            return True
        else:
            return False

    def __monitoring_time_is_lather_than_max(self) -> bool:
        return self.total_monitoring_time >= self.max_monitoring_time

    def __number_of_files_in_monitored_folder_is_lather_than_threshold(self) -> bool:
        return self.__count_number_of_files_in_monitored_folder() >= self.threshold_number_of_files_in_monitored_folder

    def __count_folder_in_monitored_root_folder(self) -> int:
        # ルートフォルダ配下のフォルダ数をカウント
        count = 0

        for path in os.scandir(self.monitored_root_folder):
            if path.is_dir():
                count += 1

        return count

    def __find_latest_folder_in_monitored_root_folder(self) -> str | None:
        # ルートフォルダ配下の最新のフォルダを探す(新しいフォルダが作成されていなければ何もしない)
        if not self.__is_new_folder_created_in_monitored_root_folder():
            return None

        latest_ctime = 0.0
        latest_folder: str | None = None

        for path in os.scandir(self.monitored_root_folder):
            if path.is_dir():
                ctime = path.stat().st_ctime
                if latest_ctime < ctime:
                    latest_ctime = ctime
                    latest_folder = path.path

        return latest_folder

    def __update_monitored_folder_if_needed(self) -> None:
        latest_folder = self.__find_latest_folder_in_monitored_root_folder()
        if latest_folder:
            self.current_monitored_folder = latest_folder

    def __reset_monitoring_status(self) -> None:
        self.current_monitored_folder = ""
        self.total_monitoring_time = 0
        self.has_process_been_executed = False

    def __update_total_monitoring_time(self, monitoring_time: int) -> int:
        self.total_monitoring_time += monitoring_time
        return self.total_monitoring_time

    def __count_number_of_files_in_monitored_folder(self) -> int:
        # 監視対象フォルダ配下のファイル数をカウント
        count = 0
        # root_dir, cur_dir, files
        for _, _, files in os.walk(self.current_monitored_folder):
            count += len(files)

        return count

    def update_monitored_folder_and_has_process_been_executed(self, monitoring_time: int) -> None:
        self.__update_monitored_folder_if_needed()
        # そもそも監視対象のフォルダが存在しない場合
        if not self.__exist_current_monitored_folder():
            self.has_process_been_executed = False
            return

        # 現在の状態: 監視対象フォルダが更新

        if self.__number_of_files_in_monitored_folder_is_lather_than_threshold():
            self.__reset_monitoring_status()
            return

        # 現在の状態: 監視対象フォルダが更新、監視対象フォルダ配下のファイル数判定終了

        self.__update_total_monitoring_time(monitoring_time)
        if self.__monitoring_time_is_lather_than_max():
            self.__reset_monitoring_status()
            return

        # 現在の状態: 監視対象フォルダが更新、監視対象フォルダ配下のファイル数判定・最大モニタリング時間の判定終了
        self.has_process_been_executed = True
