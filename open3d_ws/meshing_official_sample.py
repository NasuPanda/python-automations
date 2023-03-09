from src.common import converter, display, file_io, getter, rgb
from src.filter import crop, distance, down_sample, outlier, plane_segmentation, rgb_filter
from src.mesh import meshing, normal, smoother

path_bunny = "./data/samples/bunny.ply"
path_cube = "./data/samples/cube.ply"
path_dragon = "./data/samples/dragon.ply"
path_sphere = "./data/samples/sphere.ply"
path_vase = "./data/samples/vase.ply"

# 1. 点群を読み込んで表示
pcd = file_io.read_point_cloud(path_cube)
display.display(pcd)

# 2. 前処理
# 綺麗な点群なので前処理は不要

# 3. 法線ベクトル付与
normal.estimate_normals(pcd)
normal.orient_normals_tangent_place(pcd)
# point_show_normal オプションを付けると法線が可視化される
display.display(pcd, point_show_normal=True)

# 4. メッシュ化
# display_result=True とすると結果表示
# ■ Alpha Shapes
for alpha in [0.02, 0.05, 0.1]:
    mesh = meshing.reconstruct_by_alpha_shapes(pcd, display_result=True, alpha=alpha)

# ■ Ball Pivoting
# パラメータを自分で設定したい場合は以下のような ball_radiuses を用意
# average_distance = getter.compute_nearest_neighbor_distance_avg(pcd_with_normals)
# radius = 2 * average_distance
# ball_radiuses = [radius, radius * 2]
mesh = meshing.reconstruct_by_ball_pivoting(pcd, display_result=True)

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
    low_density_threshold=0.01,  # 綺麗な点群の場合小さめの値にしておく
)

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
# m3 = smoother.filter_smooth_taubin(mesh, 10)
# display.display(m3, mesh_show_back_face=True)
# file_io.write_mesh("./smooth_taubin_num10.ply", m3)
