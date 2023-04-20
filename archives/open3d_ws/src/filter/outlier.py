"""外れ値のフィルタリング
"""


def get_statistical_inliers(pcd, nb_neighbors=20, std_ratio=2.0):
    """外れ値ではない(残す)点群のインデックスを取得"""
    _cl, inliers = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
    return inliers


def get_radius_inliers(pcd, nb_points=16, radius=0.05):
    """外れ値ではない(残す)点群のインデックスを取得"""
    _cl, inliers = pcd.remove_radius_outlier(nb_points=nb_points, radius=radius)
    return inliers


def remove_statistical_outlier(pcd, nb_neighbors=20, std_ratio=2.0):
    """pcd の外れ値を削除する"""
    inliers = get_statistical_inliers(pcd, nb_neighbors, std_ratio)
    return pcd.select_by_index(inliers)


def remove_radius_outlier(pcd, nb_points=16, radius=0.05):
    """pcd の外れ値を削除する"""
    inliers = get_radius_inliers(pcd, nb_points, radius)
    return pcd.select_by_index(inliers)


def divide_inliers_and_outliers(pcd, inliers):
    """外れ値ではない点群 と 外れ値と判定された点群に分割する"""
    return pcd.select_by_index(inliers), pcd.select_by_index(inliers, invert=True)
