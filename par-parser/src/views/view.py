from copy import deepcopy
from typing import Callable, TypedDict

import PySimpleGUI as sg

import config


# テーマ, フォント等
FONT = "MeiryoUI"
THEME_COLOR = "BlueMono"
sg.theme(THEME_COLOR)

# Window, コンポーネントのスタイル
WINDOW_STYLES = {
    # Windowそのもののスタイル
    "style": {
        "title": config.WINDOW_TITLE,
        "size": (1000, 600),
        "font": FONT,
        "resizable": True,
    },
    # Windowが所有するコンポーネント
    "components": {
        # 試験モードの選択
        "select_mode_desc": {
            "text": "モードの選択",
            "font": (FONT, 12),
        },
        "select_mode_combo": {
            "key": config.SELECT_MODE_COMBO_KEY,
            "values": config.SELECT_EXPERIMENT_MODE_COMBO_VALUES,
            "default_value": config.DEFAULT_SELECT_EXPERIMENT_MODE_COMBO_VALUE,
            "size": (20, 1),
            "enable_events": True,
        },
        # フォルダ入力
        "par_folder_input": {
            "key": config.SRC_FOLDER_INPUT_KEY,
            "size": (30, 1),
            "font": (FONT, 12),
            "disabled": True,
            "enable_events": True,
        },
        "par_folder_browse": {
            "button_text": "フォルダを開く(.parファイル)",
            "size": (25, 1),
            "font": (FONT, 12),
        },
        # シート数/ファイルの入力
        "sheet_per_file_desc": {
            "text": "1ファイルに含むシート数を入力: ",
            "font": (FONT, 12),
        },
        "sheet_per_file_input": {
            "key": config.SHEET_PER_FILE_INPUT_KEY,
            "values": config.SHEET_PER_FILE_VALUES,
            "default_value": config.DEFAULT_SHEET_PER_FILE_VALUE,
            "size": (3, 1),
            "font": (FONT, 12),
            "enable_events": True,
        },
        # データ名の入力
        "data_name_part_desc": {
            "text": "サンプル名に当たる箇所を選択して下さい(選択した箇所がシート名/ファイル名になります)",
            "font": (FONT, 12),
        },
        "origin_filename": {
            "key": config.SELECT_DATA_NAME_ORIGIN_FILENAME_TEXT_KEY,
            "font": (FONT, 12)
        },
        "data_name_part_listbox": {
            "key": config.SELECT_DATA_NAME_PART_LISTBOX_KEY,
            "select_mode": sg.LISTBOX_SELECT_MODE_MULTIPLE,
            "size": (50, 5),
            "font": (FONT, 12),
            "enable_events": True,
        },
        # 実行 / フレーム
        "parse_par_to_vi_frame": {
            "title": "A. 各項目を選択/入力して下さい",
            "relief": sg.RELIEF_GROOVE,
            "font": (FONT, 12),
        },
        "parse_par_to_vi_submit": {
            "button_text": "A: 選択完了",
            "key": config.PARSE_PAR_TO_VI_SUBMIT_KEY,
            "font": (FONT, 14),
        },
        "write_vi_to_excel_submit": {
            "button_text": " OK (Excel出力)",
            "key": config.WRITE_VI_DATA_TO_EXCEL_SUBMIT_KEY,
            "font": (FONT, 14),
        },
        # ログ
        "output_log": {
            "key": config.LOG_KEY,
            "size": (50, 5),
            "default_text": "-- Log --\n",
            "font": (FONT, 12),
            "disabled": True,
            "no_scrollbar": True,
        },
    }
}

