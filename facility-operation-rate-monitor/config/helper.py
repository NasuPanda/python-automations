import re
import pathlib

from libs import timehelper
from libs.exceptions import NumberNotFoundError


# regex of matching underscore and number
REGEX_UNDERSCORE_AND_NUMBER = re.compile("_[0-9]+")
# regex of matching number
REGEX_NUMBER = re.compile("[0-9]+")


def __find_paths_has_duplicate_filename(filepath: str, folder_path: str) -> list[pathlib.Path] | list:
    """Find paths has duplicate filename.

    Parameters
    ----------
    file_path : str
        File path.
    folder_path : str
        Folder path.

    Returns
    -------
    list[pathlib.Path] | list[]
        Found paths.
    """
    file = pathlib.Path(filepath)
    file_name = file.stem
    # NOTE: Path.suffix return extension, it includes `.`
    extension = file.suffix

    files_in_folder_with_extension = pathlib.Path(folder_path).glob("*" + extension)
    # If file name exist duplicate, assign file to list
    return [f for f in files_in_folder_with_extension if file_name in f.stem]


def __find_sequential_number(string: str) -> int | None:
    """Find sequential number from string.
    NOTE
    Sequential number example: `example_filename_1.csv` => `_1`.
    Must includes underscore.

    Parameters
    ----------
    string : str
        Target string.

    Returns
    -------
    int | None
        Found number. If string doesn't include sequential number, returns None.
    """
    matched_underscore_and_number = REGEX_UNDERSCORE_AND_NUMBER.search(string)
    if matched_underscore_and_number is None:
        return
    # Search method returns match object, so str() is required
    return int(str(
        REGEX_NUMBER.search(str(matched_underscore_and_number))
    ))


def __find_the_string_has_the_largest_sequential_number(strings: list[str]) -> str:
    """Find the one has the largest sequential number from strings.

    Parameters
    ----------
    strings : list[str]
        Target strings.

    Returns
    -------
    str
        The found string has the largest sequential number.

    Raises
    ------
    NumberNotFoundError
        When strings doesn't have valid string.
    """
    numbers = []
    for name in strings:
        numbers.append(__find_sequential_number(name))
    if not any(numbers):
        raise NumberNotFoundError(f"Sequential number is not found from {strings}\nMust includes underscore.")
    # Get index of largest number and return value
    return strings[strings.index(max(numbers))]


def __assign_sequential_number(string: str) -> str:
    """Assign sequential number and return.

    - If sequential number doesn't exist, assign 1
    - If sequential number exists, assign incremented number

    Parameters
    ----------
    string : str
        Target string.

    Returns
    -------
    str
        String after assigning sequential number.
    """
    number = __find_sequential_number(string)
    if number:
        incremented_sequential_number = number + 1
        new_underscore_and_number = "_" + str(incremented_sequential_number)
        return REGEX_UNDERSCORE_AND_NUMBER.sub(new_underscore_and_number, string)

    # If string doesn't have part of underscore and number, assign underscore and sequential number.
    return f"{string}_1"


def resolve_filename_conflict(filepath: str, dst_folder: str) -> str:
    """Resolve filename conflicts in a folder by assigning an underscore and sequential number.

    Parameters
    ----------
    filename : str
        String to the filename.
    dst_folder : str
        Folder containing the file.

    Returns
    -------
    str
        Conflict resolved filepath.
        - If duplication doesn't exist, return it is as.
        - If duplication exists, return after assigning sequential number.
    """
    paths_has_duplicate_filename = __find_paths_has_duplicate_filename(filepath, dst_folder)
    # If doesn't exist duplication, return file_path is as
    if not paths_has_duplicate_filename:
        return filepath

    # Path object must be cast to str
    file_names_has_duplicate_filename = [path.stem for path in paths_has_duplicate_filename]
    # If there is one file has duplicate name, assign 1
    if len(file_names_has_duplicate_filename) == 1:
        return __assign_sequential_number(file_names_has_duplicate_filename[0])
    # If there are multiple files has duplicate name, find largest number and assign incremented number
    else:
        file_has_the_largest_sequential_num = __find_the_string_has_the_largest_sequential_number(file_names_has_duplicate_filename)
        return __assign_sequential_number(file_has_the_largest_sequential_num)
