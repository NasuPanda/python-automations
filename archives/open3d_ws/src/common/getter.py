"""点群からpoints, xyz, nearest_neighbor_distanceの平均などを取得する"""

import numpy as np

from src.common import converter


def get_points(pcd):
    """点群をnumpy配列として取得"""
    return converter.o3d2ndarray(pcd.points)


def get_color_points(pcd):
    """点群のRGB値をnumpy配列として取得"""
    return converter.o3d2ndarray(pcd.colors)


def get_normals(pcd):
    """点群の法線をnumpy配列として取得"""
    return converter.o3d2ndarray(pcd.normals)


def get_xyz(pcd):
    """点群の x, y, z をそれぞれ取得"""
    points = get_points(pcd)
    return points[:, 0], points[:, 1], points[:, 2]


def get_xyz_min_max(pcd):
    """xyz座標それぞれの最小値/最大値を取得
    NOTE: x.max(), x.min(), y.max(), y.min(), z.max(), z.min() の順
    """
    x, y, z = get_xyz(pcd)
    return x.max(), x.min(), y.max(), y.min(), z.max(), z.min()


def get_length_of_xyz_side(pcd):
    """xyz辺の長さを返す"""
    x_max, x_min, y_max, y_min, z_max, z_min = get_xyz_min_max(pcd)
    return x_max - x_min, y_max - y_min, z_max - z_min


def compute_nearest_neighbor_distance_avg(pcd) -> float:
    """各点について点群内の最近傍点との距離を求め、その平均を返す
    NOTE:
    - アルゴリズムのパラメータとして使う
    - 0を返す場合がある。その場合は例外を投げる
    """
    distances = pcd.compute_nearest_neighbor_distance()
    distances_avg = np.mean(distances)
    if distances_avg == 0.0:
        raise ValueError(f"Nearest neighbor distances average is invalid: {distances_avg}")
    return distances_avg
