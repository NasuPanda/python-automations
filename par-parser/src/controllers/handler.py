from typing import Callable

import config
from src.controllers.controller import Controller


class Handler:
    """イベントハンドラー。

    Instance variables
    ----------
    controller: Controller
        Controllerクラスのインスタンス。
    functions: dict[str, Callable]
        {event: self.controller.method} 形式の辞書。
    """
    def __init__(self, controller: Controller) -> None:
        """インスタンスの初期化。

        Parameters
        ----------
        controller : Controller
            Controllerクラスのインスタンス。
        """
        self.controller: Controller = controller
        self.functions: dict[str, Callable] = {
            # event: self.controller.method
            config.SRC_FOLDER_INPUT_KEY: self.controller.receive_par_folder,
            config.SHEET_PER_FILE_INPUT_KEY: self.controller.receive_sheets_per_file,
            config.SELECT_DATA_NAME_PART_LISTBOX_KEY: self.controller.sort_par_paths,
            config.SELECT_MODE_COMBO_KEY: self.controller.receive_experiment_mode,
            config.PARSE_PAR_TO_VI_SUBMIT_KEY: self.controller.parse_par_to_vi_data,
            config.UPDATE_RESISTANCE_KEY: self.controller.update_vi_data,
            config.WRITE_VI_DATA_TO_EXCEL_SUBMIT_KEY: self.controller.write_vi_data_to_excel,
        }

    def handle(self, key: str):
        """イベントのハンドリングを行う。

        Parameters
        ----------
        key : str
            発火したイベントのキー。
        """
        if key not in self.functions:
            return
        event = self.functions[key]
        event()
