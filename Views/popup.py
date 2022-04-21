import PySimpleGUI as sg

TITLE = "PowerPointFormatter"
FONT = "MeiryoUI"

WINDOW_STYLES = {
    "title": TITLE,
    "font": FONT,
}

CORRESPONDENCES_STYELES = {
    "FRAME": {
        "title": "テキスト置換設定",
        "relief": sg.RELIEF_SOLID,
    },
    "DESC_TEXT": {
        "size": (50, 1),
        "font": (FONT, 15),
    },
    "ALLOW": {
        "size": (5, 1),
        "font": (FONT, 15),
    },
    "TEXT_PLACEHOLDER": {
        "size": (20, 1),
        "font": (FONT, 15)
    },
    "COMBO": {
        "values": ["データ名", "連番"],
        "default_value": "データ名",
        "size": (20, 1),
    },
    "SUBMIT": {
        "key": "-SUBMIT-",
    }
}


class CorrespondencesPopup():
    def __init__(self, texts: list[str]) -> None:
        self.window = sg.Window(
            layout=[
                [sg.T("①テキストの置換を設定してください", **CORRESPONDENCES_STYELES["DESC_TEXT"])],
                [sg.T("②入力が完了したら「入力完了」ボタンを押してください", **CORRESPONDENCES_STYELES["DESC_TEXT"])],
                [
                    [
                        sg.T(text, **CORRESPONDENCES_STYELES["TEXT_PLACEHOLDER"]),
                        sg.T(" → ", **CORRESPONDENCES_STYELES["ALLOW"]),
                        sg.Combo(key=text, **CORRESPONDENCES_STYELES["COMBO"])
                    ]
                    for text in texts
                ],
                [sg.B("入力完了", **CORRESPONDENCES_STYELES["SUBMIT"])],
            ],
            **WINDOW_STYLES,
        )

    def get_input(self):
        """ユーザーから入力を受け取る"""
        while True:
            event, values = self.window.read()

            if event is None:
                result = []
                break

            if event == "-SUBMIT-":
                result = values
                break

        self.window.close()
        return result
