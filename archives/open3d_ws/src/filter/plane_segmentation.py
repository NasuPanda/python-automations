"""セグメンテーション
"""


def get_segmented_plane_inliers(pcd, distance_threshold, ransac_n=5, num_iterations=1000):
    """平面のインデックスを取得"""
    plane_model, inliers = pcd.segment_plane(
        distance_threshold=distance_threshold, ransac_n=ransac_n, num_iterations=num_iterations
    )

    # 結果の表示
    [a, b, c, d] = plane_model
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

    return inliers


def divide_plane_and_others(pcd, distance_threshold: int, ransec_n=5, num_iterations=1000):
    """平面 / それ以外を分割する

    Args:
        pcd : 点群
        distance_threshold (int): ある点が推定平面に対して持つことが出来る最大距離。推定平面との距離がこの値より小さいものを inlier の点群とみなす。
        ransec_n (int, optional): 平面を推定するためにランダムにサンプリングする点の数
        num_iterations (int, optional): ランダム平面をサンプリングして検証する回数

    Returns:
        tuple[pcd, pcd]: 検出された平面, それ以外 の点群
    """
    inliers = get_segmented_plane_inliers(pcd, distance_threshold, ransec_n, num_iterations)
    return pcd.select_by_index(inliers), pcd.select_by_index(inliers, invert=True)