# extend可能なコンポーネントのスタイル
# NOTE: "#"を置換することでキーを可変にする
EXTENDABLE_FRAME_STYLES = {
    "frame": {
        "title": "B: Riの値を確認, 電圧を調整して下さい",
        "key": config.EXTENDABLE_FRAME_KEY,
        "relief": sg.RELIEF_GROOVE,
        "font": (FONT, 12),
    },
    "update": {
        "button_text": "B: Ri更新",
        "key": config.UPDATE_RESISTANCE_KEY,
        "font": (FONT, 14),
    },
    config.EXTENDABLE_RESISTANCE_VALIDITY_KEY: {
        "default": True,
        "key": config.EXTENDABLE_RESISTANCE_VALIDITY_CHECKBOX_KEY,
        "text": "判定",
        "font": (FONT, 10),
        "text_color": "black",
        "checkbox_color": "red",
        "disabled": True,
    },
    config.EXTENDABLE_RESISTANCE_KEY: {
        "key": config.EXTENDABLE_RESISTANCE_TEXT_KEY,
        "font": (FONT, 10),
    },
    config.EXTENDABLE_MIN_VOLTAGE_KEY: {
        "key": config.EXTENDABLE_MIN_VOLTAGE_INPUT_KEY,
        "font": (FONT, 10),
        "size": (5, 1),
    },
    config.EXTENDABLE_MAX_VOLTAGE_KEY: {
        "key": config.EXTENDABLE_MAX_VOLTAGE_INPUT_KEY,
        "font": (FONT, 10),
        "size": (5, 1),
    },
}


class ComponentInfo(TypedDict):
    """コンポーネントの情報
    style: コンポーネント生成に使うスタイルを持つ辞書
    method: コンポーネントを生成するメソッドの名前（動的に呼び出すため使用)
    container_key: コンポーネント挿入先コンテナのキー
    """
    style: dict
    method: Callable
    container_key: str


