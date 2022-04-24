from copy import deepcopy
from pathlib import Path
import re
from typing import Text, TypedDict
from Models.content import TextBox

import config

class LabeledImage(TypedDict):
    label: str
    path: str


class ImageSorter():
    """順序付ける。"""
    def __init__(self, contents: list[Path]) -> None:
        self.image_paths: list[Path] = contents

    def get_image_paths_as_str(self):
        return [str(i) for i in self.image_paths]

    def sort_based_on_numeric_part(self, numeric_part_index=-1):
        try:
            # stemに変換 → 指定されたインデックスを基準にsplit → 数値順にソート
            self.image_paths = sorted(self.image_paths, key=lambda s: int(self.__get_partial(s.stem, numeric_part_index)))
        # 数値以外が基準に指定された場合弾く
        # TODO GUI コール
        except ValueError:
            raise ValueError("Non-numeric value is specified")

    def sort_default(self):
        self.image_paths = sorted(self.image_paths, key=lambda i: i.stem)

    def sort_based_on_createtime(self):
        self.image_paths = sorted(self.image_paths, key=lambda i: i.stat().st_ctime)

    def labeling_images(self, label_part_index=-1):
        # {group_id: [LabeldImage...]...}
        labeld_images: dict[str, list[LabeledImage]] = {}

        for image in self.image_paths:
            label, group_id = self.__split_into_label_and_others(image.stem, label_part_index)
            if group_id not in labeld_images.keys():
                labeld_images[group_id] = []
            labeld_images[group_id].append(LabeledImage(label=label, path=str(image)))

        return labeld_images

    def __get_partial(self, string: str, part_index=-1):
        try:
            # string: [foo_bar_1], part_index: 2 => 1
            return string.split(config.DELIMITER)[part_index]
        except IndexError:
            raise IndexError(f"Partial splits fail. string: {string}, index: {part_index}")

    def __split_into_label_and_others(self, string: str, label_part_index=-1):
        splits = string.split(config.DELIMITER)
        try:
            label = splits[label_part_index]
        except IndexError:
            raise IndexError(f"Label/others splits fail. string: {string}, index: {label_part_index}")
        without_label = [i for i in splits if i != label]
        without_label = config.DELIMITER.join(without_label)

        return label, without_label


class TextBoxSorter():
    def __init__(self, textboxes: list[TextBox]) -> None:
        self.textboxes: list[TextBox] = textboxes
        self.sorted_textboxes: list[list[TextBox]] = []

    def sort_based_on_label(self, *patterns: str):
        """
        TextBox["label"]を元にソートする。
        *patternsに指定したパターンごとに別々のリストに入れる。
        """
        copied_textboxes: list[TextBox] = deepcopy(self.textboxes)

        for i, pattern in enumerate(patterns):
            self.sorted_textboxes.append([])
            match: list[TextBox] = []

            for textbox in copied_textboxes:
                if re.search(pattern, textbox["label"]):
                    match.append(textbox)
            try:
                match.sort(key=self.__search_number)
                [self.sorted_textboxes[i].append(t) for t in match]
                [copied_textboxes.remove(t) for t in match]
            except TypeError:
                pass

        # 残りをappend
        [self.sorted_textboxes.append(c) for c in copied_textboxes]

    @staticmethod
    def __search_number(textbox: TextBox, ret=float("inf")):
        match = re.search('\d', textbox["label"])
        try:
            return int(match.group())
        # 存在しなければ無限大(強制的に最後尾へ)
        except Exception:
            return ret