from src.common.constants import ComponentKeys
from src.view.presentational import popup


class PopupToGetFolder:
    def __init__(self) -> None:
        self.window = popup.popup_get_folder()

    def get_folder(self) -> str | None:
        while True:
            event, values = self.window.read()  # type: ignore

            if event is None:
                return None

            if event == ComponentKeys.get_folder_popup_submit:
                return values[ComponentKeys.get_folder_popup_folder_input]

    def close_window(self) -> None:
        self.window.close()
