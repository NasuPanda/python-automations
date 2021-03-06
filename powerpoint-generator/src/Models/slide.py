import re
import math
from copy import deepcopy
from typing import Iterator, TypedDict, Optional

import src.config as config
from src.Models.sorter import LabeledImage
from src.Models.content import Image, TextBox


# Errors
class LabelNotFoundError(Exception):
    """ラベルが見つからないとき"""


class GroupIdNotNumberError(Exception):
    """GroupIDに数字以外が指定されたとき"""


class LabelNotNumberError(Exception):
    """ラベルに数字以外が指定されたとき"""


class NumberOfLabelMissMatchError(Exception):
    """コンテンツ数 ≠ グループ数×ラベル数のとき"""


class ContentsGroup(TypedDict, total=False):
    """SlideContentのグループ"""
    group_id: str
    image: list[Image]
    textbox: list[TextBox]


class Slide():
    """スライド。

    contents: list[ContentsGroup]
        ContentsGroupのリスト。
    """
    def __init__(self) -> None:
        self.contents: list[ContentsGroup] = []

    def set_contents(self, content_type: str, contents: list, group_id: str):
        """指定したidのグループにcontentsをセットする。

        Parameters
        ----------
        content_type : str
            セットするコンテンツのタイプ。(ContentsGroupのキー)
        contents : list
            セットするコンテンツのリスト。
        group_id : str
            グループのid。
        """
        self.__set_group(group_id)
        self.contents[-1][content_type] = contents

    def add_content(self, content_type: str, content: Image | TextBox, group_id: str):
        """指定したidのグループにcontentを追加する。(グループが存在しなければ作る)

        Parameters
        ----------
        content_type : str
            セットするコンテンツのタイプ。(ContentsGroupのキー)
        content : Image | TextBox
            セットするコンテンツ。
        group_id : str
            グループのid。
        """
        try:
            group = self.__search_group_by_id(group_id)
            group[content_type].append(content)
        except Exception:
            self.__set_group(group_id)
            self.contents[-1][content_type].append(content)

    def search_content_by_label(
            self,
            content_type: str,
            search_label: str,
            group_id: Optional[str] = None
        ) -> Image | TextBox:
        """ラベルを使ってコンテンツを探す。

        Parameters
        ----------
        content_type : str
            コンテンツのタイプ。
        search_label : str
            対象のラベル。
        group_id : Optional[str], optional
            グループのid。指定しなければ最後尾のグループを使う, by default None

        Returns
        -------
        Image | TextBox
            見つかったコンテンツ。

        Raises
        ------
        LabelNotFoundError
            存在しないラベルを指定した場合。
        """
        group = self.__search_group_by_id(group_id)

        for content in group[content_type]:
            if content["label"] == search_label:
                return content
        raise LabelNotFoundError(f"PowerPointテンプレートに存在しないラベルが指定されました: {search_label}")

    def get_number_of_contents(self, content_type: str) -> int:
        """コンテンツ数を返す。

        Parameters
        ----------
        content_type : str
            コンテンツのタイプ。

        Returns
        -------
        int
            コンテンツ数。
        """
        count = 0
        # 全グループのコンテンツ数を合計する
        [count := count + len(group[content_type]) for group in self.contents]
        return count

    def get_number_of_group(self) -> int:
        """グループ数を返す。

        Returns
        -------
        int
            グループ数。
        """
        return len(self.contents)

    def get_contents_from_first_group(self, content_type: str) -> list[Image | TextBox]:
        """最初のグループのコンテンツを返す。(1グループ前提のときに使用)

        Parameters
        ----------
        content_type : str
            コンテンツのタイプ。

        Returns
        -------
        list[Image | TextBox]
            コンテンツのリスト。
        """
        return self.contents[0][content_type]

    def __set_group(self, group_id: str):
        """新規グループをセットする。

        Parameters
        ----------
        group_id : str
            グループのid。
        """
        new_group = ContentsGroup(group_id=group_id, image=[], textbox=[])
        self.contents.append(new_group)

    def __search_group_by_id(self, group_id: Optional[str]) -> ContentsGroup:
        """idを使ってグループを探す。

        Parameters
        ----------
        group_id : Optional[str]
            グループのid。指定しなければ最後尾のグループを返す。

        Returns
        -------
        ContentsGroup
            見つかったグループ。

        Raises
        ------
        KeyError
            存在しないグループのidを指定した場合。
        """
        if group_id is None:
            return self.contents[0]
        else:
            for group in self.contents:
                if group["group_id"] == str(group_id):
                    return group

        raise KeyError(f"group id doesn't exist: {group_id}")


