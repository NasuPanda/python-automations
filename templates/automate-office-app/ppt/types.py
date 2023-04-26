from dataclasses import dataclass
from typing import NamedTuple, TypeAlias

from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE


class ShapeTypes(NamedTuple):
    """Shapeオブジェクトの型
    TODO 頻繁に使うShapeの型はここに追加しておくと楽
    """

    rectangle: int = MSO_SHAPE.RECTANGLE
    textbox: int = MSO_SHAPE_TYPE.TEXT_BOX


SHAPE_TYPES = ShapeTypes()

"""
PresentationAccessorで使う型
"""
SlideKey: TypeAlias = int


class LayoutInfo(NamedTuple):
    name: str
    # NOTE: indexだと名前被りを起こす
    number: int


"""
コンテンツの型
"""


@dataclass
class Coordinates:
    left: int
    top: int


@dataclass
class Size:
    width: int
    height: int


@dataclass
class Content:
    """コンテンツ"""

    coordinates: Coordinates
    size: Size
    text: str = ""


@dataclass
class Picture:
    """画像"""

    coordinates: Coordinates
    size: Size
    path: str
