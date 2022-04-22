from typing import TypedDict, Union, Optional

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
        self.contents: list[SlideContents] = [{"group_id": "", "image": [], "textbox": []}]

    def set_contents(self, content_type: str, contents: list[Union[Image, TextBox]], group_id: str):
        """指定したgroup_id, content_typeにcontentsをセット"""
        # group_idが既に存在する場合は指定したcontent_typeにcontentsをセット
        for _contents in self.contents:
            if _contents["group_id"] == group_id:
                _contents[content_type] = contents
                return
        # group_idが存在しない場合は新たに追加
        self.contents.append({"group_id": group_id, content_type: contents})

    def set_content(self, content_type: str, content: Union[Image, TextBox], group_id: str):
        for _contents in self.contents:
            if _contents["group_id"] == group_id:
                _contents[content_type].append(content)
                return

        raise KeyError(f"group id doesn't exist: {group_id}")

    def __search_contents_by_group_id(self, group_id: str | None) -> SlideContents:
        if group_id is None:
            return self.contents[0]
        else:
            for contents in self.contents:
                if contents["group_id"] == group_id:
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
        return [count := count + len(i[content_type]) for i in self.contents]

    def get_number_of_group(self):
        return len(self.contents)

    # def get_number_of_group(self, content_type: str = config.IMAGE_KEY) -> int:
    #     """
    #     content.label を id / label に分けてユニークなidをカウント。
    #     labels=[1_A, 1_B, 1_C, 2_A, 2_B, 2_C]の場合, データ数は2。
    #     """
    #     # 全てのcontent["label"]を取得する
    #     labels: list[str] = []
    #     [
    #         [labels.append(content["label"]) for content in searched_contents[content_type]]
    #         for searched_contents in self.contents
    #     ]
    #     # id_labelのみ対応しているため、split => [1, A]以外の形式は弾く
    #     splits = [i.split(config.DELIMITER) for i in labels if len(i.split(config.DELIMITER)) == 2]
    #     if not splits:
    #         return 1

    #     return len(set([i[0] for i in splits]))