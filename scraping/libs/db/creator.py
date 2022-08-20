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
        common.ShosetsuChangeableValues(
            ncode="n2267be",
            title="Ｒｅ：ゼロから始める異世界生活",
            latest_episode_number=584,
            latest_episode_title=r"第七章７４　『イドラ・ミサンガ』",
        ),
    )
    db.insert(
        common.ShosetsuChangeableValues(
            ncode="n6169dz",
            title="シャングリラ・フロンティア〜クソゲーハンター、神ゲーに挑まんとす〜",
            latest_episode_number=856,
            latest_episode_title=r"12月19日：艱難真紅にこそ笑う",
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
        {
            "title": "ワンパンマン",
            "latest_episode_url": r"https://tonarinoyj.jp/episode/3270375685396151729",
            "latest_episode_title": "[第214話] ワンパンマン",
        },
    )
    db.insert(
        {
            "title": "超人X",
            "latest_episode_url": r"https://tonarinoyj.jp/episode/3270375685401560947",
            "latest_episode_title": "[第26-1話] 超人X",
        },
    )


def create_jumpplus_table(database_path: str) -> None:
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

    db.insert(
        {
            "title": "ダンダダン",
            "first_episode_url": r"https://shonenjumpplus.com/episode/3269632237310729754",
            "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685401141568",
            "latest_episode_title": "[第68話]ダンダダン",
        },
    )

    db.insert(
        {
            "title": "マリッジトキシン",
            "first_episode_url": r"https://shonenjumpplus.com/episode/3269754496881854355",
            "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685411795919",
            "latest_episode_title": "[16話]マリッジトキシン",
        },
    )

    db.insert(
        {
            "title": "エクソシストを堕とせない",
            "first_episode_url": r"https://shonenjumpplus.com/episode/3269754496649675685",
            "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685372374256",
            "latest_episode_title": "[19話]エクソシストを堕とせない",
        },
    )

    db.insert(
        {
            "title": "【推しの子】",
            "first_episode_url": r"https://shonenjumpplus.com/episode/13933686331661632099",
            "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685428994645",
            "latest_episode_title": "[番外編29]【推しの子】",
        },
    )

    db.insert(
        {
            "title": "君のことが大大大大大好きな100人の彼女",
            "first_episode_url": r"https://shonenjumpplus.com/episode/13933686331623812157",
            "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685412227502",
            "latest_episode_title": "[第107話]君のことが大大大大大好きな100人の彼女",
        },
    )

    db.insert(
        {
            "title": "ハイパーインフレーション",
            "first_episode_url": r"https://shonenjumpplus.com/episode/13933686331749163174",
            "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685393122169",
            "latest_episode_title": "[43話]ハイパーインフレーション",
        },
    )

    db.insert(
        {
            "title": "左ききのエレン",
            "first_episode_url": r"https://shonenjumpplus.com/episode/13932016480029111789",
            "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685412227862",
            "latest_episode_title": "[200話]左ききのエレン",
        },
    )

    db.insert(
        {
            "title": "2.5次元の誘惑",
            "first_episode_url": r"https://shonenjumpplus.com/episode/13933686331679642476",
            "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685412227832",
            "latest_episode_title": "[休載イラスト42]2.5次元の誘惑",
        },
    )

    db.insert(
        {
            "title": "ドラゴンクエスト ダイの大冒険 勇者アバンと獄炎の魔王",
            "first_episode_url": r"https://shonenjumpplus.com/episode/3269754496819320015",
            "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685412227889",
            "latest_episode_title": "[第22話 前編]ドラゴンクエスト ダイの大冒険 勇者アバンと獄炎の魔王",
        },
    )
