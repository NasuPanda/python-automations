from pathlib import Path
from typing import Optional, TypedDict
import re

import config

class LabeledImage(TypedDict):
    label: str
    path: str


class ImageSequencer():
    def __init__(self, images: list[Path]) -> None:
        self.images: list[Path] = images
        # {group_id: [LabeldImage...]...}
        self.labeld_images: dict[str, list[LabeledImage]] = {}

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
            raise IndexError(f"Partial splits fail. string: {string}, index: {label_part_index}")
        without_label = [i for i in splits if not i == label]
        without_label = config.DELIMITER.join(without_label)

        return label, without_label

    def sort_based_on_numeric_part(self, numeric_part_index=-1):
        try:
            # Pathオブジェクトをstem(ファイル名のみ)に変換
            # 指定されたインデックスを基準にsplit
            # 数値順にソート
            self.images = sorted(self.images, key=lambda s: int(self.__get_partial(s.stem, numeric_part_index)))
        # 数値以外が基準に指定された場合弾く
        # TODO GUI コール
        except ValueError:
            raise ValueError("Non-numeric value is specified")

    def sort_default(self):
        self.images = sorted(self.images)

    def sort_based_on_createtime(self):
        self.images = sorted(self.images, key=lambda i: i.stat().st_ctime)

    def labeling_images(self, label_part_index=-1):
        for image in self.images:
            label, group_id = self.__split_into_label_and_others(image.stem, label_part_index)
            if group_id not in self.labeld_images.keys():
                self.labeld_images[group_id] = []
            self.labeld_images[group_id].append(LabeledImage(label=label, path=str(image)))