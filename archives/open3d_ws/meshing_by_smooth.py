"""検証中
現在: 輪切りフィルター
"""
import numpy as np
import open3d as o3d

from src.common import converter, display, file_io, getter
from src.filter import crop, down_sample, outlier, plane_segmentation
from src.mesh import meshing, normal

filepath = "./data/sample.ply"

def smooth_x(pcd, sline_num=150):
    """X方向に輪切り、Xの値を均す"""
    # X方向に輪切り
    point_clouds = crop.crop_pcd_by_axis(pcd, "x", sline_num)
    filtered_point_clouds = []

    for p in point_clouds:
        # 空だったらスキップする
        if p.is_empty():
            continue

        # 処理
        points = getter.get_points(p)
        x, _y, _z = points[:, 0], points[:, 1], points[:, 2]
        # 平均値で埋める
        x.fill(x.mean())
        points[:, 0] = x
        p.points = converter.ndarray2o3d(points)

        filtered_point_clouds.append(p)

    # pcd を結合
    return converter.concat_point_clouds(filtered_point_clouds)


def smooth_y(pcd, slice_num=150):
    """Y方向に輪切り、Yの値を均す"""
    # Y方向に輪切り
    point_clouds = crop.crop_pcd_by_axis(pcd, "y", slice_num)
    filtered_point_clouds = []

    for p in point_clouds:
        # 空だったらスキップする
        if p.is_empty():
            continue

        # 処理
        points = getter.get_points(p)
        _x, y, _z = points[:, 0], points[:, 1], points[:, 2]
        # 平均値で埋める
        y.fill(y.mean())
        points[:, 1] = y
        p.points = converter.ndarray2o3d(points)

        filtered_point_clouds.append(p)

    # pcd 結合
    return converter.concat_point_clouds(filtered_point_clouds)


def smooth_z(pcd, slice_num=300):
    """Z方向に輪切り、Zの値を均す"""
    # Z方向に輪切り
    point_clouds = crop.crop_pcd_by_axis(pcd, "z", slice_num)
    filtered_point_clouds = []

    for p in point_clouds:
        # 空だったらスキップする
        if p.is_empty():
            continue

        # 処理
        points = getter.get_points(p)
        _x, _y, z = points[:, 0], points[:, 1], points[:, 2]
        # 平均値で埋める
        z.fill(z.mean())
        points[:, 2] = z
        p.points = converter.ndarray2o3d(points)

        filtered_point_clouds.append(p)

    # pcd 結合
    return converter.concat_point_clouds(filtered_point_clouds)


def crop_and_meshing():
    """刻んでからメッシュ化"""
    # 1. 点群読み込み
    pcd_original = file_io.read_point_cloud(filepath)
    average_distance = getter.compute_nearest_neighbor_distance_avg(pcd_original)

    # 2. 前処理
    # ■ ダウンサンプリング: average distance の2~4倍
    pcd_original = down_sample.voxel_down_sample(pcd_original, average_distance * 2)

    # ■ Cropの用意
    # pcd を格納しておく配列
    point_clouds = []
    # x, z のcropに使う値: x方向2分割, z方向10分割
    z_mins = np.arange(0.0, 1.0, 0.1)
    z_maxs = z_mins + 0.1
    x_mins = np.array([0.0, 0.5])
    x_maxs = x_mins + 0.5

    # ■ オドメトリ (rosbagデータ参照) の用意
    x_odom = -0.15
    y_odom = -0.635  # 固定 とりあえずmin/maxの中間取る
    z_odom = -23.76
    # オドメトリのステップ量 : (max - min) / (分割する数 - 1)
    z_odom_step = (12.15 - (-23.76)) / (10 - 1)
    x_odom_step = (9.96 - (-0.15)) / (2 - 1)
    # 現在のオドメトリ
    current_x_odom = x_odom
    current_z_odom = z_odom

    # ■ Crop → 点群を均す → 法線付与 → オドメトリを元に、法線をカメラ座標に向ける
    for z_min, z_max in zip(z_mins, z_maxs):
        for x_min, x_max in zip(x_mins, x_maxs):
            print("x", x_min, x_max, "z", z_min, z_max, "odom:", current_x_odom, y_odom, current_z_odom)

            # crop
            pcd = crop.crop_pcd_by_ratio(
                pcd_original,
                min_x_ratio=x_min,
                max_x_ratio=x_max,
                min_z_ratio=z_min,
                max_z_ratio=z_max,
                max_y_ratio=0.45,
            )

            if pcd.is_empty():
                continue

            # 点群を均す
            pcd = smooth_x(pcd)
            pcd = smooth_y(pcd)
            pcd = smooth_z(pcd)

            # 3. 法線付与
            normal.estimate_normals(pcd, radius=average_distance * 3, max_nn=10)
            # 法線が無い状態で orient を呼ぶとエラー吐くので
            if not pcd.has_normals():
                continue

            # 法線補正
            normal.orient_normals_towards_camera_location(pcd, current_x_odom, y_odom, current_z_odom)
            point_clouds.append(pcd)

            # オドメトリ操作
            current_x_odom += x_odom_step
        # オドメトリ操作
        current_x_odom = x_odom
        current_z_odom += z_odom_step

    # 全点群結合
    pcd = converter.concat_point_clouds(point_clouds)
    print("Result:", pcd)
    display.display(pcd, point_show_normal=True)

    # ■ 外れ値除去
    # inlier_index = outlier.get_statistical_not_outlier_index(pcd)  # 可視化
    # display.display_inlier_outlier(pcd, inlier_index)  # 可視化
    # pcd = outlier.remove_statistical_outlier(pcd)

    # 4. メッシュ化
    # Alpha Shapes
    # for alpha in [0.08, 0.1]:
    #     mesh = meshing.reconstruct_by_alpha_shapes(pcd, alpha, display_result=True)
    #     file_io.write_mesh(f"./fullmap_mesh_by_alpha-{alpha}.ply", mesh)
    # Ball Pivoting
    # mesh = meshing.reconstruct_by_ball_pivoting(pcd, display_result=True)
    # file_io.write_mesh(f"./fullmap_mesh_by_BPA.ply")
    # Poisson
    mesh = meshing.reconstruct_by_poisson(
        pcd,
        display_result=True,
        display_density_colormap=True,
        low_density_threshold=0.2,
        remove_low_densities=True,
    )


def main():
    """点群均す処理のみしてからメッシュ化"""
    pcd = file_io.read_point_cloud(map_minimum_path)
    pcd = crop.crop_pcd_by_ratio(pcd, max_y_ratio=0.5)

    pcd = smooth_x(pcd, 120)
    pcd = smooth_y(pcd, 150)
    pcd = smooth_z(pcd, 300)

    display.display(pcd)

    normal.estimate_normals(pcd)
    normal.orient_normals_towards_camera_location(pcd)
    meshing.reconstruct_by_alpha_shapes(pcd, alpha=0.15, display_result=True)
    meshing.reconstruct_by_ball_pivoting(pcd, display_result=True)


if __name__ == "__main__":
    # main()
    crop_and_meshing()
