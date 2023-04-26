import datetime
import pathlib

from common.constants import DIFF_JST_FROM_UTC, GRAPH_SCALES


def decide_graph_scale_interval(max: float, min: float = 0):
    """Decide graph scale interval.
    # NOTE: Algorithm reference: https://www.eng.niigata-u.ac.jp/~nomoto/21.html
    """
    w = max - min
    d = w / 2.0
    for i, j in zip(GRAPH_SCALES, GRAPH_SCALES[1:]):
        if i <= d <= j:
            return i
    raise ValueError(f"Can't decide scale. Your inputs are max:{max} and min:{min}")


def get_timestamp(format: str):
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
    return now.strftime(format)


def get_files_from_folder(folder_path: str, extension: str):
    """フォルダーからファイルパスを取得"""
    return sorted([str(p) for p in pathlib.Path(folder_path).glob(f"**/*{extension}")])


def get_filenames_from_folder(folder_path: str, extension: str):
    """フォルダーからファイル名を取得"""
    return sorted([p.name for p in pathlib.Path(folder_path).glob(f"**/*{extension}")])


def get_file_stems_from_folder(folder_path: str, extension: str):
    """拡張子を除いてファイル名を取得"""
    files = pathlib.Path(folder_path).glob(f"**/*{extension}")
    return sorted([f.stem for f in files])
