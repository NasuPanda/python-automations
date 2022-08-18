from pprint import pprint
from typing import Final

from libs import common
from libs.db.db import DataBase
from libs.driver import WebDriver

# TODO
# 更新有無を確認する処理
# Lineで通知する処理

MANGA_TITLE: Final = "ワンパンマン"

driver = WebDriver()

# 最新話のURLとタイトルを取得する処理
ongoing_titles_and_latest_episode_url = driver.parse_ongoing_titles_in_tonarinoyj()
target_manga_latest_episode_url = ongoing_titles_and_latest_episode_url[MANGA_TITLE]
driver.get(target_manga_latest_episode_url)
print(driver.current_title, driver.current_url)

driver.quit()

# データベースにアクセス、更新する処理
db = DataBase(
    "./db/DATA.db",
    "tonarinoyj",
    ("id", "title", "latest_episode_title", "latest_episode_url"),
    ("title", "latest_episode_title", "latest_episode_url"),
)
print("before", db.select(("*",)))
db.update(
    {"title": "ワンパンマン"},
    {"title": "ワンパンマン", "id": 1},
    "OR",
)
print("after", db.select(("*",)))
