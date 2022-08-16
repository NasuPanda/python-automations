from pprint import pprint
from typing import Final

from libs.driver import WebDriver

# TODO
# sqliteに書き出す処理
# 更新有無を確認する処理
# Lineで通知する処理

PROVIDER_URL: Final = "https://tonarinoyj.jp/series"
MANGA_TITLE: Final = "ワンパンマン"

driver = WebDriver()

ongoing_titles_and_latest_episode_url = driver.parse_ongoing_titles_in_tonarinoyj(PROVIDER_URL)
target_manga_latest_episode_url = ongoing_titles_and_latest_episode_url[MANGA_TITLE]
driver.get(target_manga_latest_episode_url)
print(driver.current_title, driver.current_url)

driver.quit()
