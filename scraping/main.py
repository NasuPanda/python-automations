from __future__ import annotations

from libs import common
from libs.db.db import DataBase
from libs.driver import WebDriver
from libs.line import LineNotification


def find_latest_url_in_tonarinoyj(manga_titles: list[str]) -> dict[str, list[str]]:
    updated_titles_and_urls: dict[str, list[str]] = {"title": [], "url": []}
    driver = WebDriver()
    db = DataBase(
        "./db/DATA.db",
        "tonarinoyj",
        ("id", "title", "latest_episode_title", "latest_episode_url"),
        ("title", "latest_episode_title", "latest_episode_url"),
    )

    for manga_title in manga_titles:
        # 最新話のURLを取得
        ongoing_titles_and_latest_episode_url = driver.parse_ongoing_titles_in_tonarinoyj()
        latest_episode_url = ongoing_titles_and_latest_episode_url[manga_title]
        # 最新話のタイトルを取得
        driver.get(latest_episode_url)
        latest_episode_title = driver.current_title

        record_before_update = db.select(("latest_episode_url", "latest_episode_title"), where={"title": "ワンパンマン"})[0]

        if latest_episode_url != record_before_update["latest_episode_url"]:  # type: ignore
            db.update(
                {"latest_episode_url": latest_episode_url, "latest_episode_title": latest_episode_title},
                {"title": manga_title},
            )

            updated_titles_and_urls["title"].append(latest_episode_title)
            updated_titles_and_urls["url"].append(latest_episode_url)

    driver.quit()
    return updated_titles_and_urls


def find_latest_url_in_jumpplus(manga_titles: list[str]) -> dict[str, list[str]]:
    updated_titles_and_urls: dict[str, list[str]] = {"title": [], "url": []}
    driver = WebDriver(headless=False)
    db = DataBase(
        "./db/DATA.db",
        common.JUMPPLUS_TABLE_NAME,
        common.ALL_COLUMNS["jumpplus"],
        common.UPDATABLE_COLUMNS["jumpplus"],
    )

    for manga_title in manga_titles:
        record_before_update = db.select(("*",), {"title": manga_title})[0]

        # 最新話のURLとタイトルを取得する処理
        latest_episode_url = driver.parse_latest_episode_url_in_jumpplus(record_before_update["first_episode_url"])  # type: ignore
        driver.get(latest_episode_url)
        latest_episode_title = driver.current_title

        if latest_episode_url != record_before_update["latest_episode_url"]:  # type: ignore
            db.update(
                {"latest_episode_url": latest_episode_url, "latest_episode_title": latest_episode_title},
                {"title": manga_title},
            )
            updated_titles_and_urls["title"].append(latest_episode_title)
            updated_titles_and_urls["url"].append(latest_episode_url)

    driver.quit()
    return updated_titles_and_urls


def find_latest_url_in_shosetsu(novel_titles: list[str]) -> dict[str, list[str]]:
    updated_titles_and_urls: dict[str, list[str]] = {"title": [], "url": []}
    driver = WebDriver()
    db = DataBase(
        "./db/DATA.db",
        common.SHOSETSU_TABLE_NAME,
        common.ALL_COLUMNS["shosetsu"],
        common.UPDATABLE_COLUMNS["shosetsu"],
    )

    for novel_title in novel_titles:
        current_record = db.select(("*",), {"title": novel_title})[0]
        latest_episode_number, latest_episode_title = driver.parse_tracking_title_in_shosetsu(current_record["ncode"])  # type: ignore

        # 判定部分
        if latest_episode_number != current_record["latest_episode_number"]:  # type: ignore
            db.update(
                {"latest_episode_number": latest_episode_number, "latest_episode_title": latest_episode_title},
                {"title": novel_title},
            )
            # エピソードのタイトルに作品のタイトルが含まれないので別途追加しておく
            updated_titles_and_urls["title"].append(f"title: {novel_title}\n{latest_episode_title}")
            updated_titles_and_urls["url"].append(
                rf"{common.PROVIDER_URLS['shosetsu']}/{current_record['ncode']}/{latest_episode_number}"
            )

    return updated_titles_and_urls


def message_of_works_update(provider: str, updated_work_title_and_url: dict[str, list[str]]) -> str:
    message = f"★ {provider}の更新\n"

    if len(updated_work_title_and_url["title"]) == 0:
        message += "無し\n"
        return message

    for title, url in zip(updated_work_title_and_url["title"], updated_work_title_and_url["url"]):
        message += f"{title}\n{url}\n"

    message += "\n"

    return message


def main() -> None:
    tonarinoyj_manga_titles = ["ワンパンマン", "超人X"]
    jumpplus_manga_titles = [
        "ダンダダン",
        "マリッジトキシン",
        "エクソシストを堕とせない",
        "【推しの子】",
        "君のことが大大大大大好きな100人の彼女",
        "ハイパーインフレーション",
        "左ききのエレン",
        "2.5次元の誘惑",
        "ドラゴンクエスト ダイの大冒険 勇者アバンと獄炎の魔王",
    ]
    shosetsu_novel_titles = ["Ｒｅ：ゼロから始める異世界生活", "シャングリラ・フロンティア〜クソゲーハンター、神ゲーに挑まんとす〜"]

    LineNotification.send_notification(
        message_of_works_update("となりのヤングジャンプ", find_latest_url_in_tonarinoyj(tonarinoyj_manga_titles))
    )
    LineNotification.send_notification(
        message_of_works_update("少年ジャンププラス", find_latest_url_in_jumpplus(jumpplus_manga_titles))
    )
    LineNotification.send_notification(
        message_of_works_update("小説家になろう", find_latest_url_in_shosetsu(shosetsu_novel_titles))
    )


if __name__ == "__main__":
    main()
