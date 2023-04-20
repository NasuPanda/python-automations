"""ダウンサンプリング"""

import argparse
from dataclasses import dataclass

import open3d as o3d


def random_down_sample(pcd: o3d.geometry.PointCloud, sampling_ratio=0.5) -> o3d.geometry.PointCloud:
    """ランダムダウンサンプリング。点群からランダムにインデックスをサンプリングする。

    Args:
        pcd (o3d.geometry.PointCloud): o3d の PointCloud 型
        sampling_ratio (float, optional): サンプリング比率。0.5なら半分になる。

    Returns:
        o3d.geometry.PointCloud: ダウンサンプリング後の PointCloud
    """
    return pcd.random_down_sample(sampling_ratio)


def uniform_down_sample(pcd: o3d.geometry.PointCloud, every_k_points=5) -> o3d.geometry.PointCloud:
    """uniform (均一な) ダウンサンプリング。k 点ごとに 1点を選択する。

    Args:
        pcd (o3d.geometry.PointCloud): o3d の PointCloud 型
        every_k_points (int, optional): [0, k, 2k, ...]のインデックスの点が残る。デフォルトは 5

    Returns:
        o3d.geometry.PointCloud: ダウンサンプリング後の PointCloud
    """
    return pcd.uniform_down_sample(every_k_points)


def voxel_down_sample(opne3d_cloud: o3d.geometry.PointCloud, voxel_size=0.1) -> o3d.geometry.PointCloud:
    """ボクセルダウンサンプリング。
    空間を一辺の長さ a[m] の立方体に分割し、それぞれの立方体の中で代表点(重心)を求めることで点群を削減する。

    Args:
        opne3d_cloud (o3d.geometry.PointCloud): o3d の PointCloud 型
        voxel_size (float, optional): ボクセルサイズ。デフォルトは 0.1.

    Returns:
        o3d.geometry.PointCloud: ダウンサンプリング後の PointCloud
    """
    return opne3d_cloud.voxel_down_sample(voxel_size)


"""
コマンドライン引数の設定
"""
# ダウンサンプリング手法
@dataclass
class MethodsName:
    RANDOM = "random"
    UNIFORM = "uniform"
    VOXEL = "voxel"


# 各手法のデフォルト値
__DEFAULT_VALUES = {
    MethodsName.RANDOM: 0.5,
    MethodsName.UNIFORM: 5,
    MethodsName.VOXEL: 0.1,
}

# コマンドライン引数のヘルプ
DESC_MESSAGES = {
    "prog": """o3dにより点群のダウンサンプリングを行う
参考: http://www.o3d.org/docs/release/python_api/o3d.geometry.PointCloud.html?highlight=downsample    
""",
    "method": """ダウンサンプリングに使う手法
    random: ランダムダウンサンプリング。点群からランダムにインデックスをサンプリングする。毎回異なる点が選択されるので、機械学習に用いるデータの補強に有用。
    uniform: 均一なダウンサンプリング。k 点ごとに 1点を選択する。
    voxel: ボクセルダウンサンプリング。
""",
    "value": """ダウンサンプリング時に使う値
    random: サンプリング比率。 例: 0.5 なら半分
    uniform: k点ごとに1点を選択する。[0, k, 2k, ...]のインデックスの点が残る。
    voxel: ボクセルサイズ。
""",
}

parser = argparse.ArgumentParser(
    description=DESC_MESSAGES["prog"],
    formatter_class=argparse.RawTextHelpFormatter,
)


def set_cl_args():
    """ダウンサンプリングに関連するコマンドライン引数を設定する"""
    parser.add_argument(
        "--method",
        "-m",
        help=DESC_MESSAGES["method"],
        default="voxel",
        choices=[MethodsName.RANDOM, MethodsName.UNIFORM, MethodsName.VOXEL],
    )
    parser.add_argument("--value", "-v", help=DESC_MESSAGES["value"], type=float)


def get_cl_args():
    """ダウンサンプリングに関連するコマンドライン引数を取得する"""
    args = parser.parse_args()
    method, value = args.method, args.value

    if method == MethodsName.RANDOM:
        if value is None:
            value = __DEFAULT_VALUES[MethodsName.RANDOM]
        # random の許容値は 0 ~ 1
        # http://www.o3d.org/docs/release/python_api/o3d.geometry.PointCloud.html?highlight=downsample#o3d.geometry.PointCloud.random_down_sample
        else:
            if not 0 <= value <= 1:
                raise ValueError("random の場合値は 0 ~ 1 に設定してください")
    elif method == MethodsName.UNIFORM:
        if value is None:
            value = __DEFAULT_VALUES[MethodsName.UNIFORM]
    elif method == MethodsName.VOXEL:
        if value is None:
            value = __DEFAULT_VALUES[MethodsName.VOXEL]
    else:
        print("invalid method.")
        raise ValueError("指定されたメソッドは無効です")

    return method, value