class UserInterFace():
    """GUI。ユーザとやり取りする役割を持つ。

    NOTE
    PySimpleGUIでは各コンポーネントをkeyで管理する。
    イベントの検知, 値の取得, 更新等を全てkeyで行う。

    Instance variables
    ----------
    next_keys: dict[str, int]
        現在のコンポーネント数(extendableなもの)を追跡するための辞書。
    extended_component_keys: list[str]
        extendされたコンポーネントのkeyを持つ配列。
    invalid_component_keys: dict[int, dict[str, str]]
        無効なコンポーネントの情報を持つ辞書。
        {index: {key: component, key_2: component}}
    window: sg.Window
        GUIウィンドウ。

    Class variables
    ----------
    EXTENDABLE_COMPONENTS: dict[str, ComponentInfo]
        extend可能なコンポーネントの情報
    EXTENDABLE_COMPONENT_KEYS: list[str]
        extend可能なコンポーネントのkey
    """

    EXTENDABLE_COMPONENTS = {
        config.EXTENDABLE_RESISTANCE_VALIDITY_KEY: ComponentInfo(
            style=EXTENDABLE_FRAME_STYLES[config.EXTENDABLE_RESISTANCE_VALIDITY_KEY],
            method=sg.Checkbox,
            container_key=config.EXTENDABLE_FRAME_KEY,
        ),
        config.EXTENDABLE_RESISTANCE_KEY: ComponentInfo(
            style=EXTENDABLE_FRAME_STYLES[config.EXTENDABLE_RESISTANCE_KEY],
            method=sg.Text,
            container_key=config.EXTENDABLE_FRAME_KEY,
        ),
        config.EXTENDABLE_MIN_VOLTAGE_KEY: ComponentInfo(
            style=EXTENDABLE_FRAME_STYLES[config.EXTENDABLE_MIN_VOLTAGE_KEY],
            method=sg.Input,
            container_key=config.EXTENDABLE_FRAME_KEY,
        ),
        config.EXTENDABLE_MAX_VOLTAGE_KEY: ComponentInfo(
            style=EXTENDABLE_FRAME_STYLES[config.EXTENDABLE_MAX_VOLTAGE_KEY],
            method=sg.Input,
            container_key=config.EXTENDABLE_FRAME_KEY,
        ),
    }
    EXTENDABLE_COMPONENT_KEYS = [config.EXTENDABLE_RESISTANCE_VALIDITY_KEY, config.EXTENDABLE_RESISTANCE_KEY, config.EXTENDABLE_MIN_VOLTAGE_KEY, config.EXTENDABLE_MAX_VOLTAGE_KEY]

    def __init__(self) -> None:
        self.next_keys = {
            config.EXTENDABLE_RESISTANCE_VALIDITY_KEY: 1,
            config.EXTENDABLE_RESISTANCE_KEY: 1,
            config.EXTENDABLE_MIN_VOLTAGE_KEY: 1,
            config.EXTENDABLE_MAX_VOLTAGE_KEY: 1
        }
        self.extended_component_keys = {
            config.EXTENDABLE_RESISTANCE_VALIDITY_KEY: [],
            config.EXTENDABLE_RESISTANCE_KEY: [],
            config.EXTENDABLE_MIN_VOLTAGE_KEY: [],
            config.EXTENDABLE_MAX_VOLTAGE_KEY: []
        }
        self.invalid_component_keys: dict[int, dict[str, str]] = {}
        self.window = sg.Window(
            layout=[
                [
                    # HACK: sg.T("")でレイアウト調整(あまりよろしくない)
                    sg.Column([
                        [
                            sg.Frame(layout=[
                                [
                                    sg.T(**WINDOW_STYLES["components"]["select_mode_desc"]),
                                    sg.Combo(**WINDOW_STYLES["components"]["select_mode_combo"])
                                ],
                                [
                                    sg.Input(**WINDOW_STYLES["components"]["par_folder_input"]),
                                    sg.FolderBrowse(**WINDOW_STYLES["components"]["par_folder_browse"])
                                ],
                                [
                                    sg.T(**WINDOW_STYLES["components"]["sheet_per_file_desc"]),
                                    sg.Combo(**WINDOW_STYLES["components"]["sheet_per_file_input"])
                                ],
                                [sg.T("")],
                                [sg.T(**WINDOW_STYLES["components"]["data_name_part_desc"])],
                                [sg.T("元ファイル名: 未入力です", **WINDOW_STYLES["components"]["origin_filename"])],
                                [sg.Listbox(["parファイルを入力して下さい"], **WINDOW_STYLES["components"]["data_name_part_listbox"])],
                                [sg.T("")],
                                [sg.Submit(**WINDOW_STYLES["components"]["parse_par_to_vi_submit"])],
                            ], **WINDOW_STYLES["components"]["parse_par_to_vi_frame"])
                        ],

                        [sg.T("")],
                        [sg.Submit(**EXTENDABLE_FRAME_STYLES["update"])],
                        [sg.T("")],

                        [sg.Multiline(**WINDOW_STYLES["components"]["output_log"])],
                        [sg.Submit(**WINDOW_STYLES["components"]["write_vi_to_excel_submit"])],
                    ]),
                    sg.Column([
                        [sg.Frame(layout=[], **EXTENDABLE_FRAME_STYLES["frame"])],
                    ]),
                ]
            ], **WINDOW_STYLES["style"]
        )

    def close_window(self):
        """windowを閉じる。
        """
        self.window.close()

    def print_alert(self, *messages: str):
        """警告を出力する。
        """
        [self.window[config.LOG_KEY].print(message, t="red") for message in messages]

    def print_notice(self, *messages: str):
        """noticeを出力する
        """
        [self.window[config.LOG_KEY].print(message, t="green") for message in messages]

    def clear_value(self, component_key: str):
        """値をクリアする。

        Parameters
        ----------
        component_key : str
            クリアするコンポーネントのキー。
        """
        self.window[component_key].update(value="")

    def component_value(self, component_key: str) -> str | bool | int | float:
        """コンポーネントの値を取得する。

        Parameters
        ----------
        component_key : str
            コンポーネントのキー。

        Returns
        -------
        str
            コンポーネントの持つ値。
        """
        return self.window[component_key].get()

    def get_indexes(self, listbox_component_key: str) -> list[int]:
        """Listboxの選択されたインデックスを取得する。n

        Parameters
        ----------
        listbox_component_key : str
            ListBoxのキー。

        Returns
        -------
        list[int]
            選択された要素のインデックス。
        """
        return self.window[listbox_component_key].get_indexes()

    def __validate_container_key(self, component_keys: list[str]) -> None | str:
        """componentのcontainerが共通かどうか検証する。
        コンテナ要素が共通の場合はコンテナ要素のキーを返す。

        Parameters
        ----------
        component_keys : list[str]
            コンポーネントのkeyの配列。

        Returns
        -------
        str
            コンテナ要素のキー
        """
        if len(component_keys) == 1:
            return self.EXTENDABLE_COMPONENTS[component_keys[0]]["container_key"]
        else:
            container_keys = []
            for i in component_keys:
                container_keys.append(self.EXTENDABLE_COMPONENTS[i]["container_key"])
            # 異なるkeyが含まれる場合
            if len(set(container_keys)) >= 2:
                return
            else:
                return container_keys[0]

    def __get_component_info(self, component_key: str):
        """コンポーネントの情報を取得する。
        """
        return self.EXTENDABLE_COMPONENTS[component_key]["method"], \
            self.EXTENDABLE_COMPONENTS[component_key]["style"], \
            self.next_keys[component_key]

    def __create_component(self, component_key: str) -> sg.Element:
        """コンポーネントを生成する。

        Parameters
        ----------
        component_key : str
            コンポーネントのキー。

        Returns
        -------
        sg.Element
            コンポーネント。
        """
        method, style, key_num = self.__get_component_info(component_key)

        # keyを置換したいのでdeepcopyする
        new_style = deepcopy(style)
        key_before_replaced = style["key"]
        new_key = key_before_replaced.replace(config.REPLACED_WORD, str(key_num))
        new_style["key"] = new_key

        component = method(**new_style)

        # インスタンス変数更新
        self.next_keys[component_key] += 1
        self.extended_component_keys[component_key].append(new_key)

        return component

    def add_component_to_container(self, *component_keys: str):
        """コンテナ要素のコンポーネントを追加する。
        """
        # containerが共通かどうか検証(共通ならkeyが返る)
        container_key = self.__validate_container_key(component_keys)
        if not container_key:
            return

        component_row = []
        for component_key in component_keys:
            component_row.append(self.__create_component(component_key))

        if component_row:
            self.window.extend_layout(
                self.window[container_key],
                [component_row]
            )

    def update_component(self, key: str, keyword_and_args: dict):
        """コンポーネントのkeyと{更新したい属性:値}のkwargsを元にコンポーネントを更新する
        """
        self.window[key].update(**keyword_and_args)

    def update_all_resistances(self, values: list[float]):
        """すべての抵抗コンポーネントを更新する。
        """
        [
            self.update_component(key, {"value": value})
            for key, value in zip(self.extended_component_keys[config.EXTENDABLE_RESISTANCE_KEY], values)
        ]

    def update_all_min_voltage(self, values: list[float]):
        """全ての開始電圧コンポーネントを更新する
        """
        [
            self.update_component(key, {"value": value})
            for key, value in zip(self.extended_component_keys[config.EXTENDABLE_MIN_VOLTAGE_KEY], values)
        ]

    def update_all_max_voltage(self, values: list[float]):
        """全ての終了電圧コンポーネントを更新する
        """
        [
            self.update_component(key, {"value": value})
            for key, value in zip(self.extended_component_keys[config.EXTENDABLE_MAX_VOLTAGE_KEY], values)
        ]

    def update_all_judge(self, is_check_array: list[bool]):
        """全てのcheckboxを更新する
        """
        [
            self.update_component(key, {"value": is_check})
            for key, is_check in zip(self.extended_component_keys[config.EXTENDABLE_RESISTANCE_VALIDITY_KEY], is_check_array)
        ]
        self.set_invalid_component_keys()

    def set_invalid_component_keys(self):
        """checkboxの値を見てインスタンス変数を更新する
        """
        for i, checkbox_key in enumerate(self.extended_component_keys[config.EXTENDABLE_RESISTANCE_VALIDITY_KEY]):
            # checkboxがfalseの場合
            if not self.component_value(checkbox_key):
                self.invalid_component_keys[i] = {
                    config.EXTENDABLE_MIN_VOLTAGE_KEY: self.extended_component_keys[config.EXTENDABLE_MIN_VOLTAGE_KEY][i],
                    config.EXTENDABLE_MAX_VOLTAGE_KEY: self.extended_component_keys[config.EXTENDABLE_MAX_VOLTAGE_KEY][i],
                }

    @property
    def all_judges(self) -> list[bool]:
        return [self.component_value(key) for key in self.extended_component_keys[config.EXTENDABLE_RESISTANCE_VALIDITY_KEY]]  # type: ignore
