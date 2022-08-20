from __future__ import annotations

from typing import Final

import requests
from credentials import credentials


class LineNotification:
    API_URL: Final = "https://notify-api.line.me/api/notify"

    @classmethod
    def send_notification(cls, message: str) -> None:
        """
        LINEに通知する
        """
        headers = {"Authorization": f"Bearer {credentials.LINE_NOTIFY_TOKEN}"}
        # 末尾の改行を消しておく
        data = {"message": "\n" + message.strip()}
        requests.post(cls.API_URL, headers=headers, data=data)
