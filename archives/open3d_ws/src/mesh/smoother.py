"""メッシュのスムージング処理"""

import open3d as o3d


def filter_smooth_laplacian(
    mesh: o3d.geometry.TriangleMesh,
    number_of_iterations=5,
    lambda_filter=0.5,
    filter_scope=o3d.geometry.FilterScope.All,
) -> o3d.geometry.TriangleMesh:
    """ラプラシアンによるスムージング処理。
    NOTE
        - http://www.open3d.org/docs/release/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.filter_smooth_laplacian
        - filter_scope: 定数。0~3。 http://www.open3d.org/docs/release/python_api/open3d.geometry.FilterScope.html

    """
    print(
        "Filter smooth laplacian.\n",
        f"Params:\n\tnum_of_iterations:{number_of_iterations}\n\tlambda_filter:{lambda_filter}",
    )
    return mesh.filter_smooth_laplacian(number_of_iterations, lambda_filter, filter_scope)


def filter_smooth_simple(
    mesh: o3d.geometry.TriangleMesh, number_of_iterations=5, filter_scope=o3d.geometry.FilterScope.All
) -> o3d.geometry.TriangleMesh:
    """近傍点の平均によるスムージング処理。
    NOTE
        - http://www.open3d.org/docs/release/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.filter_smooth_simple
        - filter_scope: 定数。0~3。 http://www.open3d.org/docs/release/python_api/open3d.geometry.FilterScope.html
    """
    print(
        "Filter smooth simple.\n",
        f"Params:\n\tnum_of_iterations:{number_of_iterations}",
    )
    return mesh.filter_smooth_simple(number_of_iterations, filter_scope)


def filter_smooth_taubin(
    mesh: o3d.geometry.TriangleMesh,
    number_of_iterations=5,
    lambda_filter=0.5,
    mu=-0.53,
    filter_scope=o3d.geometry.FilterScope.All,
) -> o3d.geometry.TriangleMesh:
    """Taubin法によるスムージング処理。
    NOTE
        - http://www.open3d.org/docs/release/python_api/open3d.geometry.TriangleMesh.html#open3d.geometry.TriangleMesh.filter_smooth_taubin
        - filter_scope: 定数。0~3。 http://www.open3d.org/docs/release/python_api/open3d.geometry.FilterScope.html
    """
    print(
        "Filter smooth Taubin.\n",
        f"Params:\n\tnum_of_iterations:{number_of_iterations}\n\tlambda_filter:{lambda_filter}\n\tmu:{mu}",
    )
    return mesh.filter_smooth_taubin(number_of_iterations, lambda_filter, mu, filter_scope)
