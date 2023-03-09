"""RGB関連"""

from dataclasses import dataclass


@dataclass
class RGB_INDEX:
    """Open3DのcolorsにおけるRGBのインデックス"""

    R = 0
    G = 1
    B = 2


def _validate_color(color):
    """RGB値のバリデーション"""
    if 0.0 <= color <= 255.0:
        return
    else:
        raise ValueError(f"{color} は 0 ~ 255 で指定してください")


def rgb2o3d(rgb_value):
    """RGB値(0~255)をOpen3Dフォーマット(0~1)に変換"""
    _validate_color(rgb_value)
    return rgb_value / 255.0


def paint_pcd_to_uniform_color(pcd, rgb) -> None:
    """点群を単色に染める"""
    color = [rgb2o3d(rgb[RGB_INDEX.R]), rgb2o3d(rgb[RGB_INDEX.G]), rgb2o3d(rgb[RGB_INDEX.B])]
    pcd.paint_uniform_color(pcd, color)
