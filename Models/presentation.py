from copy import deepcopy

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE

import config
from Models.slide import Slide
from Models.content import SlideContent


class PresentationReader():
    """プレゼンテーションを読み込むクラス。"""
    def __init__(self, path: str) -> None:
        self.prs: Presentation = Presentation(path)
        # TODO
        self.template_slide
        self.contents: dict[str, list[SlideContent]] = {}

    def __set_contents(self, key=config.IMAGE_KEY, shape_type=MSO_SHAPE.RECTANGLE, index=0):
        """特定のshape_typeのテキストを取得"""
        contents: list[SlideContent] = []
        shapes = self.prs.slides[index].shapes

        for shape in shapes:
            if not shape.shape_type == shape_type:
                continue
            if not shape.text:
                continue
            contents.append(
                SlideContent(
                    coordinates=(shape.left, shape.top), size=(shape.width, shape.height), label=shape.text
                )
            )

        self.contents[key] = contents

    def set_imgs(self, index=0):
        """スライドが持つ画像の情報をセットする(RECTANGLEを使用)"""
        self.imgs = self.__set_contents(key=config.IMAGE_KEY, shape_type=MSO_SHAPE.RECTANGLE, index=index)

    def set_textbox(self, index=0):
        """スライドが持つテキストボックスの情報をセットする"""
        self.textboxes = self.__set_contents(key=config.TEXTBOX_KEY, shape_type=MSO_SHAPE_TYPE.TEXT_BOX, index=index)

    def get_contents(self, key=config.IMAGE_KEY):
        """スライドが持つコンテンツを情報を取得する"""
        return self.contents.get(key)


class PresentationWriter():
    """プレゼンテーションを出力するクラス。"""
    def __init__(self, path: str) -> None:
        self.slides: list[Slide] = []
        self.prs: Presentation = Presentation(path)