class TemplateSlide(Slide):
    """テンプレートスライド。

    contents: list[ContentsGroup]
        ContentsGroupのリスト。
    """
    def __init__(
            self,
            template_contents: list[Image],
            template_content_type: str = config.IMAGE_KEY
    ) -> None:
        """初期化。
        グループ数を画像のテンプレートから定義するため画像のリストを渡す。

        例: 1グループ/1スライドの場合
            labels = [1, 2, 3, 4]
            splits = [] => 空なので1グループ/1スライド

        例: 複数グループ/1スライドの場合
            labels = [1_1, 1_2, 1_3, 2_1, 2_2, 2_3]
            splits = [[1, 1], [1, 2]...] => 複数グループ/1スライド
            group_ids = [1, 2], labels = (1, 2, 3)
            group1: label[1, 2, 3], group2: label[1, 2, 3]

        Parameters
        ----------
        template_contents : list[Image]
            テンプレート用のコンテンツのリスト
        template_content_type : str, optional
            コンテンツのタイプ, by default config.IMAGE_KEY

        Raises
        ------
        GroupIdNotNumberError
            グループIDが数字で無い場合
        NumberOfLabelMissMatchError
            ラベル数が一致していない場合
        """
        super().__init__()
        labels: list[str] = [content["label"] for content in template_contents]

        # 複数グループ/1スライドの場合: group_label形式のみ対応。"1_A".split => [1, A] 以外になる場合弾く
        splits = [i.split(config.DELIMITER) for i in labels if len(i.split(config.DELIMITER)) == 2]
        if not splits:
            # labelが分割出来ない = 1グループ/1スライド
            self.set_contents(template_content_type, template_contents, group_id="1")
            return

        # 複数グループ/1スライドの場合
        # 重複を排除しつつ数値順に並び替える
        try:
            group_ids: list[str] = sorted(set([i[0] for i in splits]), key=lambda i: int(i))
        except ValueError:
            raise GroupIdNotNumberError("グループIDに数字以外の値が指定されました。")

        new_labels: set[str] = set([i[1] for i in splits])

        # labels = [1_A, 1_B, 2_A] のようにlabelの数が一致していない場合は弾く
        if len(template_contents) != len(group_ids) * len(new_labels):
            raise NumberOfLabelMissMatchError("ラベルの数が一致していません。")

        # group_ids = [1, 2], new_labels = (A, B)
        # group 1 : label A, B / group2: label A, B
        for group_id in group_ids:
            for label in new_labels:
                searching_label = group_id + config.DELIMITER + label
                for content in template_contents:
                    if searching_label == content["label"]:
                        content["label"] = label
                        self.add_content(template_content_type, content, group_id)
                        continue

    def sort_contents_by_numeric_label(self, content_type: str = config.IMAGE_KEY):
        """コンテンツをラベルの数値順にソートする

        Parameters
        ----------
        content_type : str
            コンテンツのタイプ, by default config.IMAGE_KEY

        Raises
        ------
        LabelNotNumberError
            数値以外のラベルが指定された場合
        """
        try:
            self.contents[0][content_type] = sorted(
                self.contents[0][content_type], key=lambda i: int(i["label"])
            )
        except ValueError:
            raise LabelNotNumberError("ラベルに数字以外の値が指定されました。")

    def set_textboxes(self, textboxes: list[TextBox]):
        """テキストボックスをセットする。

        Parameters
        ----------
        textboxes : list[TextBox]
            テキストボックスのリスト。
        """
        if (number_of_group := self.get_number_of_group()) == 1:
            [self.contents[0]["textbox"].append(textbox) for textbox in textboxes]
            return
        # グループ数が2以上の場合、分割しつつ追加する
        split_textboxes: list[list[TextBox]] = self.__split_list(textboxes, number_of_group)
        for textboxes, group, in zip(split_textboxes, self.contents):
            [group["textbox"].append(textbox) for textbox in textboxes]

    @staticmethod
    def __split_list(list: list, number_of_splits: int):
        """リストをN分割する

        Parameters
        ----------
        list : list
            分割したリスト
        number_of_splits : int
            N数

        Returns
        -------
        list
            分割後のリスト
        """
        # [10]のリストを3分割したい => 要素数は 3/ 10 = 3
        number_of_elements = math.ceil(len(list) / number_of_splits)
        result = [list[i: i + number_of_elements] for i in range(0, len(list), number_of_elements)]
        return result


