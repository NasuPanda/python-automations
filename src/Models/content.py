from typing import TypedDict


class SlideContent(TypedDict):
    """スライドコンテンツ
    """
    coordinates: tuple[int, int]
    size: tuple[int, int]
    label: str


# total=False: 辞書初期化時などにキーが必須で無くなる
class Image(SlideContent, total=False):
    """画像"""
    path: str


class TextBox(SlideContent, total=False):
    """テキストボックス"""
    text: str

