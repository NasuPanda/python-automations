from src.common import types
from src.common.constants import ComponentKeys
from src.view.presentational import popup


class PopupToGetFolderAndMode:
    def __init__(self) -> None:
        self.window = popup.popup_get_folder_and_mode()

    def get_folder_and_mode(self) -> tuple[str, types.DomainModeOptions] | None:
        while True:
            event, values = self.window.read()  # type: ignore

            if event is None:
                return None

            if event == ComponentKeys.get_folder_popup_submit:
                return (
                    values[ComponentKeys.get_folder_popup_folder_input],
                    values[ComponentKeys.get_folder_popup_select_mode_combo],
                )

    def close_window(self) -> None:
        self.window.close()
