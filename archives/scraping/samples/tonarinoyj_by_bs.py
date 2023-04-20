from __future__ import annotations

from typing import Final  # 型アノテーション用

import bs4
from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

PROVIDER_URL: Final = "https://tonarinoyj.jp/series"
MANGA_TITLE: Final = "ワンパンマン"


def find_latest_episode_url_by_title(page_source: str, title: str) -> str | None:
    """タイトルを元に最新話のURLを取得"""
    soup = bs4.BeautifulSoup(page_source, "html.parser")
    manga_title_tag = soup.select_one(f"h4:-soup-contains('{title}')")

    if isinstance(manga_title_tag, Tag) and isinstance(manga_title_tag.parent, Tag):
        manga_container = manga_title_tag.parent.parent
    else:
        return None

    if isinstance(manga_container, Tag):
        latest_episode_link = manga_container.select_one(".episode-link-container .link-latest a")
    else:
        return None

    if isinstance(latest_episode_link, Tag):
        latest_episode_url = latest_episode_link["href"]
        if isinstance(latest_episode_url, str):
            return latest_episode_url
    else:
        return None


def find_latest_episode_url_and_title_by_title() -> None:
    """タイトルを元に最新話のURL・タイトルを取得"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(PROVIDER_URL)

    latest_episode_url = find_latest_episode__url_by_title(driver.page_source, MANGA_TITLE)

    if latest_episode_url:
        driver.get(latest_episode_url)
        latest_episode_title = driver.title
        print(f"{latest_episode_title} : {latest_episode_url}")

    driver.quit()


def find_titles_and_latest_episode_url():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(PROVIDER_URL)

    soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
    ongoing_titles = soup.select_one(".series-table-list")
    if isinstance(ongoing_titles, bs4.element.Tag):
        for i, tag in enumerate(ongoing_titles.select("li.subpage-table-list-item")):
            title = tag.select_one("h4")
            link = tag.select_one(".link-latest a")

            # 漫画のタイトルを取得
            if isinstance(title, bs4.element.Tag):
                manga_title = title.get_text()
                print(manga_title)

            # 最新話のURLとタイトルを取得
            if isinstance(link, bs4.element.Tag):
                latest_episode_url = link["href"]

                driver.get(latest_episode_url)  # type: ignore
                latest_episode_title = driver.title

                print(latest_episode_url)
                print(latest_episode_title)
    else:
        print("Not found.")

    driver.quit()
