from __future__ import annotations

from typing import Final, Literal, TypedDict, Union

PROVIDER_URLS: Final = {
    "jumpplus": "https://shonenjumpplus.com/series",
    "tonarinoyj": "https://tonarinoyj.jp/series",
    "shosetsu": "https://ncode.syosetu.com/",
}

SHOSETSU_TABLE_NAME: Final = "shosetsu"
JUMPPLUS_TABLE_NAME: Final = "jumpplus"
TONARINOYJ_TABLE_NAME: Final = "tonarinoyj"

ALL_COLUMNS: Final = {
    "jumpplus": ("id", "title", "first_episode_url", "latest_episode_title", "latest_episode_url"),
    "tonarinoyj": ("id", "title", "latest_episode_title", "latest_episode_url"),
    "shosetsu": (
        "id",
        "ncode",
        "title",
        "latest_episode_number",
        "latest_episode_title",
    ),
}

UPDATABLE_COLUMNS: Final = {
    "jumpplus": ("title", "first_episode_url", "latest_episode_title", "latest_episode_url"),
    "tonarinoyj": ("title", "latest_episode_title", "latest_episode_url"),
    "shosetsu": (
        "ncode",
        "title",
        "latest_episode_number",
        "latest_episode_title",
    ),
}

LOGICAL_OPERATOR = Literal["AND", "OR"]


class UpdatedTitlesAndUrls(TypedDict):
    title: list[str]
    url: list[str]


class JumpplusChangeableValues(TypedDict, total=False):
    title: str
    first_episode_url: str
    latest_episode_title: str
    latest_episode_url: str


class TonarinoyjChangeableValues(TypedDict, total=False):
    title: str
    latest_episode_title: str
    latest_episode_url: str


class ShosetsuChangeableValues(TypedDict, total=False):
    ncode: str
    title: str
    latest_episode_number: int
    latest_episode_title: str


CHANGEABLE_VALUES = Union[JumpplusChangeableValues, TonarinoyjChangeableValues, ShosetsuChangeableValues]
