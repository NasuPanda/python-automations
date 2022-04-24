from copy import deepcopy
import itertools
import math
from msilib import text
import re
from typing import Iterator, TypedDict, Optional

from Models.sorter import LabeledImage

import config
from Models.content import Image, TextBox


class ContentsGroup(TypedDict, total=False):
    """SlideContentの集合"""
    group_id: str
    image: list[Image]
    textbox: list[TextBox]


class Slide():
    """スライドクラス"""
    def __init__(self) -> None:
        self.contents: list[ContentsGroup] = []

    def set_contents(self, content_type: str, contents: list, group_id: str):
        """指定したgroup_id, content_typeにcontentsをセット"""
        new_contents: ContentsGroup = {"group_id": group_id, content_type: contents}
        self.contents.append(new_contents)

    def set_content(self, content_type: str, content: Image | TextBox, group_id: str):
        for _contents in self.contents:
            if _contents["group_id"] == group_id:
                _contents[content_type].append(content)
                return

        new_contents: ContentsGroup = {"group_id": group_id, content_type: [content]}
        self.contents.append(new_contents)

    def __search_contents_by_group_id(self, group_id: Optional[str]) -> ContentsGroup:
        if group_id is None:
            return self.contents[0]
        else:
            for contents in self.contents:
                if contents["group_id"] == str(group_id):
                    return contents

        raise KeyError(f"group id doesn't exist: {group_id}")

    def search_content_by_label(self, content_type: str, search_label: str, group_id: Optional[str] = None):
        """labelを元にcontnetを検索する"""
        searched_contents = self.__search_contents_by_group_id(group_id)

        for content in searched_contents[content_type]:
            if content["label"] == search_label:
                return content
        # TODO エラーキャッチしてGUIコール
        raise KeyError(f"Key doesn't exits: {search_label}")

    def get_content_labels(self, content_type: str, group_id: Optional[str] = None) -> list[str]:
        searched_contents = self.__search_contents_by_group_id(group_id)
        return [content["label"] for content in searched_contents[content_type]]

    def get_content_coordinates_and_sizes(self, content_type: str, group_id: Optional[str] = None):
        searched_contents = self.__search_contents_by_group_id(group_id)
        return [(*content["coordinates"], *content["size"]) for content in searched_contents[content_type]]

    def get_number_of_contents(self, content_type: str):
        count = 0
        [count := count + len(i[content_type]) for i in self.contents]
        return count

    def get_number_of_group(self):
        return len(self.contents)

    def get_first_group_of_contents(self, content_type: str):
        return self.contents[0][content_type]


class TemplateSlide(Slide):
    def __init__(
            self,
            template_contents: list[Image],
            template_content_type: str = config.IMAGE_KEY
    ) -> None:
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
            # TODO GUI
            raise ValueError("group id isn't number.")
        new_labels: set[str] = set([i[1] for i in splits])
        # labels = [1_A, 1_B, 2_A] のようにlabelの数が一致していない場合は弾く
        if len(template_contents) != len(group_ids) * len(new_labels):
            # TODO GUI
            raise Exception("number of contents / number of group_id's * number of label's are not equal")

        # group_ids = (1, 2)
        # new_labels = (A, B)
        # group 1 : label A, B / group2: label A, B
        for group_id in group_ids:
            for label in new_labels:
                searching_label = group_id + config.DELIMITER + label
                for content in template_contents:
                    if searching_label == content["label"]:
                        content["label"] = label
                        self.set_content(template_content_type, content, group_id)
                        continue

    def sort_contents_by_numeric_label(self, content_type: str = config.IMAGE_KEY):
        try:
            self.contents[0][content_type] = sorted(
                self.contents[0][content_type], key=lambda i: int(i["label"])
            )
        # TODO GUI コール
        except ValueError:
            raise ValueError("Non-numeric value is specified")

    def set_textboxes(self, textboxes: list):
        if (number_of_group := self.get_number_of_group()) == 1:
            self.contents[0]["textbox"] = textboxes
            return
        # グループ数が2以上の場合、分割しつつ追加する
        split_textboxes: list[list[TextBox]] = self.__split_list(textboxes, number_of_group)
        for textboxes, contents, in zip(split_textboxes, self.contents):
            contents["textbox"] = textboxes

    @staticmethod
    def __split_list(list, number_of_splits):
        # [10]のリストを3分割したい => 要素数は 3/ 10 = 3
        number_of_elements = math.ceil(len(list) / number_of_splits)
        result = [list[i: i + number_of_elements] for i in range(0, len(list), number_of_elements)]
        return result


class SlideGenerator():
    """
    スライドを生成する。
    画像を元にグループ分けする都合上画像を先にセットする。
    """
    def __init__(
            self,
            template_contents: list[Image],
            template_content_type: str,
            total_number_of_contents: int
    ) -> None:
        self.template_slide = TemplateSlide(template_contents, template_content_type)
        number_of_slide = math.ceil(total_number_of_contents / len(template_contents))
        self.slides = [Slide() for _ in range(number_of_slide)]

    def set_textboxes_to_template(self, textboxes: list):
        self.template_slide.set_textboxes(textboxes)

    def set_sequence_images_to_slides(self, grouped_images: dict[str, list[LabeledImage]]):
        """
        順序画像をセットする。(複数グループを持つ画像を許容しない)
        """
        if (group_id := self.__get_single_group_id(grouped_images)) is None:
            raise Exception("Group exists two or more.")
        images = grouped_images[group_id]
        template_contents = self.template_slide.get_first_group_of_contents(config.IMAGE_KEY)
        image_index = 0

        for slide in self.slides:
            temp_contents = []

            for content in template_contents:
                image = images[image_index]
                temp_contents.append(
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

            slide.set_contents(config.IMAGE_KEY, temp_contents, group_id)

    def set_laidout_images_to_slides(self, grouped_images: dict[str, list[LabeledImage]]):
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
        for slide in self.slides:
            template_contents = deepcopy(self.template_slide.contents)
            current_label = 0

            for template_group, group in itertools.zip_longest(template_contents, slide.contents):
                # 終了条件
                if not group:
                    return

                for textbox in template_group["textbox"]:
                    textbox["text"] = re.sub(config.REGEX_POINTING_GROUP, group["group_id"], textbox["text"])
                    if re.search(config.REGEX_POINTING_LABEL, textbox["text"]):
                        replaced_label = group["image"][current_label]
                        textbox["text"] = re.sub(config.REGEX_POINTING_LABEL, replaced_label, textbox["text"])
                        current_label += 1

                group["textbox"] = template_group["textbox"]

    @staticmethod
    def __generate_dict_items_generator(dict: dict) -> Iterator[tuple[str, list[Image]]]:
        for k, v in dict.items():
            yield k, v

    @staticmethod
    def __get_single_group_id(grouped_contents: dict[str, list[LabeledImage]]):
        # 複数group存在する場合弾く
        if len(group_ids := [key for key in grouped_contents.keys()]) != 1:
            return
        return group_ids[0]
