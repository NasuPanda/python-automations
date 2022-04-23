import math
from typing import Iterator, TypedDict, Union, Optional
from Models.sorter import LabeledImage

import config
from Models.content import Image, TextBox


class SlideContents(TypedDict, total=False):
    """SlideContentの集合"""
    group_id: str
    image: list[Image]
    textbox: list[TextBox]


class Slide():
    """スライドクラス"""
    def __init__(self) -> None:
        self.contents: list[SlideContents] = []

    def set_contents(self, content_type: str, contents: list[Union[Image, TextBox]], group_id: str):
        """指定したgroup_id, content_typeにcontentsをセット"""
        # group_idが存在しない場合は新たに追加
        new_contents: SlideContents = {"group_id": group_id, content_type: contents}  # type: ignore
        self.contents.append(new_contents)

    def set_content(self, content_type: str, content: Union[Image, TextBox], group_id: str):
        for _contents in self.contents:
            if _contents["group_id"] == group_id:
                _contents[content_type].append(content)
                return

        new_contents: SlideContents = {"group_id": group_id, content_type: [content]}  # type: ignore
        self.contents.append(new_contents)

    def __search_contents_by_group_id(self, group_id: str | None) -> SlideContents:
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
        # := は walrus operator, 代入に使う
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
        group_ids: set[str] = set([i[0] for i in splits])
        new_labels: set[str] = set([i[1] for i in splits])
        # labels = [1_A, 1_B, 2_A] のようにlabelの数が一致していない場合は弾く
        if len(template_contents) != len(group_ids) * len(new_labels):
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

class SlideGenerator():
    def __init__(
            self,
            labeld_contents: dict[str, list[LabeledImage]],
            template_contents: list[Image],
            template_content_type: str = config.IMAGE_KEY
    ) -> None:
        self.grouped_contents = labeld_contents
        self.template_slide = TemplateSlide(template_contents, template_content_type)

        total_number_of_contents = 0
        [total_number_of_contents := total_number_of_contents + len(contents_group) for contents_group in labeld_contents.values()]
        number_of_slide = math.ceil(total_number_of_contents / len(template_contents))
        self.slides = [Slide() for _ in range(number_of_slide)]

    def set_sequence_images(self):
        if (group_id := self.__get_single_group_id()) is None:
            raise Exception("Group exists two or more.")
        labeld_images = self.grouped_contents[group_id]
        template_contents = self.template_slide.get_first_group_of_contents(config.IMAGE_KEY)
        image_index = 0

        for slide in self.slides:
            temp_contents = []
            for content in template_contents:
                image = labeld_images[image_index]
                temp_contents.append(
                    Image(
                        coordinates=content["coordinates"],
                        size=content["size"],
                        label=image["label"],
                        path=image["path"]
                    )
                )
                image_index += 1
                # スライド数×1スライドのコンテンツ数 != コンテンツ数の合計の時
                if image_index == len(labeld_images):
                    break
            slide.set_contents(config.IMAGE_KEY, temp_contents, group_id)

    def set_laidout_images(self):
        labled_image_generator = self.__generate_dict_items_generator(self.grouped_contents)

        for slide in self.slides:
            for searching_group_id in range(1, self.template_slide.get_number_of_group() + 1):
                try:
                    new_group_id, images = next(labled_image_generator)
                except StopIteration:
                    break
                temp_contents = []
                for image in images:
                    content = self.template_slide.search_content_by_label(config.IMAGE_KEY, image["label"], str(searching_group_id))
                    temp_contents.append(
                        Image(
                            coordinates=content["coordinates"],
                            size=content["size"],
                            label=content["label"],
                            path=image["path"]
                        ),
                    )
                slide.set_contents(config.IMAGE_KEY, temp_contents, new_group_id)

    def __generate_dict_items_generator(self, dict: dict) -> Iterator[tuple[str, list[Image]]]:
        for k, v in dict.items():
            yield k, v

    def __get_single_group_id(self):
        # 複数group存在する場合弾く
        if len(group_ids := [key for key in self.grouped_contents.keys()]) != 1:
            return
        return group_ids[0]
