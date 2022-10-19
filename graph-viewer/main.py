from src.common.exception import InitializeError
from src.view.container.popup import PopupToGetFolderAndMode

popup_get_folder = PopupToGetFolderAndMode()
if folder_and_mode := popup_get_folder.get_folder_and_mode():
    initial_folder, selected_mode = folder_and_mode
    popup_get_folder.close_window()
else:
    raise InitializeError("初期化に失敗しました")


if selected_mode == "通常":
    from src.view.container.components import UserInterface

    print("通常モード")
    ui = UserInterface(initial_folder)
    ui.start_event_loop()
    ui.close_window()
elif selected_mode == "Graphtec":
    from src.view.container.domains.graphtec.components import GraphtecUserInterface

    print("グラフテックモード")
    ui = GraphtecUserInterface(initial_folder)
    ui.start_event_loop()
    ui.close_window
