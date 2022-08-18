from libs import common

from .db import DataBase


def create_shosetsu_table(database_path: str) -> None:
    table_info = """
    id integer unique primary key autoincrement,
    ncode string unique,
    title string unique,
    latest_episode_number integer,
    latest_episode_title string
    """
    db = DataBase(
        database_path,
        common.SHOSETSU_TABLE_NAME,
        common.ALL_COLUMNS["shosetsu"],
        common.UPDATABLE_COLUMNS["shosetsu"],
        table_info,
    )

    db.insert(
        ("ncode", "title", "latest_episode_number", "latest_episode_title"),
        common.ShosetsuChangeableValues(
            ncode="n2267be",
            title="Ｒｅ：ゼロから始める異世界生活",
            latest_episode_number=585,
            latest_episode_title="第七章７５　『I know』",
        ),
    )


def create_tonarinoyj_table(database_path: str) -> None:
    table_info = """
    id integer unique primary key autoincrement,
    title string unique,
    latest_episode_url string unique,
    latest_episode_title string unique
    """

    db = DataBase(
        database_path,
        common.TONARINOYJ_TABLE_NAME,
        common.ALL_COLUMNS["tonarinoyj"],
        common.UPDATABLE_COLUMNS["tonarinoyj"],
        table_info,
    )

    db.insert(
        ("title", "latest_episode_url", "latest_episode_title"),
        {
            "title": "ワンパンマン",
            "latest_episode_url": "3270375685396151729",
            "latest_episode_title": "[第214話] ワンパンマン",
        },
    )


def create_jumpplus_table(database_path: str) -> None:
    table_info = """
    id integer unique primary key autoincrement,
    title string unique,
    latest_episode_url string unique,
    latest_episode_title string unique
    """

    db = DataBase(
        database_path,
        common.JUMPPLUS_TABLE_NAME,
        common.ALL_COLUMNS["jumpplus"],
        common.UPDATABLE_COLUMNS["jumpplus"],
        table_info,
    )

    db.insert(
        ("title", "latest_episode_url", "latest_episode_title"),
        {
            "title": "ダンダダン",
            "latest_episode_url": "3269632237310729754",
            "latest_episode_title": "[第69話]ダンダダン",
        },
    )
