"""Utility モジュール"""
import pathlib


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


def get_file_ctimes_from_folder(folder_path: str, extension: str):
    """ファイルの作成日時を取得"""
    files = pathlib.Path(folder_path).glob(f"**/*{extension}")
    return sorted([f.stat().st_ctime for f in files])


def longest_ljust(strings: list[str]):
    """渡された配列の中で最も長い文字列を基準にして左揃えする"""
    longest_len = max([len(s) for s in strings])
    return [s.ljust(longest_len) for s in strings]
