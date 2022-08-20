import os

from libs import common
from libs.db import creator

DATABASE_PATH = os.path.abspath("./db/DATA.db")


shosetsu_insert_values: list[common.ShosetsuChangeableValues] = [
    common.ShosetsuChangeableValues(
        ncode="n2267be",
        title="Ｒｅ：ゼロから始める異世界生活",
        latest_episode_number=584,
        latest_episode_title=r"第七章７４　『イドラ・ミサンガ』",
    ),
    common.ShosetsuChangeableValues(
        ncode="n6169dz",
        title="シャングリラ・フロンティア〜クソゲーハンター、神ゲーに挑まんとす〜",
        latest_episode_number=856,
        latest_episode_title=r"12月19日：艱難真紅にこそ笑う",
    ),
]

tonarinoyj_insert_values: list[common.TonarinoyjChangeableValues] = [
    {
        "title": "ワンパンマン",
        "latest_episode_url": r"https://tonarinoyj.jp/episode/3270375685396151729",
        "latest_episode_title": "[第214話] ワンパンマン",
    },
    {
        "title": "超人X",
        "latest_episode_url": r"https://tonarinoyj.jp/episode/3270375685401560947",
        "latest_episode_title": "[第26-1話] 超人X",
    },
]

jumpplus_insert_values: list[common.JumpplusChangeableValues] = [
    {
        "title": "ダンダダン",
        "first_episode_url": r"https://shonenjumpplus.com/episode/3269632237310729754",
        "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685401141568",
        "latest_episode_title": "[第68話]ダンダダン",
    },
    {
        "title": "マリッジトキシン",
        "first_episode_url": r"https://shonenjumpplus.com/episode/3269754496881854355",
        "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685411795919",
        "latest_episode_title": "[16話]マリッジトキシン",
    },
    {
        "title": "エクソシストを堕とせない",
        "first_episode_url": r"https://shonenjumpplus.com/episode/3269754496649675685",
        "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685372374256",
        "latest_episode_title": "[19話]エクソシストを堕とせない",
    },
    {
        "title": "【推しの子】",
        "first_episode_url": r"https://shonenjumpplus.com/episode/13933686331661632099",
        "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685428994645",
        "latest_episode_title": "[番外編29]【推しの子】",
    },
    {
        "title": "君のことが大大大大大好きな100人の彼女",
        "first_episode_url": r"https://shonenjumpplus.com/episode/13933686331623812157",
        "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685412227502",
        "latest_episode_title": "[第107話]君のことが大大大大大好きな100人の彼女",
    },
    {
        "title": "ハイパーインフレーション",
        "first_episode_url": r"https://shonenjumpplus.com/episode/13933686331749163174",
        "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685393122169",
        "latest_episode_title": "[43話]ハイパーインフレーション",
    },
    {
        "title": "左ききのエレン",
        "first_episode_url": r"https://shonenjumpplus.com/episode/13932016480029111789",
        "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685412227862",
        "latest_episode_title": "[200話]左ききのエレン",
    },
    {
        "title": "2.5次元の誘惑",
        "first_episode_url": r"https://shonenjumpplus.com/episode/13933686331679642476",
        "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685412227832",
        "latest_episode_title": "[休載イラスト42]2.5次元の誘惑",
    },
    {
        "title": "ドラゴンクエスト ダイの大冒険 勇者アバンと獄炎の魔王",
        "first_episode_url": r"https://shonenjumpplus.com/episode/3269754496819320015",
        "latest_episode_url": r"https://shonenjumpplus.com/episode/3270375685412227889",
        "latest_episode_title": "[第22話 前編]ドラゴンクエスト ダイの大冒険 勇者アバンと獄炎の魔王",
    },
]

creator.create_shosetsu_table(DATABASE_PATH, shosetsu_insert_values)
creator.create_tonarinoyj_table(DATABASE_PATH, tonarinoyj_insert_values)
creator.create_jumpplus_table(DATABASE_PATH, jumpplus_insert_values)