class SlideGenerator():
    """書き込みに使う情報を持つスライドを生成する。

    template_slide: TemplateSlide
        テンプレートスライド。
    slides: list[Slide]
        書き込みに使う情報を持つSlideのリスト。
    """
    def __init__(
            self,
            template_contents: list[Image],
            template_content_type: str,
            total_number_of_contents: int
    ) -> None:
        """
        初期化。

        Parameters
        ----------
        template_contents : list[Image]
            テンプレートのコンテンツ。デフォルトは画像
        template_content_type : str
            テンプレートのコンテンツタイプ。
        total_number_of_contents : int
            コンテンツ数の合計。

        Raise
        ----------
        GroupIdNotNumberError
            template_slideの初期化: グループIDが数字で無い場合
        NumberOfLabelMissMatchError
            template_slideの初期化: ラベル数が一致していない場合
        """
        self.template_slide = TemplateSlide(template_contents, template_content_type)
        number_of_slide = math.ceil(total_number_of_contents / len(template_contents))
        self.slides = [Slide() for _ in range(number_of_slide)]

    def set_textboxes_to_template(self, textboxes: list):
        """テンプレートにテキストボックスをセットする。

        Parameters
        ----------
        textboxes : list
            テキストボックスのリスト。
        """
        self.template_slide.set_textboxes(textboxes)

    def set_sequence_images_to_slides(self, grouped_images: dict[str, list[LabeledImage]]):
        """スライドに対して順番に画像をセットする。複数グループを持つ画像を許容しない。

        Parameters
        ----------
        grouped_images : dict[str, list[LabeledImage]]
            グループ化された画像のリスト。

        Raises
        ------
        Exception
            グループが2つ以上存在する場合。
        """
        if (group_id := self.__get_single_group_id(grouped_images)) is None:
            raise Exception("Group exists two or more.")

        images = grouped_images[group_id]
        template_contents = self.template_slide.get_contents_from_first_group(config.IMAGE_KEY)
        image_index = 0

        for slide in self.slides:
            tmp_contents = []

            for content in template_contents:
                image = images[image_index]
                tmp_contents.append(
                    Image(
                        coordinates=content["coordinates"],
                        size=content["size"],
                        label=image["label"],
                        path=image["path"]
                    )
                )
                image_index += 1
                # スライド数×1スライドのコンテンツ数 != コンテンツ数の合計の時、処理を中断するための分岐
                if image_index == len(images):
                    break

            slide.set_contents(config.IMAGE_KEY, tmp_contents, group_id)

    def set_laidout_images_to_slides(self, grouped_images: dict[str, list[LabeledImage]]):
        """スライドに対してレイアウトされた画像をセットする。

        Parameters
        ----------
        grouped_images : dict[str, list[LabeledImage]]
            グループ化された画像のリスト。

        Raises
        ----------
        LabelNotFoundError
            search_content_by_label: 存在しないラベルを指定した場合。
        """
        labled_image_generator = self.__generate_dict_items_generator(grouped_images)

        for slide in self.slides:
            for group in self.template_slide.contents:
                try:
                    new_group_id, images = next(labled_image_generator)
                except StopIteration:
                    break

                temp_contents = []

                for image in images:
                    content = self.template_slide.search_content_by_label(
                        config.IMAGE_KEY,
                        image["label"],
                        group["group_id"]
                    )
                    temp_contents.append(
                        Image(
                            coordinates=content["coordinates"],
                            size=content["size"],
                            label=content["label"],
                            path=image["path"]
                        ),
                    )

                slide.set_contents(config.IMAGE_KEY, temp_contents, new_group_id)

    def set_textboxes_to_slides(self):
        """スライドに対してテキストボックスをセットする。

        Raises
        ------
        IndexError
            ラベル数がオーバーした場合。
        """
        for slide in self.slides:
            template_contents = deepcopy(self.template_slide.contents)
            current_label = 0
            matched_pairs: dict[str, str] = {}
            # グループ数が奇数の場合に備えてzip_longestを使う
            for template_group, group in zip(template_contents, slide.contents):
                if not group:
                    return
                for textbox in template_group["textbox"]:
                    text = textbox["text"]
                    # group_idを指す文字列が存在すれば置換する
                    text = re.sub(config.REGEX_POINTING_GROUP, group["group_id"], text)
                    # labelを指す文字列が存在すれば置換する
                    if re.search(config.REGEX_POINTING_LABEL, text):
                        # 既にマッチしたlabelを指す文字列が存在する場合それを利用する
                        if text in matched_pairs.keys():
                            text = matched_pairs[text]
                        # matched_pairsに存在しなければペアに追加して置換
                        else:
                            try:
                                replacement_label = group["image"][current_label]["label"]
                            except IndexError:
                                break
                            matched_pairs[text] = replacement_label
                            text = re.sub(config.REGEX_POINTING_LABEL, replacement_label, text)
                            current_label += 1
                    textbox["text"] = text
                group["textbox"] = template_group["textbox"]

    def sort_template_images_by_numeric_label(self):
        """テンプレートの画像をラベル順(数値順)にソートする。
        順序データの時にのみ使用し、数値以外のラベルを許容しない。

        Raises
        ----------
        LabelNotNumberError
            template_slide.sort_contents_by_numeric_label: 数値以外のラベルが指定された場合
        """
        self.template_slide.sort_contents_by_numeric_label(config.IMAGE_KEY)

    @staticmethod
    def __generate_dict_items_generator(dict: dict) -> Iterator[tuple[str, list[Image]]]:
        """key, valueを返すジェネレーターを生成する。

        Parameters
        ----------
        dict : dict
            辞書。

        Yields
        ------
        Iterator[tuple[str, list[Image]]]
            key, valueの返す。
        """
        for k, v in dict.items():
            yield k, v

    @staticmethod
    def __get_single_group_id(grouped_contents: dict[str, list[LabeledImage]]) -> str:
        """グループidを取得。(複数グループの場合は弾く)

        Parameters
        ----------
        grouped_contents : dict[str, list[LabeledImage]]
            グループ化されたコンテンツのリスト。

        Returns
        -------
        str
            グループのid。
        """
        # 複数group存在する場合弾く
        if len(group_ids := [key for key in grouped_contents.keys()]) != 1:
            return
        return group_ids[0]
