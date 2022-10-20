import os
import shutil
from pathlib import Path

from src.common import exceptions
from src.config.config import config


class FileFilter:
    def __init__(
        self,
        src_files: list[str] | None = None,
        src_folder: str | None = None,
    ) -> None:
        if src_files:
            self.paths = [file for file in src_files]
        elif src_folder:
            self.paths = [str(p) for p in Path(src_folder).glob("**/*")]
        else:
            raise ValueError("引数が無効です")

    @classmethod
    def has_target_extension(cls, path: str, target_extension: str) -> bool:
        return path[-len(target_extension) :] == target_extension

    def filter_by_extension(
        self,
        target_extension: str = config.target_extension,
    ) -> None:
        if target_extension[0] != ".":
            raise exceptions.ExtensionError(f"拡張子には `.` を含めて下さい : {target_extension}")

        paths_only_target_extension = [
            file for file in self.paths if self.has_target_extension(file, target_extension)
        ]

        if not paths_only_target_extension:
            raise FileNotFoundError(f"拡張子{target_extension}のファイルが存在しません")

        self.paths = paths_only_target_extension

    def exclude_by_exclude(self, excluded_name: str) -> None:
        paths = [file for file in self.paths if not excluded_name in file]

        if not paths:
            raise FileNotFoundError(f"全てのファイルが{excluded_name}を含んでいます")

        self.paths = paths

    def filter_by_include(self, included_name: str) -> None:
        paths = [file for file in self.paths if included_name in file]

        if not paths:
            raise FileNotFoundError(f"どのファイルも{included_name}を含んでいません")

        self.paths = paths


class FileRenamer:
    delimiter = config.delimiter

    def __init__(
        self,
        src_files: list[str] | None = None,
        src_folder: str | None = None,
    ) -> None:
        if src_files:
            self.src_paths = src_files
        elif src_folder:
            self.src_paths = [str(p) for p in Path(src_folder).glob("**/*")]
        else:
            raise ValueError("引数が無効です")

        self.dst_names: list[str] = [Path(i).stem for i in self.src_paths]
        print(self.dst_names)

    @classmethod
    def split(cls, original: str) -> list[str]:
        return original.split(cls.delimiter)

    @classmethod
    def swap(cls, original: str, before: int, after: int) -> str:
        parts = cls.split(original)
        parts[before], parts[after] = parts[after], parts[before]
        return cls.delimiter.join(parts)

    @classmethod
    def replace(cls, original: str, new_part: str, replaced_index: int) -> str:
        parts = cls.split(original)
        parts[replaced_index] = new_part
        return cls.delimiter.join(parts)

    @property
    def number_of_dst_files(self) -> int:
        return len(self.dst_names)

    def replace_parts(
        self,
        new_parts: list[str],
        replaced_index: int,
    ) -> None:
        if self.number_of_dst_files != len(new_parts):
            raise exceptions.LengthDoesNotMatchError("dst_names と new_parts の長さが一致していません")

        try:
            self.dst_names = [
                self.replace(filename, new_part, replaced_index)
                for filename, new_part in zip(self.dst_names, new_parts)
            ]
        except IndexError:
            exceptions.ReplaceError("ファイルの部分置換に失敗しました")

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
            exceptions.ReplaceError("ファイルの部分スワップに失敗しました")

    def copy_from_src_to_dst(self, dst_folder: str) -> None:
        extension = Path(self.src_paths[0]).suffix

        for src_path, dst_name in zip(self.src_paths, self.dst_names):
            dst_path = os.path.join(dst_folder, dst_name + extension)
            shutil.copy(src_path, dst_path)

    def get_sample(self) -> str:
        return self.dst_names[0]
