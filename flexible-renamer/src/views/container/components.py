from typing import Any

from src.common import exceptions, utils
from src.common.constants import ComponentKeys
from src.common.types import Config
from src.config.parser import ConfigParser
from src.models.file import FileFilter, FileRenamer
from src.views.presentational import components


class UserInterface:
    def __init__(self) -> None:
        self.window = components.window()

        self.events = {
            ComponentKeys.input_setting_file: self.on_input_setting_file,
            ComponentKeys.input_folder: self.on_input_folder,
            ComponentKeys.submit: self.on_click_submit,
        }
        self.config: Config | None = None

    def start_event_loop(self) -> None:
        """イベントループを発生させる"""
        while True:
            event, self.values = self.window.read()  # type: ignore

            if event is None:
                break

            else:
                self.events[event]()

    def close_window(self) -> None:
        """ウィンドを閉じる。"""
        self.window.close()

    def _notice_error(self, *messages: str) -> None:
        components.popup_error(*messages)

    def _notice_ok(self, *messages: str) -> None:
        components.popup_ok(*messages)

    def _get_values(self, key: str) -> Any:
        """特定のkeyのvaluesを返す

        Args:
            key (str): コンポーネントのキー

        Returns:
            Any: 取得したvalues
        """
        try:
            return self.values[key]
        except AttributeError:
            print("read_window が実行されていません!")

    def _clear(self, key: str) -> None:
        self.window[key].update("")  # type: ignore

    def _update_value(self, key: str, value: str) -> None:
        self.window[key].update(value)  # type: ignore

    def clear_input_folder(self) -> None:
        self._clear(ComponentKeys.input_folder)

    def update_preview(self) -> None:
        """プレビューを表示する

        Args:
            *messages (str): 表示するメッセージの配列
        """
        if self.config is None:
            return
        if not self.config.src_folder_path:
            return

        filter = self._exec_filter(self.config.layouts[0])
        if filter is None:
            return
        renamer = self._exec_rename(filter.filepaths)
        if renamer is None:
            return

        self._clear(ComponentKeys.multiline_preview)
        [self.window[ComponentKeys.multiline_preview].print(message) for message in renamer.format_previews()]  # type: ignore

    def _exec_filter(self, flag_name: str) -> FileFilter | None:
        if self.config is None:
            return None
        if not self.config.src_folder_path:
            return None

        filter = FileFilter(src_folder=self.config.src_folder_path)
        try:
            filter.filter_by_extension(self.config.target_extension)
        except (FileNotFoundError, exceptions.ExtensionError) as e:
            self._notice_error(str(e))
            self.clear_input_folder()
            return None

        try:
            filter.filter_by_name_include(flag_name)
        except FileNotFoundError as e:
            self._notice_error(str(e))
            self.clear_input_folder()
            return None
        return filter

    def _exec_rename(self, src_files: list[str]) -> FileRenamer | None:
        if self.config is None:
            return None
        if not self.config.src_folder_path:
            return None

        renamer = FileRenamer(src_files=src_files, delimiter=self.config.delimiter)
        try:
            renamer.replace_parts(self.config.data_names, self.config.name_index.get_before())
        except (exceptions.LengthDoesNotMatchError, IndexError) as e:
            self._notice_error(str(e))
            self.clear_input_folder()
            return None
        try:
            renamer.swap_parts(self.config.name_index.get_after(), self.config.layout_index.get_after())
        except (ValueError, exceptions.ReplaceError) as e:
            self._notice_error(str(e))
            self.clear_input_folder()
            return None
        return renamer

    def on_input_setting_file(self) -> None:
        setting_file = self._get_values(ComponentKeys.input_setting_file)
        try:
            parser = ConfigParser(setting_file)
            self.config = parser.parse_config()
        except (KeyError, exceptions.ConfigParseError) as e:
            self._notice_error(str(e))
            self._clear(ComponentKeys.input_setting_file)
            return

        if self.config.src_folder_path:
            self._update_value(ComponentKeys.input_folder, self.config.src_folder_path)
        self.update_preview()

    def on_input_folder(self) -> None:
        if self.config is None:
            self._notice_error("先に設定ファイルを入力して下さい")
            self.clear_input_folder()
            return
        self.config.src_folder_path = self._get_values(ComponentKeys.input_folder)
        self.update_preview()

    def on_click_submit(self) -> None:
        if self.config is None:
            self._notice_error("設定ファイルを入力して下さい")
            return
        if not self.config.src_folder_path:
            self._notice_error("画像が入ったフォルダを入力して下さい")
            return

        for layout in self.config.layouts:
            filter = self._exec_filter(layout)
            if filter is None:
                return
            renamer = self._exec_rename(filter.filepaths)
            if renamer is None:
                return
            renamer.copy_from_src_to_dst(self.config.dst_folder)

        self._notice_ok("ファイルのリネームに成功しました", f"保存先: {self.config.dst_folder}")
