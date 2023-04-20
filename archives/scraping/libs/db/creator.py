from libs import common

from .db import DataBase


def create_shosetsu_table(database_path: str, insert_values: list[common.ShosetsuChangeableValues]) -> None:
    """DBに小説家になろう用のテーブルを生成する。

    Args:
        database_path (str): DBのパス。
        insert_values (list[common.ShosetsuChangeableValues]): 作成したテーブルに書き込むデータ。
    """

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

    [db.insert(i) for i in insert_values]


def create_tonarinoyj_table(database_path: str, insert_values: list[common.TonarinoyjChangeableValues]) -> None:
    """DBにとなりのヤングジャンプ用のテーブルを生成する。

    Args:
        database_path (str): DBのパス。
        insert_values (list[common.TonarinoyjChangeableValues]): 作成したテーブルに書き込むデータ。
    """

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

    [db.insert(i) for i in insert_values]


def create_jumpplus_table(database_path: str, insert_values: list[common.JumpplusChangeableValues]) -> None:
    """DBにジャンププラス用のテーブルを生成する。

    Args:
        database_path (str): DBのパス。
        insert_values (list[common.JumpplusChangeableValues]): 作成したテーブルに書き込むデータ。
    """

    table_info = """
    id integer unique primary key autoincrement,
    title string unique,
    first_episode_url string unique,
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

    [db.insert(i) for i in insert_values]
