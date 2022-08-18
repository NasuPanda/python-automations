from __future__ import annotations

import bs4
from bs4.element import ResultSet, Tag


class ParserError(Exception):
    """Parserクラスのベースエラー"""

    pass


class TagNotFoundError(ParserError):
    """parse時にTagが見つからなかった場合"""

    pass


class BaseParser:
    def __init__(self, html: str) -> None:
        self._soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html, "html.parser")

    def _select_tag(self, selector: str, tag: Tag | None = None) -> Tag:
        # tag が引数として渡されなかった場合は self._soup を使う
        result_tag = self._soup.select_one(selector) if tag is None else tag.select_one(selector)
        if result_tag is None:
            raise TagNotFoundError(f"{selector} is invalid selector")
        return result_tag

    def _select_tags(self, selector: str, tag: Tag | None = None) -> ResultSet[Tag]:
        # tag が引数として渡されなかった場合は self._soup を使う
        result_tags = self._soup.select(selector) if tag is None else tag.select(selector)
        if result_tags is None:
            raise TagNotFoundError(f"{selector} is invalid selector")
        return result_tags
