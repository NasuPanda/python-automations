from typing import Final

import requests
from credentials import credentials


class LineNotification:
    API_URL: Final = "https://notify-api.line.me/api/notify"

    def __init__(self) -> None:
        self.message: str = ""

    def send_notification(self) -> None:
        """
        LINEに通知する
        """
        headers = {"Authorization": f"Bearer {credentials.LINE_NOTIFY_TOKEN}"}
        data = {"message": f"message: {self.message}"}
        requests.post(self.API_URL, headers=headers, data=data)

    def add_message(self, message: str) -> None:
        self.message += "\n" + message
