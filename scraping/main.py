from __future__ import annotations

from turtle import update
from typing import Final

from libs import common
from libs.db.db import DataBase
from libs.driver import WebDriver
from libs.line import LineNotification


def find_latest_url_in_tonarinoyj() -> dict[str, list[str]]:
    # TODO 対象のタイトルは外からリストとして渡す
    MANGA_TITLE: Final = "ワンパンマン"

    updated_titles_and_urls: dict[str, list[str]] = {"title": [], "url": []}

    driver = WebDriver()

    # 最新話のURLとタイトルを取得する処理
    ongoing_titles_and_latest_episode_url = driver.parse_ongoing_titles_in_tonarinoyj()
    target_manga_latest_episode_url = ongoing_titles_and_latest_episode_url[MANGA_TITLE]

    driver.get(target_manga_latest_episode_url)
    latest_episode_title, latest_episode_url = driver.current_title, driver.current_url
    driver.quit()

    db = DataBase(
        "./db/DATA.db",
        "tonarinoyj",
        ("id", "title", "latest_episode_title", "latest_episode_url"),
        ("title", "latest_episode_title", "latest_episode_url"),
    )
    record_before_update = db.select(("latest_episode_url", "latest_episode_title"), where={"title": "ワンパンマン"})[0]

    if latest_episode_url != record_before_update["latest_episode_url"]:  # type: ignore
        db.update(
            {"latest_episode_url": latest_episode_url, "latest_episode_title": latest_episode_title},
            {"title": "ワンパンマン"},
        )

        updated_titles_and_urls["title"].append(latest_episode_title)
        updated_titles_and_urls["url"].append(latest_episode_url)

    return updated_titles_and_urls


def find_latest_url_in_jumpplus() -> dict[str, list[str]]:
    MANGA_TITLE: Final = "ダンダダン"

    updated_titles_and_urls: dict[str, list[str]] = {"title": [], "url": []}

    db = DataBase(
        "./db/DATA.db",
        common.JUMPPLUS_TABLE_NAME,
        common.ALL_COLUMNS["jumpplus"],
        common.UPDATABLE_COLUMNS["jumpplus"],
    )
    record_before_update = db.select(("*",), {"title": MANGA_TITLE})[0]

    driver = WebDriver(headless=False)

    # 最新話のURLとタイトルを取得する処理
    latest_episode_url = driver.parse_latest_episode_url_in_jumpplus(record_before_update["first_episode_url"])  # type: ignore
    driver.get(latest_episode_url)
    latest_episode_title = driver.current_title
    driver.quit()

    if latest_episode_url != record_before_update["latest_episode_url"]:  # type: ignore
        db.update(
            {"latest_episode_url": latest_episode_url, "latest_episode_title": latest_episode_title},
            {"title": "ダンダダン"},
        )
        updated_titles_and_urls["title"].append(latest_episode_title)
        updated_titles_and_urls["url"].append(latest_episode_url)

    return updated_titles_and_urls


def find_latest_url_in_shosetsu() -> dict[str, list[str]]:
    SHOSETSU_TITLE = "Ｒｅ：ゼロから始める異世界生活"
    updated_titles_and_urls: dict[str, list[str]] = {"title": [], "url": []}

    db = DataBase(
        "./db/DATA.db",
        common.SHOSETSU_TABLE_NAME,
        common.ALL_COLUMNS["shosetsu"],
        common.UPDATABLE_COLUMNS["shosetsu"],
    )
    current_record = db.select(("*",), {"title": SHOSETSU_TITLE})[0]

    driver = WebDriver()
    latest_episode_number, latest_episode_title = driver.parse_tracking_title_in_shosetsu(current_record["ncode"])  # type: ignore

    # 判定部分
    if latest_episode_number != current_record["latest_episode_number"]:  # type: ignore
        db.update(
            {"latest_episode_number": latest_episode_number, "latest_episode_title": latest_episode_title},
            {"title": SHOSETSU_TITLE},
        )
        updated_titles_and_urls["title"].append(latest_episode_title)
        updated_titles_and_urls["url"].append(f"{common.PROVIDER_URLS['shosetsu']}{latest_episode_number}")

    return updated_titles_and_urls


def main() -> None:
    line_notification = LineNotification()
    line_notification.add_message_of_work_update("となりのヤングジャンプ", find_latest_url_in_tonarinoyj())
    line_notification.add_message_of_work_update("少年ジャンププラス", find_latest_url_in_jumpplus())
    line_notification.add_message_of_work_update("小説家になろう", find_latest_url_in_shosetsu())
    print(line_notification.message)
    line_notification.send_notification()


if __name__ == "__main__":
    main()
