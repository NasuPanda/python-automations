import itertools
import os
import pathlib
import re

from src.common.constants import WORD_LENGTH_REMOVE_DUPLICATE


def get_filename_from_path(filepath: str) -> str:
    return pathlib.Path(filepath).name


def is_dir(filepath: str) -> bool:
    return os.path.isdir(filepath)


def find_longest_duplicate_word(string1: str, string2: str) -> str:
    answer = ""
    length_1, length_2 = len(string1), len(string2)

    for i in range(length_1):
        match = ""
        for j in range(length_2):
            if i + j < length_1 and string1[i + j] == string2[j]:
                match += string2[j]
            else:
                if len(match) > len(answer):
                    answer = match
                match = ""
        if len(match) > len(answer):
            answer = match  # this was missing
    return answer


def escape_regex(string: str) -> str:
    return string.translate(str.maketrans({"(": "\(", ")": "\)"}))


def create_regex_or_pattern(*strings: str) -> str:
    """`foo|bar` というパターンの正規表現を作る。
    NOTE: 長さ1の配列が与えられた場合は `foo` (そのまま) を返す
    """
    result = rf"{strings[0]}"

    if len(strings) == 1:
        return escape_regex(result)

    for s in strings[1:]:
        result += f"|{s}"
    # ()をエスケープする
    return escape_regex(result)


def remove_duplicates(*strings: str) -> list[str]:
    # [find and remove common substring with python - Stack Overflow](https://stackoverflow.com/questions/27963222/find-and-remove-common-substring-with-python)
    # [Remove specific characters from a string in Python - Stack Overflow](https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python)
    longest_duplicate_words = []

    # 与えられた配列の要素の組み合わせ全てに対して重複する文字列を探す処理を実行
    for pair in itertools.combinations(strings, 2):
        longest_duplicate_word = find_longest_duplicate_word(*pair)
        # 長さが一定以下の場合は重複削除しない
        if len(longest_duplicate_word) > WORD_LENGTH_REMOVE_DUPLICATE:
            longest_duplicate_words.append(longest_duplicate_word)

    # 配列の重複を排除
    longest_duplicate_words = list(set(longest_duplicate_words))
    if not longest_duplicate_words:
        return list(strings)

    regex = create_regex_or_pattern(*longest_duplicate_words)
    return [re.sub(regex, "", s) for s in strings]


def validate_input_min_max_range(min: str, max: str) -> bool:
    try:
        min_number = float(min)
        max_number = float(max)
    except ValueError:
        return False

    if min_number >= max_number:
        return False
    return True
