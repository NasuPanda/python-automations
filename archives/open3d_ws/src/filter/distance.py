"""距離によるフィルタリング
"""

import open3d as o3d

from src.common import getter


def filter_by_distance(pcd: o3d.geometry.PointCloud, distance=10) -> o3d.geometry.PointCloud:
    # enumerate(zip(x, y, z))
    inlier_indexes = [
        i
        for i, (x, y, z) in enumerate(zip(*getter.get_xyz(pcd)))
        if x**2 + y**2 + z**2 <= distance**2
    ]
    return pcd.select_by_index(inlier_indexes)
