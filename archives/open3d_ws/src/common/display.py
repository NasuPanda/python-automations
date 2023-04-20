import open3d as o3d


def display(
    geometry,
    point_show_normal=False,
    mesh_show_wireframe=False,
    mesh_show_back_face=True,
):
    """PointCloud, Mesh等のオブジェクトを表示する
    NOTE: 表示出来るのは1つのみ

    Args:
        geometry : 表示したいオブジェクト
        point_show_normal (bool, optional): 点群に付与された法線を表示するかどうか. デフォルトは False.
        mesh_show_wireframe (bool, optional): メッシュの表示に関するオプション. デフォルトは False.
        mesh_show_back_face (bool, optional): メッシュの表示に関するオプション. デフォルトは True.
    """
    o3d.visualization.draw_geometries(
        [geometry],
        point_show_normal=point_show_normal,
        mesh_show_wireframe=mesh_show_wireframe,
        mesh_show_back_face=mesh_show_back_face,
    )


def display_inlier_outlier(pcd: o3d.geometry.PointCloud, inlier_index):
    """特定のインデックスの点群を可視化する
    NOTE: 外れ値の可視化用。外れ値を検出する関数は外れ値で無い点群のインデックスを返すため、それを渡す
    """
    inlier_pcd = pcd.select_by_index(inlier_index)
    outlier_pcd = pcd.select_by_index(inlier_index, invert=True)

    print("Showing outliers (red) and inliers (gray): ")
    outlier_pcd.paint_uniform_color([1, 0, 0])
    inlier_pcd.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([inlier_pcd, outlier_pcd])
