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


try:
    raise GroupIdNotNumberError("グループIDが数字ではありません。")
except Exception as e:
    print(e)
    print(type(str(e)))

# NOTE: 引数として渡された文字列を発生したエラーから取り出すことが出来る(Exception as eで)
