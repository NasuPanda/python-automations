from __future__ import annotations

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
        # 末尾の改行を消しておく
        data = {"message": "\n" + self.message.strip()}
        requests.post(self.API_URL, headers=headers, data=data)

    def add_message_of_work_update(self, provider: str, updated_work_title_and_url: dict[str, list[str]]) -> None:
        self.message += f"★ {provider}の更新\n"

        if len(updated_work_title_and_url["title"]) == 0:
            self.message += "無し\n"

        for title, url in zip(updated_work_title_and_url["title"], updated_work_title_and_url["url"]):
            self.message += f"{title}\n{url}\n"

        self.message += "\n"
