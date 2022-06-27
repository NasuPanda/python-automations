import numpy as np
from scipy import stats


def calc_slope(x: list[int | float], y: list[int | float]) -> int | float:
    """既知のxとyのデータ範囲を元に回帰直線の傾きを求める。

    - ExcelのSlope関数と似た動作をする。
    - scipyを使用。

    Parameters
    ----------
    x : list[int  |  float]
        既知のxの配列。
    y : list[int  |  float]
        既知のyの配列。

    Returns
    -------
    int | float
        算出された回帰直線の傾き。
    """
    slope, __, __, __, __ = stats.linregress(x, y)
    return slope


def find_closest_value_index(array: list, searched_value: int | float) -> int:
    """配列から対象の値と最も近い値のindexを返す。

    Parameters
    ----------
    array : list
        検索する配列。
    searched_value : int | float
        検索対象の値。

    Returns
    -------
    int | float
        最も近い値。
    """
    # 配列と対象値の差分を計算し最小値のインデックスを取得
    closest_index = np.abs(np.asarray(array) - searched_value).argmin()
    return closest_index
