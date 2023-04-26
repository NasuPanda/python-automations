import os
import pathlib

# フォルダー作成(存在していてもOK)
os.makedirs("./folder", exist_ok=True)

# パスの結合
os.path.join("./parent", "child.txt")
# or
p = pathlib.Path("folder")
p_sub_dir_file = p / "sub_dir" / "file.txt"
# or
p = pathlib.Path("folder")
p.joinpath('sub_dir', 'file.txt')

# ファイルかどうか判定
os.path.isfile("file.txt")
# or
p = pathlib.Path("file.txt")
p.exists()

# ファイルを開く(処理が終わったファイルをユーザに見せたいときなど)
os.startfile("output_path")

#
# フォルダーからファイルを取得する系の処理
#
def get_files_from_folder(folder_path: str, extension: str):
    """フォルダーからファイルパスを取得
    NOTE: 複数拡張子で指定する方法: https://ekapyw.byte.jp/python/pathlib-glob-multiple-extension/
    """
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

