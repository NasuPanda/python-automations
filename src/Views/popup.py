import PySimpleGUI as sg

TITLE = "PowerPointFormatter"
FONT = "MeiryoUI"

WINDOW_STYLES = {
    "title": TITLE,
    "font": FONT,
}


class Popup():
    def __init__(self) -> None:
        pass

    @staticmethod
    def call_error_popup(message="エラー"):
        sg.popup(message, text_color="red", auto_close=True, auto_close_duration=3)

    @staticmethod
    def call_success_popup(message="成功しました"):
        sg.popup_ok(message, auto_close=True, auto_close_duration=2)
