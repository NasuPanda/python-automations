from __future__ import annotations

from bs4.element import Tag

from .base import BaseParser, TagNotFoundError


class TonarinoyjParser(BaseParser):
    def __init__(self, html: str) -> None:
        super().__init__(html)

    def parse_ongoing_titles(self) -> dict[str, str]:
        ongoing_titles_and_latest_episode_url = {}

        ongoing_title_tags = self._select_tag(".series-table-list")
        for tag in self._select_tags("li.subpage-table-list-item", ongoing_title_tags):
            manga_title, latest_episode_url = self.select_title_and_latest_episode_url(tag)
            ongoing_titles_and_latest_episode_url[manga_title] = latest_episode_url

        return ongoing_titles_and_latest_episode_url

    def select_title_and_latest_episode_url(self, manga_tag: Tag) -> tuple[str, str]:
        title = self._select_tag("h4", tag=manga_tag).get_text()
        try:
            link_tag = self._select_tag(".link-latest a", tag=manga_tag)
        # NOTE: 最新話のリンクが無い場合1話のみである可能性が高いので1話のリンクを取得
        except TagNotFoundError:
            link_tag = self._select_tag(".link-first-episode a")

        # 見つからなかった場合エラーを投げる
        try:
            latest_episode_url = link_tag["href"]
        except KeyError:
            raise TagNotFoundError(f"Link doesn't exist\n{link_tag}")

        # リストだった場合最初の要素を返す
        if isinstance(latest_episode_url, list):
            latest_episode_url = latest_episode_url[0]
        return title, latest_episode_url


class JumpplusParser(BaseParser):
    def __init__(self, html: str) -> None:
        super().__init__(html)

    def parse_latest_episode_url(self) -> str:
        link_tag = self._select_tag("a.series-episode-list-container")
        try:
            latest_episode_url = link_tag["href"]
        except KeyError:
            raise TagNotFoundError(f"Link doesn't exist\n{link_tag}")

        if isinstance(latest_episode_url, list):
            latest_episode_url = latest_episode_url[0]
        return latest_episode_url


class ShosetsuParser(BaseParser):
    def __init__(self, html: str) -> None:
        super().__init__(html)

    def parse_latest_episode_number_and_title(self) -> tuple[int, str]:
        novel_episode_list = self._select_tags(".novel_sublist2")
        try:
            latest_episode_title = self._select_tag("a", novel_episode_list[-1])
        except IndexError:
            raise TagNotFoundError(f"Link doesn't exist\n{novel_episode_list}")

        latest_episode_number = len(novel_episode_list)
        return latest_episode_number, latest_episode_title.text
