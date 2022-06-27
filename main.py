from src.Controllers.controller import Controller
from src.Controllers.handler import Handler
from src.Views.view import InterFace


def main():
    interface = InterFace()
    controller = Controller(interface.window)
    handler = Handler(controller)

    while True:
        event, values = interface.window.read()
        handler.handle(event, values)

        if event is None:
            interface.close_window()
            break


if __name__ == "__main__":
    main()
