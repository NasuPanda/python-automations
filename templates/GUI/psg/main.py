"""サンプルGUI"""
from gui.container.ui import UserInterface


def main() -> None:
    ui = UserInterface()
    ui.init_window()


if __name__ == "__main__":
    main()
