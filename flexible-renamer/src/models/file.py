import glob
import os
import shutil
from pathlib import Path

from src.common import exceptions


class FileFilter:
    def __init__(
        self,
        src_files: list[str] | None = None,
        src_folder: str | None = None,
    ) -> None:
        if src_files:
            self.filepaths = [file for file in src_files]
        elif src_folder:
            self.filepaths = glob.glob(f"{src_folder}/*.*")
        else:
            raise ValueError("引数が無効です")

        self.filepaths.sort()

    @classmethod
    def has_target_extension(cls, path: str, target_extension: str) -> bool:
        return path[-len(target_extension) :] == target_extension

    def filter_by_extension(
        self,
        target_extension: str,
    ) -> None:
        if target_extension[0] != ".":
            raise exceptions.ExtensionError(f"拡張子には `.` を含めて下さい : {target_extension}")

        paths_only_target_extension = [
            file for file in self.filepaths if self.has_target_extension(file, target_extension)
        ]
        if not paths_only_target_extension:
            raise FileNotFoundError(f"拡張子{target_extension}のファイルが存在しません")

        self.filepaths = paths_only_target_extension

    def exclude_by_name_exclude(self, excluded_name: str) -> None:
        paths = [file for file in self.filepaths if not excluded_name in file]

        if not paths:
            raise FileNotFoundError(f"全てのファイルが{excluded_name}を含んでいます")

        self.filepaths = paths

    def filter_by_name_include(self, included_name: str) -> None:
        paths = [file for file in self.filepaths if included_name in file]

        if not paths:
            raise FileNotFoundError(f"どのファイルも{included_name}を含んでいません")

        self.filepaths = paths


class FileRenamer:
    def __init__(
        self, src_files: list[str] | None = None, src_folder: str | None = None, delimiter: str = "_"
    ) -> None:
        if src_files:
            self.src_paths = src_files
        elif src_folder:
            self.src_paths = glob.glob(f"{src_folder}/*.*")
        else:
            raise ValueError("引数が無効です")

        self.src_paths.sort()

        self.delimiter = delimiter
        # renameするのはfileのstem(拡張子を除いたファイル名)
        self.dst_names: list[str] = [Path(i).stem for i in self.src_paths]

    def split(self, original: str) -> list[str]:
        return original.split(self.delimiter)

    def swap(self, original: str, before: int, after: int) -> str:
        parts = self.split(original)
        parts[before], parts[after] = parts[after], parts[before]
        return self.delimiter.join(parts)

    def replace(self, original: str, new_part: str, replaced_index: int) -> str:
        parts = self.split(original)
        parts[replaced_index] = new_part
        return self.delimiter.join(parts)

    @property
    def number_of_dst_files(self) -> int:
        return len(self.dst_names)

    def replace_parts(
        self,
        new_parts: list[str],
        replaced_index: int,
    ) -> None:
        if self.number_of_dst_files != len(new_parts):
            raise exceptions.LengthDoesNotMatchError("設定されたデータ名の数 と 入力ファイル数が一致していません")

        try:
            self.dst_names = [
                self.replace(filename, new_part, replaced_index)
                for filename, new_part in zip(self.dst_names, new_parts)
            ]
        except IndexError:
            exceptions.ReplaceError(f"ファイルの部分置換に失敗しました。ファイル名に`{self.delimiter}`は含まれていますか?")

    def swap_parts(
        self,
        before_index: int,
        after_index: int,
    ) -> None:
        if not self.dst_names:
            raise ValueError("replace_parts が実行されていません")

        try:
            self.dst_names = [self.swap(i, before_index, after_index) for i in self.dst_names]
        except IndexError:
            exceptions.ReplaceError(f"ファイルの部分スワップに失敗しました。ファイル名に`{self.delimiter}`は含まれていますか?")

    def copy_from_src_to_dst(self, dst_folder: str) -> None:
        os.makedirs(dst_folder, exist_ok=True)
        extension = Path(self.src_paths[0]).suffix

        for src_path, dst_name in zip(self.src_paths, self.dst_names):
            dst_path = os.path.join(dst_folder, dst_name + extension)
            try:
                shutil.copy(src_path, dst_path)
            except OSError:
                raise OSError(f"ファイル名に使えない名前が指定されました: {dst_name}")

    def _format_preview(self, src: str, dst: str) -> str:
        return f"変更前: {Path(src).stem} ===> 変更後: {dst}"

    def format_previews(self) -> list[str]:
        return [self._format_preview(src, dst) for (src, dst) in zip(self.src_paths, self.dst_names)]
