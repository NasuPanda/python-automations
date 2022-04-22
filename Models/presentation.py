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

    def get_imgs(self, slide_index=0) -> list[Image]:
        """スライドが持つ画像の情報を取得(RECTANGLEを使用)"""
        return self.__get_contents(
            content_type=config.IMAGE_KEY,
            shape_type=MSO_SHAPE.RECTANGLE,
            slide_index=slide_index
        )

    def get_textbox(self, slide_index=0):
        """スライドが持つテキストボックスの情報を取得"""
        return self.__get_contents(
            content_type=config.TEXTBOX_KEY,
            shape_type=MSO_SHAPE_TYPE.TEXT_BOX,
            slide_index=slide_index
        )

    def __set_content(self, content_type: str, shape) -> Union[Image, TextBox]:
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

    def __get_contents(self, content_type: str, shape_type: Union[MSO_SHAPE, MSO_SHAPE_TYPE], slide_index=0):
        """特定のshape_typeを取得"""
        contents: list[Union[Image, TextBox]] = []
        shapes = self.prs.slides[slide_index].shapes

        for shape in shapes:
            if not shape.shape_type == shape_type:
                continue
            if not shape.text:
                continue
            contents.append(self.__set_content(content_type, shape))

        return contents


class PresentationWriter():
    """プレゼンテーションを出力するクラス。"""
    def __init__(self, path: str) -> None:
        self.slides: list[Slide] = []
        self.prs: Presentation = Presentation(path)