from src.common import converter, display, file_io, getter, rgb
from src.filter import crop, distance, down_sample, outlier, plane_segmentation, rgb_filter
from src.mesh import meshing, normal, smoother

# 1. 点群を読み込んで表示
pcd = file_io.read_point_cloud("./data/sample.ply")
converter.normalize_ros_xyz(pcd)
display.display(pcd)

# 2. 前処理
# ■ 対象物だけ切り出す
# 距離指定
# pcd = distance.filter_by_distance(pcd, 5)
# 座標指定
# pcd = crop.crop_pcd_by_ratio(pcd, 0.5, 0.9, 0.0, 1.0, 0.7, 1.0)

# ■ ダウンサンプリング
# pcd = down_sample.voxel_down_sample(pcd, 0.02)
# display.display(pcd)

# ■ 外れ値除去
display.display_inlier_outlier(pcd, outlier.get_statistical_inliers(pcd))
pcd = outlier.remove_radius_outlier(pcd, radius=0.037)

# ■ 保存
# file_io.write_point_cloud("result.ply", pcd)
# display.display(pcd)

# 3. 法線ベクトル付与
normal.estimate_normals(pcd)
normal.orient_normals_tangent_place(pcd)
# point_show_normal オプションを付けると法線が可視化される
display.display(pcd, point_show_normal=True)

# 4. メッシュ化
# display_result=True とすると結果表示
# ■ Alpha Shapes
# for alpha in [0.02, 0.05, 0.1]:
#     mesh = meshing.reconstruct_by_alpha_shapes(pcd, display_result=True, alpha=alpha)
# file_io.write_mesh(f"./mesh_by_alpha-{alpha}.ply", mesh)

# ■ Ball Pivoting
# パラメータを自分で設定したい場合は以下のような ball_radiuses を用意
# average_distance = getter.compute_nearest_neighbor_distance_avg(pcd_with_normals)
# radius = 2 * average_distance
# ball_radiuses = [radius, radius * 2]
mesh = meshing.reconstruct_by_ball_pivoting(pcd, display_result=True)
# file_io.write_mesh(f"./mesh_by_BPA.ply", mesh)

# ■ Poisson
"""
display_density_colormap: 点の密度を可視化
remove_low_densities: 点の密度が低い頂点を除去するかどうか
low_density_threshold: 除去される点密度のしきい値
"""
mesh = meshing.reconstruct_by_poisson(
    pcd,
    display_result=True,
    display_density_colormap=True,
    remove_low_densities=True,
    low_density_threshold=0.2,
)
file_io.write_mesh(f"./data/221212_LiDs1frame/7_board/mesh_by_poisson_low-0.2_outlier-0.037.ply", mesh)

# ■ スムージング
# 手法ごとの結果は大差無い

# 平均値
# m1 = smoother.filter_smooth_simple(mesh, 10)
# display.display(m1, mesh_show_back_face=True)
# file_io.write_mesh("./smooth_simple_num10.ply", m1)

# ラプラシアン
# m2 = smoother.filter_smooth_laplacian(mesh, 10)
# display.display(m2, mesh_show_back_face=True)
# file_io.write_mesh("./smooth_laplacian_num10.ply", m2)

# Taubin法
m3 = smoother.filter_smooth_taubin(mesh, 10)
display.display(m3, mesh_show_back_face=True)
# file_io.write_mesh("./smooth_taubin_num10.ply", m3)
