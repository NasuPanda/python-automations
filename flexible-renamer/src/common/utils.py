import os
import pathlib


def is_dir(path: str) -> bool:
    return os.path.isdir(path)


def get_path_stem(path: str) -> str:
    return pathlib.Path(path).stem
