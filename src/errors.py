class LabelNotFoundError(Exception):
    """ラベルが見つからないとき"""


class GroupIdNotNumberError(Exception):
    """GroupIDに数字以外が指定されたとき"""


class LabelNotNumberError(Exception):
    """ラベルに数字以外が指定されたとき"""


class NumberOfLabelMissMatchError(Exception):
    """コンテンツ数 ≠ グループ数×ラベル数のとき"""


class SortBasePartNotNumberError(Exception):
    """ソートの基準となる部分に数字以外が指定されたとき"""
