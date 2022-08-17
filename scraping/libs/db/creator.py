from .db import DataBase

PROVIDER_TABLE_NAME = "providers"
WORKS_TABLE_NAME = "works"


def create_providers_table(database_path: str) -> None:
    table_info = """
    id integer unique primary key autoincrement,
    name string unique,
    series_domain string unique
    episode_domain string unique
    """

    db = DataBase(database_path, PROVIDER_TABLE_NAME, table_info)

    db.insert(
        ("name", "series_domain"),
        {"name": "となりのヤングジャンプ", "series_domain": "tonarinoyj.jp/series", "episode_domain": "tonarinoyj.jp/episode"},
        {
            "name": "少年ジャンププラス",
            "series_domain": "shonenjumpplus.com/series",
            "episode_domain": "shonenjumpplus.com/episode",
        },
        {"name": "小説家になろう", "series_domain": "syosetu.com/", "episode_domain": "hoge"},
    )

    db.close()


def create_works_table(database_path: str) -> None:
    table_info = f"""
    id integer unique, primary key autoincrement,
    title string unique,
    latest_episode_url string unique,
    latest_episode_title string unique,
    foreign key(provider_id) references {PROVIDER_TABLE_NAME}
    """

    db = DataBase(database_path, WORKS_TABLE_NAME, table_info)

    db.insert(
        ("title", "latest_episode_url", "latest_episode_title", "provider_id"),
        {
            "title": "ワンパンマン",
            "latest_episode_url": "3270375685396151729",
            "latest_episode_title": "[第214話] ワンパンマン",
            "provider_id": 1,
        },
    )
