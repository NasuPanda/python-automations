from src.common.exception import InitializeError
from src.view.container.components import UserInterface
from src.view.container.popup import PopupToGetFolder


popup_get_folder = PopupToGetFolder()
if initial_folder := popup_get_folder.get_folder():
    popup_get_folder.close_window()
else:
    raise InitializeError("初期化に失敗しました")

ui = UserInterface(initial_folder)
ui.start_event_loop()
ui.close_window()
