from __future__ import annotations

import bs4
from bs4.element import ResultSet, Tag


class ParserError(Exception):
    """Parserクラスのベースエラー"""

    pass


class TagNotFoundError(ParserError):
    """parse時にTagが見つからなかった場合"""

    pass


class Parser:
    def __init__(self, html: str) -> None:
        self._soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html, "html.parser")

    def parse_ongoing_titles(self) -> dict[str, str]:
        ongoing_title_and_latest_episode_url = {}

        ongoing_title_tags = self.__select_tag(".series-table-list")
        for tag in self.__select_tags("li.subpage-table-list-item", ongoing_title_tags):
            manga_title, latest_episode_url = self.select_title_and_latest_episode_url(tag)
            ongoing_title_and_latest_episode_url[manga_title] = latest_episode_url

        return ongoing_title_and_latest_episode_url

    def select_title_and_latest_episode_url(self, manga_tag: Tag) -> tuple[str, str]:
        title = self.__select_tag("h4", tag=manga_tag).get_text()
        link_tag = self.__select_tag(".link-latest a", tag=manga_tag)

        # 見つからなかった場合エラーを投げる
        try:
            latest_episode_url = link_tag["href"]
        except KeyError:
            raise TagNotFoundError(f"Link doesn't exist\n{link_tag}")

        # リストだった場合最初の要素を返す
        if isinstance(latest_episode_url, list):
            latest_episode_url = latest_episode_url[0]
        return title, latest_episode_url

    def __select_tag(self, selector: str, tag: Tag | None = None) -> Tag:
        # tag が引数として渡されなかった場合は self._soup を使う
        result_tag = self._soup.select_one(selector) if tag is None else tag.select_one(selector)
        if result_tag is None:
            raise TagNotFoundError(f"{selector} is invalid selector")
        return result_tag

    def __select_tags(self, selector: str, tag: Tag | None = None) -> ResultSet[Tag]:
        # tag が引数として渡されなかった場合は self._soup を使う
        result_tags = self._soup.select(selector) if tag is None else tag.select(selector)
        if result_tags is None:
            raise TagNotFoundError(f"{selector} is invalid selector")
        return result_tags
