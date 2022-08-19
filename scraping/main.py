from pprint import pprint
from typing import Final

from libs import common
from libs.db.db import DataBase
from libs.driver import WebDriver

# TODO
# ジャンプラのパース
# なろうのパース
# 更新を検知したらLineで通知する処理


def find_latest_url_in_tonarinoyj() -> None:
    MANGA_TITLE: Final = "ワンパンマン"

    driver = WebDriver()

    # 最新話のURLとタイトルを取得する処理
    ongoing_titles_and_latest_episode_url = driver.parse_ongoing_titles_in_tonarinoyj()
    target_manga_latest_episode_url = ongoing_titles_and_latest_episode_url[MANGA_TITLE]
    driver.get(target_manga_latest_episode_url)
    latest_episode_title, latest_episode_url = driver.current_title, driver.current_url
    print("latest: ", latest_episode_url, latest_episode_title)

    driver.quit()

    # データベースにアクセス、更新する処理
    db = DataBase(
        "./db/DATA.db",
        "tonarinoyj",
        ("id", "title", "latest_episode_title", "latest_episode_url"),
        ("title", "latest_episode_title", "latest_episode_url"),
    )

    current_record = db.select(("latest_episode_url", "latest_episode_title"), where={"title": "ワンパンマン"})[0]

    # 判定部分
    if latest_episode_url != current_record["latest_episode_url"]:  # type: ignore
        print("needs update!")

        print("before_update", current_record)
        db.update(
            {"latest_episode_url": latest_episode_url, "latest_episode_title": latest_episode_title},
            {"title": "ワンパンマン"},
        )
        print("after update", db.select(("latest_episode_url", "latest_episode_title"), where={"title": "ワンパンマン"})[0])
    else:
        print("doesn't need update!")


def find_latest_url_in_jumpplus() -> None:
    MANGA_TITLE: Final = "ダンダダン"

    db = DataBase(
        "./db/DATA.db",
        common.JUMPPLUS_TABLE_NAME,
        common.ALL_COLUMNS["jumpplus"],
        common.UPDATABLE_COLUMNS["jumpplus"],
    )
    current_record = db.select(("*",), {"title": MANGA_TITLE})[0]

    driver = WebDriver(headless=False)

    # 最新話のURLとタイトルを取得する処理
    latest_episode_url = driver.parse_latest_episode_url_in_jumpplus(current_record["first_episode_url"])  # type: ignore
    driver.get(latest_episode_url)
    latest_episode_title = driver.current_title
    print("latest: ", latest_episode_url, latest_episode_title)

    driver.quit()

    # 判定部分
    if latest_episode_url != current_record["latest_episode_url"]:  # type: ignore
        print("needs update!")

        print("before_update", current_record)
        db.update(
            {"latest_episode_url": latest_episode_url, "latest_episode_title": latest_episode_title},
            {"title": "ダンダダン"},
        )
        print("after update", db.select(("latest_episode_url", "latest_episode_title"), where={"title": "ダンダダン"})[0])
    else:
        print("doesn't need update!")


def find_latest_url_in_shosetsu() -> None:
    SHOSETSU_TITLE = "Ｒｅ：ゼロから始める異世界生活"

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
        print("needs update!")

        print("before_update", current_record)
        db.update(
            {"latest_episode_number": latest_episode_number, "latest_episode_title": latest_episode_title},
            {"title": SHOSETSU_TITLE},
        )
        print(
            "after update",
            db.select(("latest_episode_number", "latest_episode_title"), where={"title": SHOSETSU_TITLE})[0],
        )
    else:
        print("doesn't need update!")


def main() -> None:
    find_latest_url_in_jumpplus()
    find_latest_url_in_tonarinoyj()
    find_latest_url_in_shosetsu()


if __name__ == "__main__":
    main()
