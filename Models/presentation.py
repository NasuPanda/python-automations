from typing import Union
from copy import deepcopy

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE

import config
from Models.slide import Slide
from Models.content import SlideContent, Image, TextBox


class PresentationReader():
    """プレゼンテーションを読み込むクラス。"""
    def __init__(self, path: str) -> None:
        self.prs: Presentation = Presentation(path)
        self.template_slide: Slide = Slide()

    def __create_content(self, content_type: str, shape) -> Union[Image, TextBox]:
        if content_type == config.IMAGE_KEY:
            return Image(
                coordinates=(shape.left, shape.top),
                size=(shape.width, shape.height),
                label=shape.text,
                path=""
            )
        if content_type == config.TEXTBOX_KEY:
            return TextBox(
                coordinates=(shape.left, shape.top),
                size=(shape.width, shape.height),
                label=shape.text,
                text=shape.text
            )

    def __set_contents(self, content_type: str, shape_type: Union[MSO_SHAPE, MSO_SHAPE_TYPE], index=0):
        """特定のshape_typeのテキストを取得"""
        contents: list[Union[Image, TextBox]] = []
        shapes = self.prs.slides[index].shapes

        for shape in shapes:
            if not shape.shape_type == shape_type:
                continue
            if not shape.text:
                continue
            contents.append(self.__create_content(content_type, shape))

        self.template_slide.set_contents(content_type, contents)

    def set_imgs(self, index=0):
        """スライドが持つ画像の情報をセットする(RECTANGLEを使用)"""
        self.__set_contents(content_type=config.IMAGE_KEY, shape_type=MSO_SHAPE.RECTANGLE, index=index)

    def set_textbox(self, index=0):
        """スライドが持つテキストボックスの情報をセットする"""
        self.__set_contents(content_type=config.TEXTBOX_KEY, shape_type=MSO_SHAPE_TYPE.TEXT_BOX, index=index)

    def get_contents(self, content_type: str):
        """スライドが持つコンテンツを情報を取得する"""
        return self.template_slide.contents.get(content_type)


class PresentationWriter():
    """プレゼンテーションを出力するクラス。"""
    def __init__(self, path: str) -> None:
        self.slides: list[Slide] = []
        self.prs: Presentation = Presentation(path)