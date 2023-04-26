import os
import re
from typing import Any

import colorama
from termcolor import cprint

from common import utils
from common.constants import CLI_COLORS, DATA_FILE_EXTENSION

colorama.init()


def print_default(*texts: str):
    [print(text) for text in texts]


def print_notices(*texts: str):
    [cprint(text, CLI_COLORS.notice) for text in texts]


def print_alerts(*texts: str):
    [cprint(text, CLI_COLORS.alert) for text in texts]


def print_section(*texts: str, separator = "* " * 20):
    cprint(separator, CLI_COLORS.section)
    [cprint(text, CLI_COLORS.section) for text in texts]
    cprint(separator, CLI_COLORS.section)


def __get_option(*options: Any) -> Any:
    while True:
        selected = input()
        if selected in options or selected == "":
            break
        else:
            print_alerts(f"{selected}は無効な値です", "有効な値を入力して下さい")
    return selected


def get_filepath(message: str, extension: str = ".xlsx") -> str:
    print_notices(f"{message} 拡張子: {extension}")

    while True:
        # NOTE: パスのコピペを想定してダブルクォーテーションを削除しておく
        filepath = input().strip('"')
        if filepath[-len(extension) :] == extension and os.path.exists(filepath):
            break
        else:
            print_alerts(f"{filepath}は無効な形式です", f"拡張子{extension}のファイルパスを入力して下さい")

    return os.path.abspath(filepath)


def get_folder(message: str, extension: str = DATA_FILE_EXTENSION):
    print_notices(f"{message} 拡張子: {extension}")

    while True:
        # NOTE: パスのコピペを想定してダブルクォーテーションを削除しておく
        folder_path = input().strip('"')
        if utils.get_filenames_from_folder(folder_path, extension):
            break
        else:
            print_alerts(f"{folder_path}に拡張子{extension}のファイルが存在しません。")

    return os.path.abspath(folder_path)


def get_date(message: str, format_regex: re.Pattern = re.compile(r"\d{6}")) -> str:
    # FIXME: format_regexを引数として受け取るのにメッセージがyymmdd形式固定になっている
    print_notices(message, "yymmdd形式で入力して下さい (例: 221025)")
    while True:
        date = input()
        if date == "":
            return date
        if format_regex.match(date):
            return f"20{date[:2]}年    {date[2:4]}月    {date[4:6]}日"
        print_alerts(f"{date}は無効な日付です", "yymmdd形式で入力して下さい (例: 221025)")


def get_selected_option(options: list[str], *messages: str) -> str:
    display_options = []
    user_select_options = []

    for i, option in enumerate(options, start=1):
        display_options.append(f"\t{i}.{option}")
        user_select_options.append(str(i))

    [print_notices(message) for message in messages]
    print_default(*display_options)
    try:
        return options[int(__get_option(*user_select_options)) - 1]
    # 何も入力されなかった場合
    except ValueError:
        return ""
