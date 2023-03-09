"""
- Open3d形式の点群をnumpy形式に変換
- Open3d形式の点群を結合
- ROS座標系の点群を通常の座標系に変換
"""

import numpy as np
import open3d as o3d


def ndarray2o3d(array):
    """float64のnumpy配列（n, 3）をOpen3Dフォーマットに変換"""
    return o3d.utility.Vector3dVector(array)


def o3d2ndarray(points):
    """Open3Dフォーマットのデータをfloat64のnumpy配列(n,3)に変換"""
    return np.asarray(points)


def concat_point_clouds(point_clouds):
    """点群の配列を結合する
    NOTE: RGB, normalが無い場合を考慮していないので注意
    """
    points_array = []
    colors_array = []
    normals_array = []

    for p in point_clouds:
        points_array.append(o3d2ndarray(p.points))
        colors_array.append(o3d2ndarray(p.colors))
        normals_array.append(o3d2ndarray(p.normals))

    pcd = o3d.geometry.PointCloud()
    pcd.points = ndarray2o3d(np.concatenate(points_array, axis=0))
    pcd.colors = ndarray2o3d(np.concatenate(colors_array, axis=0))
    pcd.normals = ndarray2o3d(np.concatenate(normals_array, axis=0))

    return pcd


def normalize_ros_xyz(pcd) -> o3d.geometry.PointCloud:
    """ROSのXYZ座標(右手系)を通常のXYZ座標に変換する
    FIXME: 名前
    """
    return pcd.rotate(np.array([[0, 1, 0], [0, 0, 1], [-1, 0, 0]]))
