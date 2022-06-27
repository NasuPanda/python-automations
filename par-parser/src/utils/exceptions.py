"""par関連のエラー
"""
class ParException(Exception):
    """parファイルのBaseException"""
    pass


class ParParseError(ParException):
    """parファイルのparseエラー"""
    pass


"""csv関連のエラー
"""
class CSVException(Exception):
    """csvファイルのBaseException"""
    pass


class HeaderNotFoundError(CSVException):
    """headerが見つからなかった時"""
    pass


class ColumnNotFoundError(CSVException):
    """columnが見つからなかった時"""
    pass


"""バリデーションエラー
"""
class ValidationError(Exception):
    """バリデーションエラー"""
    pass


class PresenceValidationError(ValidationError):
    """存在性バリデーションエラー"""
    pass


class NumelicalityValidationError(ValidationError):
    pass


class RangeValidationError(ValidationError):
    pass


class EqualityValidationError(ValidationError):
    pass


class UniquenessValidationError(ValidationError):
    pass


class ArrayLengthValidationError(ValidationError):
    pass


class ExclusionError(ValidationError):
    pass


class NotLessThanError(ValidationError):
    pass