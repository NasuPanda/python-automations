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

    def get_textbox(self, slide_index=0) -> list[TextBox]:
        """スライドが持つテキストボックスの情報を取得"""
        return self.__get_contents(
            content_type=config.TEXTBOX_KEY,
            shape_type=MSO_SHAPE_TYPE.TEXT_BOX,
            slide_index=slide_index
        )

    def __set_content(self, content_type: str, shape) -> Image | TextBox:
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

    def __get_contents(self, content_type: str, shape_type: MSO_SHAPE | MSO_SHAPE_TYPE, slide_index=0):
        """特定のshape_typeを取得"""
        contents: list[Image | TextBox] = []
        shapes = self.prs.slides[slide_index].shapes

        for shape in shapes:
            if shape.shape_type != shape_type:
                continue
            if not shape.text:
                continue
            contents.append(self.__set_content(content_type, shape))

        return contents


class PresentationWriter():
    """プレゼンテーションを出力するクラス。"""
    def __init__(self, path: str, slides: list[Slide]) -> None:
        self.prs: Presentation = Presentation(path)
        self.slides: list[Slide] = slides

        # 優先順位: 白紙 > タイトルとコンテンツ > 最後
        # get_by_nameは存在しない場合Noneを返す
        self.layout = self.prs.slide_layouts.get_by_name("白紙")
        if not self.layout:
            self.layout = self.prs.slide_layouts.get_by_name("タイトルとコンテンツ")
        if not self.layout:
            self.layout = self.prs.slide_layouts[-1]

    def add_slide(self):
        """空のスライドを追加する。
        """
        return self.prs.slides.add_slide(self.layout)

    def __get_slide_index(self, slide) -> int:
        """スライドのindexを取得する。
        """
        return self.prs.slides.index(slide)

    def duplicate_slide(self, base_slide_index=0) -> int:
        """スライドを複製する。
        参考 : https://stackoverflow.com/questions/50866634/python-pptx-copy-slide

        Parameters
        ----------
        base_slide_index : int, optional
            複製元スライドのインデックス, by default 0

        Returns
        -------
        int
            複製したスライドのインデックス。
        """
        base_slide = self.prs.slides[base_slide_index]
        duplicate_slide = self.add_slide()
        for shape in base_slide.shapes:
            el = shape.element
            new_el = deepcopy(el)
            duplicate_slide.shapes._spTree.insert_element_before(new_el, "p:extLst")
        return self.__get_slide_index(duplicate_slide)

    def __paste_img(
                self,
                coordinates: tuple[int, int],
                sizes: tuple[int, int],
                img: str,
                slide_index=1
        ):
        """スライドに画像を貼り付ける。
        """
        shapes = self.prs.slides[slide_index].shapes
        shapes.add_picture(img, *coordinates, *sizes)