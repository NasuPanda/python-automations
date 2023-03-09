"""法線ベクトル"""

import numpy as np
import open3d as o3d


def __print_start(method):
    print(f"[Start] {method}")


def __print_finish(method):
    print(f"[Finish] {method}")


def estimate_normals(
    pcd: o3d.geometry.PointCloud,
    radius=0.1,
    max_nn=30,
) -> None:
    """点群に法線を付与する
    NOTE: 返り値は無い

    Args:
        pcd (o3d.geometry.PointCloud): 点群データ
        radius (float, optional): 探索範囲. デフォルトは 0.1.
        max_nn (int, optional): 考慮する最大近傍点数. デフォルトは 30.
    """
    __print_start("Estimating normals")
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius, max_nn=max_nn))
    __print_finish("Estimating normals")


def orient_normals_towards_camera_location(
    pcd_with_normals: o3d.geometry.PointCloud, x=0.0, y=0.0, z=0.0
) -> None:
    """法線の向きをカメラ座標に合わせる

    Args:
        pcd_with_normals (o3d.geometry.PointCloud): 法線を持った点群データ
        x (float, optional): カメラ座標(x). Defaults to 0.0.
        y (float, optional): カメラ座標(y). Defaults to 0.0.
        z (float, optional): カメラ座標(z). Defaults to 0.0.
    """
    if not pcd_with_normals.has_normals():
        print("点群が法線を持っていません。処理を中断します")
        return
    pcd_with_normals.orient_normals_towards_camera_location(np.array([x, y, z]))


def orient_normals_tangent_place(pcd_with_normals: o3d.geometry.PointCloud, k=10) -> None:
    """法線方向の一貫性を保つ処理。法線を一貫した接平面に対して方向付ける

    Args:
        pcd_with_normals (o3d.geometry.PointCloud): 法線を持った点群データ
        k (int, optional): 法線方向を伝達するためのリーマングラフを構成する際に利用される，最近傍の k 個の数 デフォルトは 10.
    """
    if not pcd_with_normals.has_normals():
        print("点群が法線を持っていません。処理を中断します")
        return

    __print_start("Orient the normals with respect to consistent tangent planes")
    pcd_with_normals.orient_normals_consistent_tangent_plane(k)
    __print_finish("Orient the normals with respect to consistent tangent planes")
