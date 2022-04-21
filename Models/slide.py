import config
from Models.content import Contents

class Slide():
    """スライドクラス"""
    def __init__(self) -> None:
        self.labels: tuple[str, ...]
        self.contents: Contents
