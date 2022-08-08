from __future__ import annotations  # 型アノテーション用

from pprint import pprint

import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def find_latest_url_by_title(page_source: str, title: str) -> str | None:
    soup = bs4.BeautifulSoup(page_source, "html.parser")
    manga_title_tag = soup.select_one(f"h4:-soup-contains('{title}')")
    try:
        manga_container = manga_title_tag.parent.parent
    except AttributeError as e:
        print(e)
        return None
    latest_episode_link = manga_container.select_one(".episode-link-container .link-latest a")
    if latest_episode_link:
        latest_episode_url = latest_episode_link["href"]
        if isinstance(latest_episode_url, str):
            return latest_episode_url


def find_latest_episode_url_and_title_by_title():
    url = "https://tonarinoyj.jp/series"
    manga_title = "ワンパンマン"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    latest_episode_url = find_latest_url_by_title(driver.page_source, manga_title)

    # タイトルとURLの取得
    driver.get(latest_episode_url)
    latest_episode_title = driver.title

    driver.quit()

    print(f"{latest_episode_title} : {latest_episode_url}")
