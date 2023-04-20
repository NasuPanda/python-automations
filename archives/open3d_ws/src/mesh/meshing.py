"""点群メッシュ化

参考
    - http://www.open3d.org/docs/latest/tutorial/Advanced/surface_reconstruction.html
    - https://orbi.uliege.be/bitstream/2268/254933/1/TDS_generate_3D_meshes_with_python.pdf
"""

import numpy as np
import open3d as o3d
from matplotlib import pyplot as plt

from src.common import converter, display, getter


def __print_start(method) -> None:
    print(f"[Start] {method}")


def __print_finish(method) -> None:
    print(f"[Finish] {method}")


def reconstruct_by_alpha_shapes(
    pcd: o3d.geometry.PointCloud, alpha=0.1, display_result=False
) -> o3d.geometry.TriangleMesh:
    """Alpha Shapes による点群メッシュ化

    Args:
        pcd (o3d.geometry.PointCloud): 点群データ
        alpha (float, optional): α値。大きいほど粗いメッシュになる. デフォルトは 0.1.
        display_result (bool, optional): 結果を表示するかどうか. デフォルトは False.

    Returns:
        o3d.geometry.TriangleMesh: 生成されたメッシュ
    """
    __print_start("alpha_shape")

    print("Creating tetra mesh...")
    tetra_mesh, pt_map = o3d.geometry.TetraMesh.create_from_point_cloud(pcd)

    print(f"Creating triangle mesh...\n\tAlpha: {alpha: {alpha:.3f}}")
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha, tetra_mesh, pt_map)
    mesh.compute_vertex_normals()

    print(f"[Result] mesh: {tetra_mesh}")
    if display_result:
        o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)
    __print_finish("alpha")
    return mesh


def reconstruct_by_ball_pivoting(
    pcd_with_normals: o3d.geometry.PointCloud,
    ball_radiuses=None,
    display_result=False,
) -> o3d.geometry.TriangleMesh:
    """Ball Pivoting による点群メッシュ化

    Args:
        pcd_with_normals (o3d.geometry.PointCloud): 法線を持った点群データ
        ball_radiuses (list[float], optional):
            アルゴリズムのパラメータ。転がす球の大きさ。
            None の場合はデフォルト値を設定して実行する。 デフォルトは None.
        display_result (bool, optional): 結果を表示するかどうか デフォルトは False.

    Returns:
        o3d.geometry.TriangleMesh: 生成されたメッシュ
    """
    __print_start("Ball Pivoting")

    # パラメータがNoneの場合はデフォルト値をセット
    if ball_radiuses is None:
        average_distance = getter.compute_nearest_neighbor_distance_avg(pcd_with_normals)
        radius = 2 * average_distance
        ball_radiuses = [radius, radius * 2]

    print(f"Creating triangle mesh...\n\tBall radius: {ball_radiuses}")

    # 第2引数 radii: メッシュ再構成に使うボールの半径
    reconstructed_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd_with_normals, o3d.utility.DoubleVector(ball_radiuses)
    )

    print(f"[Result] mesh:{reconstructed_mesh}")
    if display_result:
        o3d.visualization.draw_geometries([reconstructed_mesh], mesh_show_back_face=True)
    __print_finish("Ball Pivoting")
    return reconstructed_mesh


def __display_density_colormap(mesh, densities):
    """点密度を可視化(黄色が密度高)"""
    densities = converter.o3d2ndarray(densities)
    density_colors = plt.get_cmap("plasma")(
        (densities - densities.min()) / (densities.max() - densities.min())
    )
    density_colors = density_colors[:, :3]
    density_mesh = o3d.geometry.TriangleMesh()
    density_mesh.vertices = mesh.vertices
    density_mesh.triangles = mesh.triangles
    density_mesh.triangle_normals = mesh.triangle_normals
    density_mesh.vertex_colors = converter.ndarray2o3d(density_colors)
    display.display(density_mesh)


def reconstruct_by_poisson(
    pcd_with_normals: o3d.geometry.PointCloud,
    depth=9,
    scale=1.1,
    linear_fit=False,
    remove_low_densities=True,
    low_density_threshold=0.01,
    display_density_colormap=False,
    display_result=False,
) -> o3d.geometry.TriangleMesh:
    """Poisson法による点群メッシュ化
    references:
        - http://www.open3d.org/docs/latest/python_api/open3d.geometry.TriangleMesh.html?highlight=poisson#open3d.geometry.TriangleMesh.create_from_point_cloud_poisson
        - http://www.open3d.org/docs/latest/tutorial/Advanced/surface_reconstruction.html#Poisson-surface-reconstruction

    Args:
        pcd_with_normals (o3d.geometry.PointCloud): 法線を持った点群データ
        depth (int, optional): アルゴリズムの引数. デフォルトは 9.
        scale (float, optional): アルゴリズムの引数. デフォルトは 1.1.
        linear_fit (bool, optional): アルゴリズムの引数. デフォルトは False.
        remove_low_densities (bool, optional): 構成する点の密度が低い頂点・三角形を除去するかどうか. デフォルトは True.
        low_density_threshold (float, optional): 点の密度によるフィルタリングをかける場合、その時使うしきい値. デフォルトは 0.01.
        display_density_colormap (bool, optional): 構成する点の密度を表示するかどうか. デフォルトは False.
        display_result (bool, optional): 結果を表示するかどうか. デフォルトは False.

    Returns:
        o3d.geometry.TriangleMesh: 生成されたメッシュ
    """
    __print_start("Poisson")

    print(
        f"Creating triangle mesh...\n\tdepth: {depth}\n\tscale: {scale}\n\tlinear_fit: {linear_fit}\n\tremove_low_densities: {remove_low_densities}\n\tlow_density_threshold: {low_density_threshold}"
    )
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        (mesh, densities) = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd_with_normals, depth=depth, scale=scale, linear_fit=linear_fit
        )
    print(f"[Result] mesh: {mesh}")

    # 点群密度のカラーマップを表示する
    if display_density_colormap:
        __display_density_colormap(mesh, densities)

    # 点群密度の低い頂点・三角形を削除する
    if remove_low_densities:
        vertices_to_remove = densities < np.quantile(densities, low_density_threshold)
        mesh.remove_vertices_by_mask(vertices_to_remove)

    if display_result:
        display.display(mesh, mesh_show_back_face=True)

    __print_finish("Poisson")
    return mesh
