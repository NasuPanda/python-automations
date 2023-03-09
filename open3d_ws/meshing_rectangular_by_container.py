"""点が均等に配置されていることを前提にSORCをメッシュ化。自力で法線ベクトルを付与する。

NOTE
- 欠損値扱いをする要素は None/nan で埋める。座標に0が存在するため0埋めはしない。
- Open3D の visualizer は None/nan を含むデータを許容しないので、表示前に0等に置換する必要がある。
"""

import numpy as np

from src.common import converter, display, file_io, getter
from src.filter import rgb_filter
from src.mesh import meshing

X = 200
Y = 70
Z = 70
POINTS_1D_SHAPE = (Z * Y * X, 3)
POINTS_3D_SHAPE = (Z, Y, X, 3)
POINTS_3D_CONTAINER_SHAPE = (Z + 2, Y + 2, X + 2, 3)
filepath = "./data/sample.ply"


def main():
    # テスト用
    # X = 10
    # Y = 10
    # Z = 10
    # points_container = np.full((Z + 2, Y + 2, X + 2, 3), None)
    # normals = np.zeros((Z,Y,X, 3))
    # points_for_create_pcd = []
    # for _x in range(Z):
    #     for _y in range(Y):
    #         for _z in range(X):
    #             points_for_create_pcd.append([_x, _y, _z])
    # pcd = o3d.geometry.PointCloud(points=o3d.utility.Vector3dVector(points_for_create_pcd))

    # 1マス分余分な空間を持ったnan埋めのコンテナを作る
    # このコンテナの内側に実際の値を格納することで、値がnanの箇所=データが存在しない領域とすることが出来る
    points_container = np.full(POINTS_3D_CONTAINER_SHAPE, np.nan)
    # 法線を格納する配列
    normals = np.zeros(POINTS_3D_SHAPE)

    # 点群読み込み
    pcd = file_io.read_point_cloud(filepath)
    # RGBフィルタリング: 空乏に当たる空間をnanに置換する
    rgb_filter.filter_points_by_rgb(pcd, r=255.0)

    points = getter.get_points(pcd)
    colors = getter.get_color_points(pcd)

    # points の整形
    points = points.flatten().reshape(POINTS_3D_SHAPE)
    # コンテナ配列に points を代入
    points_container[1:-1, 1:-1, 1:-1] = points

    print("Original: ", pcd)
    print("points shape", points.shape, "container shape", points_container.shape)

    # NOTE 法線ベクトルに使う点間のキョリ
    distance = 1

    print("[Start] Estimate normals...")
    for z_index in range(1, Z + 1):
        for y_index in range(1, Y + 1):
            for x_index in range(1, X + 1):
                x_vec, y_vec, z_vec = 0, 0, 0
                # 中心
                # xc, yc, zc = points_container[z_index][y_index][x_index]
                # X方向 xr:右 xl:左
                xr, _, _ = points_container[z_index][y_index][x_index + 1]
                xl, _, _ = points_container[z_index][y_index][x_index - 1]
                # Y方向 yt:上 yb:下
                _, yt, _ = points_container[z_index][y_index + 1][x_index]
                _, yb, _ = points_container[z_index][y_index - 1][x_index]
                # Z方向 zb:奥 zf:手前
                _, _, zb = points_container[z_index + 1][y_index][x_index]
                _, _, zf = points_container[z_index - 1][y_index][x_index]

                # 隣接する点群の値がnan=存在しない場合ベクトル計算を行う
                if np.isnan(xr):
                    x_vec += distance
                if np.isnan(xl):
                    x_vec -= distance
                if np.isnan(yt):
                    y_vec += distance
                if np.isnan(yb):
                    y_vec -= distance
                if np.isnan(zb):
                    z_vec += distance
                if np.isnan(zf):
                    z_vec -= distance

                normals[z_index - 1][y_index - 1][x_index - 1] = [x_vec, y_vec, z_vec]
    print("[Finish] Estimate normals...")

    # 点群表示 Open3Dは表示前に None / nan の置換が必須
    pcd.points = converter.ndarray2o3d(np.nan_to_num(points.flatten().reshape(POINTS_1D_SHAPE)))
    pcd.colors = converter.ndarray2o3d(np.nan_to_num(colors))
    pcd.normals = converter.ndarray2o3d(normals.flatten().reshape(POINTS_1D_SHAPE))
    display.display(pcd, point_show_normal=True)

    # メッシュ化
    mesh = meshing.reconstruct_by_poisson(pcd, display_result=True)
    # file_io.write_mesh("./result.ply", mesh)


if __name__ == "__main__":
    main()
