from typing import TypedDict, Union

import config
from Models.content import Image, TextBox


class SlideContents(TypedDict, total=False):
    """SlideContentの集合"""
    image: list[Image]
    textbox: list[TextBox]


class Slide():
    """スライドクラス"""
    def __init__(self) -> None:
        self.labels: tuple[str, ...]
        self.contents: SlideContents = {}

    def set_contents(self, content_type: str, contents: list[Union[Image, TextBox]]):
        """指定したcontent_typeにcontentsをセット"""
        self.contents[content_type] = contents

    def get_labels(self, content_type: str) -> list[str]:
        return [content["label"] for content in self.contents[content_type]]

    def get_coordinates_and_sizes(self, content_type: str):
        return [(*content["coordinates"], *content["size"]) for content in self.contents[content_type]]

    def get_number_of_contents(self, content_type: str):
        return len(self.contents[content_type])
