import os
from typing import Any

import colorama
from termcolor import cprint

from common import utils
from common.constants import CLI_COLORS, DATA_FILE_EXTENSION

colorama.init()


def print_default(*texts: str):
    [print(text) for text in texts]


def print_notices(*texts: str):
    [cprint(text, CLI_COLORS["notice"]) for text in texts]


def print_alerts(*texts: str):
    [cprint(text, CLI_COLORS["alert"]) for text in texts]


def print_section(*texts: str):
    margin = "* " * 20
    cprint(margin, CLI_COLORS["section"])
    [cprint(text, CLI_COLORS["section"]) for text in texts]
    cprint(margin, CLI_COLORS["section"])


def get_filepath(message: str, extension: str = ".xlsx") -> str:
    print_notices(f"{message} 拡張子: {extension}")

    while True:
        # NOTE: パスのコピペが想定されるのでダブルクォーテーションを削除しておく
        filepath = input().strip('"')
        if filepath[-len(extension) :] == extension and os.path.exists(filepath):
            break
        else:
            print_alerts(f"{filepath}は無効な形式です", f"拡張子{extension}のファイルパスを入力して下さい")

    return os.path.abspath(filepath)


def get_folder(message: str, extension: str = DATA_FILE_EXTENSION):
    print_notices(f"{message} 拡張子: {extension}")

    while True:
        # NOTE: パスのコピペが想定されるのでダブルクォーテーションを削除しておく
        folder_path = input().strip('"')
        if utils.get_filenames_from_folder(folder_path, extension):
            break
        else:
            print_alerts(f"{folder_path}に拡張子{extension}のファイルが存在しません。")

    return os.path.abspath(folder_path)
