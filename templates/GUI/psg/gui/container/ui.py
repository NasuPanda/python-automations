from typing import Any

from backend import sample
from common import utils
from common.constants import (
    APP_PREVIEWER_HEIGHT,
    TARGET_EXTENSION,
    DefaultText,
    LogTextColors,
    UIEventKeys,
)
from gui.presentational.index import create_window


class UserInterface:
    """UIのread/write, backend処理の呼び出しを担う"""

    def __init__(self) -> None:
        self._window = create_window()
        self._events = {
            UIEventKeys.setting_file_input: self.on_input_setting_file,
            UIEventKeys.folder_input: self.on_input_folder,
            UIEventKeys.exec_button: self.on_click_execute_button,
        }

    def __del__(self) -> None:
        self._window.close()

    def init_window(self) -> None:
        """ウィンドウを初期化し、イベントループを発生させる"""
        while True:
            event, self._ui_values = self._window.read()  # type: ignore

            if event is None:
                break

            else:
                # イベントの呼び出し
                self._events[event]()

    # Private methods
    def _get_values_from_ui(self, key: str) -> Any:
        """private: 指定したkeyのvaluesを返す"""
        return self._ui_values[key]

    def _get_component(self, key: str) -> Any:
        """private: 指定したkeyのコンポーネントを返す"""
        return self._window[key]

    def _update_component(self, key: str, value: Any) -> None:
        """private: 指定したキーのコンポーネントの値を更新"""
        self._window[key].update(value)

    def _print_notice(self, *messages: str) -> None:
        """private: 通知をログに出力する"""
        [
            self._get_component(UIEventKeys.log).print(message, t=LogTextColors.notice)
            for message in messages
        ]

    def _print_alert(self, *messages: str) -> None:
        """private: 警告をログに出力する"""
        [
            self._get_component(UIEventKeys.log).print(message, t=LogTextColors.alert)
            for message in messages
        ]

    def _update_previewer(self, *messages) -> None:
        """private: プレビューの更新"""
        [
            self._get_component(UIEventKeys.previewer).print(message)
            for message in messages
        ]

    def _clear_previewer(self) -> None:
        """private: プレビューをクリアする"""
        [
            self._get_component(UIEventKeys.previewer).print("")
            for _ in range(APP_PREVIEWER_HEIGHT)
        ]

    def _exists_input_folder(self) -> bool:
        """private: フォルダの入力があるかどうか"""
        return self._get_values_from_ui(UIEventKeys.folder_input) != DefaultText.folder

    def _exists_input_user_setting(self) -> bool:
        """private: 設定ファイルの入力があるかどうか"""
        return (
            self._get_values_from_ui(UIEventKeys.setting_file_input)
            != DefaultText.user_setting
        )

    # Events
    def on_input_setting_file(self) -> None:
        setting_file_path = self._get_values_from_ui(UIEventKeys.setting_file_input)
        user_setting = sample.read_setting_from_excel(setting_file_path)
        self._update_previewer(*list(user_setting))

        # 例: 設定をインスタンス変数として保持する例
        # self._input_data["user_setting"] = user_setting

        # 例: 設定の検証を追加する
        # if user_setting.is_invalid:
        # self._print_alert("[Error] 設定ファイルに誤りが含まれます")
        # return

        self._print_notice("[Success] 設定ファイルの読み込みに成功しました")

    def on_input_folder(self) -> None:
        # 例: 設定が入力されていなければエラー
        # if self._input_data["user_setting"] is None:
        #     self._print_alert("[Error] 先に設定を入力して下さい")
        #     return

        folder = self._get_values_from_ui(UIEventKeys.folder_input)
        files = utils.get_file_stems_from_folder(folder, TARGET_EXTENSION)

        if not files:
            self._print_alert(f"[Error]拡張子[{TARGET_EXTENSION}]のファイルが存在しません")
            return

        self._print_notice(
            "[Success]ファイル読み込み、拡張子の除外に成功しました", *[f"\t{file}" for file in files]
        )
        return

    def on_click_execute_button(self) -> None:
        self._print_notice("[Success]実行！！！")
