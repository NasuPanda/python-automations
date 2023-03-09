"""点やメッシュを切り出す"""

import itertools
import math
from typing import Literal

import open3d as o3d

from src.common import getter

AXIS = Literal["x", "y", "z"]


def create_bounding_box_by_coordinate(
    min_x=-math.inf,
    max_x=math.inf,
    min_y=-math.inf,
    max_y=math.inf,
    min_z=-math.inf,
    max_z=math.inf,
) -> o3d.geometry.AxisAlignedBoundingBox:
    """座標を元に点群やメッシュを分割する BoundingBox を生成する"""
    bounds = [[min_x, max_x], [min_y, max_y], [min_z, max_z]]
    bounding_box_points = list(itertools.product(*bounds))
    return o3d.geometry.AxisAlignedBoundingBox.create_from_points(
        o3d.utility.Vector3dVector(bounding_box_points)
    )


def create_bounding_box_by_axis(pcd, axis: AXIS = "x", slice_num=10):
    """指定軸を基準として、点群やメッシュをN分割する BoundingBox を生成する"""
    x, y, z = getter.get_xyz(pcd)
    min_x, max_x = x.min(), x.max()
    min_y, max_y = y.min(), y.max()
    min_z, max_z = z.min(), z.max()

    bounding_boxes = []

    # 基準軸を元に以下を定義
    # 1ステップごとに進む値,  表示範囲の最大値(初回ループ)
    if axis == "x":
        step_value = (max_x - min_x) / slice_num
        max_x = min_x + step_value
    elif axis == "y":
        step_value = (max_y - min_y) / slice_num
        max_y = min_y + step_value
    elif axis == "z":
        step_value = (max_z - min_z) / slice_num
        max_z = min_z + step_value
    else:
        raise ValueError(f"{axis} は無効な引数です。xyzのいずれかを指定してください。")

    for i in range(slice_num):
        print(f"SLICE{i+1} X:{min_x}~{max_x} Y:{min_y}~{max_y} Z:{min_z}~{max_z}")
        bb = create_bounding_box_by_coordinate(min_x, max_x, min_y, max_y, min_z, max_z)

        if axis == "x":
            min_x += step_value
            max_x += step_value
        elif axis == "y":
            min_y += step_value
            max_y += step_value
        elif axis == "z":
            min_z += step_value
            max_z += step_value

        bounding_boxes.append(bb)

    return bounding_boxes


def create_bounding_box_by_ratio(
    pcd, min_x_ratio=0.0, max_x_ratio=1.0, min_y_ratio=0.0, max_y_ratio=1.0, min_z_ratio=0.0, max_z_ratio=1.0
):
    """点群が持つXYZ座標の最大/最小値に対する比率を元に、点群やメッシュを分割する Bounding Box を生成する
    NOTE: 比率は0.0~1.0
    """
    x, y, z = getter.get_xyz(pcd)
    _min_x, _max_x = x.min(), x.max()
    _min_y, _max_y = y.min(), y.max()
    _min_z, _max_z = z.min(), z.max()

    min_x = _min_x + ((_max_x - _min_x) * min_x_ratio)
    max_x = _min_x + ((_max_x - _min_x) * max_x_ratio)
    min_y = _min_y + ((_max_y - _min_y) * min_y_ratio)
    max_y = _min_y + ((_max_y - _min_y) * max_y_ratio)
    min_z = _min_z + ((_max_z - _min_z) * min_z_ratio)
    max_z = _min_z + ((_max_z - _min_z) * max_z_ratio)

    print("Crop by ratio.\n")
    print(
        f"\tRatio\nX:{min_x_ratio}~{max_x_ratio} Y:{min_y_ratio}~{max_y_ratio} Z:{min_z_ratio}~{max_z_ratio}"
    )
    print(f"\tCoordinates\nX:{min_x}~{max_x} Y:{min_y}~{max_y} Z:{min_z}~{max_z}")

    return create_bounding_box_by_coordinate(min_x, max_x, min_y, max_y, min_z, max_z)


def crop_pcd_by_coordinates(
    pcd,
    min_x=-math.inf,
    max_x=math.inf,
    min_y=-math.inf,
    max_y=math.inf,
    min_z=-math.inf,
    max_z=math.inf,
):
    """座標を元に点群やメッシュを切り出す"""
    bounding_box = create_bounding_box_by_coordinate(min_x, max_x, min_y, max_y, min_z, max_z)
    return pcd.crop(bounding_box)


def crop_pcd_by_axis(pcd, axis: AXIS = "x", slice_num=10):
    """指定軸を基準として点群やメッシュをN分割する"""
    bounding_boxes = create_bounding_box_by_axis(pcd, axis, slice_num)
    return [pcd.crop(box) for box in bounding_boxes]


def crop_pcd_by_ratio(
    pcd, min_x_ratio=0.0, max_x_ratio=1.0, min_y_ratio=0.0, max_y_ratio=1.0, min_z_ratio=0.0, max_z_ratio=1.0
):
    """点群が持つXYZ座標の最大/最小値に対する比率を元に点群やメッシュを分割する
    NOTE: 比率は0.0~1.0
    """
    bounding_box = create_bounding_box_by_ratio(
        pcd, min_x_ratio, max_x_ratio, min_y_ratio, max_y_ratio, min_z_ratio, max_z_ratio
    )
    return pcd.crop(bounding_box)
