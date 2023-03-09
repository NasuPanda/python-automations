from dataclasses import dataclass

from openpyxl.utils.cell import get_column_letter


def _get_anchor_from_index(row: int, column: int) -> str:
    """Get anchor letter from row and column integer index"""
    return get_column_letter(column) + str(row)


@dataclass
class AttachedImage:
    """Attached image in Excel.

    NOTE: Adjust width and height based on default cell w/h.

    Example:
        img.width = 72 * 10
        img.height = 25 * 13

    References:
        - https://openpyxl.readthedocs.io/en/stable/api/openpyxl.worksheet.worksheet.html?highlight=add_image#openpyxl.worksheet.worksheet.Worksheet.add_image
        - https://openpyxl.readthedocs.io/en/stable/api/openpyxl.drawing.image.html?highlight=drawing#openpyxl.drawing.image.Image

    Arguments:
        filename: str
            画像のパス
        width: int
            画像の幅
        height: int
            画像の高さ
        anchor: str
            画像の位置(ex: A1, T4, ...)
    """

    filename: str
    width: int | float
    height: int | float
    anchor: str

    def __init__(
        self,
        filename: str,
        width: int | float,
        height: int | float,
        row_index: int,
        column_index: int,
        anchor_letter: None | str = None,
    ) -> None:
        self.filename = filename
        self.width = width
        self.height = height
        if anchor_letter:
            self.anchor = anchor_letter
        else:
            self.anchor = _get_anchor_from_index(row=row_index, column=column_index)
