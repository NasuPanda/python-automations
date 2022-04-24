import re
from copy import deepcopy
from pathlib import Path
from typing import TypedDict

import src.config as config
from src.Models.content import TextBox


class LabeledImage(TypedDict):
    """ラベリングされた画像。
    """
    label: str
    path: str


class ImageSorter():
    """画像を順序付ける。

    image_paths: list[Path]
        画像のパス。(Pathオブジェクトのリスト。)
    """
    def __init__(self, images: list[Path]) -> None:
        """初期化。

        Parameters
        ----------
        images : list[Path]
            Pathオブジェクトのリスト。
        """
        self.image_paths: list[Path] = images

    def get_image_paths_as_str(self) -> list[str]:
        """文字列としてパスのリストを取得。

        Returns
        -------
        list[str]
            文字列のリスト
        """
        return [str(i) for i in self.image_paths]

    def sort_based_on_numeric_part(self, numeric_part_index=-1):
        """数値部分を基準にソート。
        stemに変換 → 指定されたインデックスを基準にsplit → 数値順にソート

        Parameters
        ----------
        numeric_part_index : int, optional
            数値部分のインデックス, by default -1

        Raises
        ------
        ValueError
            数値以外が指定された場合。
        """
        try:
            self.image_paths = sorted(self.image_paths, key=lambda s: int(self.__get_partial(s.stem, numeric_part_index)))
        # 数値以外が基準に指定された場合弾く
        # TODO GUI コール
        except ValueError:
            raise ValueError("Non-numeric value is specified")

    def sort_default(self):
        """デフォルト順にソートする。
        """
        self.image_paths = sorted(self.image_paths, key=lambda i: i.stem)

    def sort_based_on_createtime(self):
        """作成日時順にソートする。
        """
        self.image_paths = sorted(self.image_paths, key=lambda i: i.stat().st_ctime)

    def labeling_images(self, label_part_index=-1) -> dict[str, list[LabeledImage]]:
        """画像をラベリングする。

        Parameters
        ----------
        label_part_index : int, optional
            ラベル部分のインデックス, by default -1

        Returns
        -------
        dict[str, list[LabeledImage]]
            グループ化されたラベリング済画像のリスト。
        """
        labeld_images: dict[str, list[LabeledImage]] = {}

        for image in self.image_paths:
            label, group_id = self.__split_into_label_and_others(image.stem, label_part_index)
            if group_id not in labeld_images.keys():
                labeld_images[group_id] = []
            labeld_images[group_id].append(LabeledImage(label=label, path=str(image)))

        return labeld_images

    def __get_partial(self, string: str, part_index=-1) -> list[str]:
        """部分を取得する。
        ex. string: [foo_bar_1], part_index: 2 => 1

        Parameters
        ----------
        string : str
            対象の文字。_
        part_index : int, optional
            取得したい部分のインデックス, by default -1

        Returns
        -------
        list[str]
            分割後のリスト。

        Raises
        ------
        IndexError
            分割に失敗。
        """
        try:
            return string.split(config.DELIMITER)[part_index]
        except IndexError:
            raise IndexError(f"Partial splits fail. string: {string}, index: {part_index}")

    def __split_into_label_and_others(self, string: str, label_part_index=-1) -> tuple[str, str]:
        """ラベルとそれ以外に分割する。

        Parameters
        ----------
        string : str
            文字列。
        label_part_index : int, optional
            ラベル部分のインデックス, by default -1

        Returns
        -------
        tuple[str, str]
            label, without_label

        Raises
        ------
        IndexError
            ラベル部分のインデックス指定が間違っている時。
        """
        splits = string.split(config.DELIMITER)
        try:
            label = splits[label_part_index]
        except IndexError:
            raise IndexError(f"Label/others splits fail. string: {string}, index: {label_part_index}")
        without_label = [i for i in splits if i != label]
        without_label = config.DELIMITER.join(without_label)

        return label, without_label


class TextBoxSorter():
    """テキストボックスを順序付ける。

    textboxes: list[TextBox]
        テキストボックスのリスト。
    sorted_textboxes: list[TextBox]
        ソート後のテキストボックス。(ラベルごとに分割される)
    """
    def __init__(self, textboxes: list[TextBox]) -> None:
        """初期化。

        Parameters
        ----------
        textboxes : list[TextBox]
            テキストボックスのリスト。
        """
        self.textboxes: list[TextBox] = textboxes
        self.sorted_textboxes: list[list[TextBox]] = []

    def sort_based_on_label(self, *patterns: str):
        """TextBox["label"]を元にソートする。指定したパターンごとに別々のリストに入れる。

        Parameters
        ----------
        patterns : *args[str]
            対象のパターン。
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
        self.sorted_textboxes.append(copied_textboxes)

    @staticmethod
    def __search_number(textbox: TextBox, ret=float("inf")):
        """数値を探す。(ソート用)

        Parameters
        ----------
        textbox : TextBox
            テキストボックス。
        ret : float, optional
            無限。(数値が存在しない場合強制的に最後尾へ), by default float("inf")

        Returns
        -------
        _type_
            _description_
        """
        match = re.search('\d', textbox["label"])
        try:
            return int(match.group())
        # 存在しなければ無限大(強制的に最後尾へ)
        except Exception:
            return ret