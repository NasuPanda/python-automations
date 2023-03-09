"""RGB値によるフィルター"""

import numpy as np

from src.common import converter, getter, rgb


def _flat_where(query):
    """np.where の結果を1次元の配列として返す(元はtuple)"""
    return np.array(np.where(query)).flatten()


def filter_points_by_rgb(pcd, r=None, g=None, b=None, value_to_fill=np.nan) -> None:
    """指定色の点群を指定値に置換する
    NOTE: 単色のみ, RGB値は 0 ~ 255 で指定する
    """
    # RGB 情報を持っていなければ早期return
    if not pcd.has_colors:
        print("Filter point cloud by RGB is failure.", "Input pcd hasn't RGB color.")
        return
    # (N, 3)の要素が対象なので[None,None,None]にしておく
    values_to_fill = [value_to_fill] * 3

    points = getter.get_points(pcd)
    colors = getter.get_color_points(pcd)

    # int を指定しておかないと append 時に勝手に float にキャストされてしまう
    target_indexes = np.array([], dtype=int)

    # numpy の append は元配列に破壊的変更を加えないので代入が必要
    if r:
        target_indexes = np.append(target_indexes, _flat_where(colors[:, rgb.RGB_INDEX.R] == rgb.rgb2o3d(r)))
    if g:
        target_indexes = np.append(target_indexes, _flat_where(colors[:, rgb.RGB_INDEX.G] == rgb.rgb2o3d(g)))
    if b:
        target_indexes = np.append(target_indexes, _flat_where(colors[:, rgb.RGB_INDEX.B] == rgb.rgb2o3d(b)))

    # 単に削除する
    # pcd.points = format.ndarray2o3d(np.delete(points, [*target_indexes], 0))
    # pcd.colors = format.ndarray2o3d(np.delete(colors, [*target_indexes], 0))

    # 指定した値に置換する
    points[target_indexes] = values_to_fill
    pcd.points = converter.ndarray2o3d(points)
    colors[target_indexes] = values_to_fill
    pcd.colors = converter.ndarray2o3d(colors)
