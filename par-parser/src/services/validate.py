from src.utils.exceptions import (
    ArrayLengthValidationError,
    ExclusionError,
    NotLessThanError,
    RangeValidationError,
    PresenceValidationError,
    NumelicalityValidationError,
    UniquenessValidationError
)


class Validator:
    messages = {
        "presence": "が入力されていません !",
        "uniqueness": "がユニークではありません !",
        "numericality": "は数字ではありません",
        "within_range": "の範囲内にしてください !",
        "exclusion": "が含まれています !"
    }

    @classmethod
    def validate_presence(cls, object, object_name: str):
        if not object:
            raise PresenceValidationError(object_name + cls.messages["presence"])

    @classmethod
    def validate_numericality(cls, number: int):
        # 数値かどうか判定
        try:
            int(number)
        except TypeError:
            raise NumelicalityValidationError(str(number) + cls.messages["numericality"])

    @classmethod
    def validate_numericality_and_within_range(cls, number: float, min=1.0, max=10.0):
        # 数値かどうか判定
        try:
            float(number)
        except TypeError:
            raise NumelicalityValidationError(str(number) + cls.messages["numericality"])

        # 範囲内かどうか判定
        if not min <= float(number) <= max:
            raise RangeValidationError(f"{min} ~ {max}{cls.messages['within_range']}")

    @classmethod
    def validate_array_length_equality(cls, *arrays: list):
        array_lengths = [len(array) for array in arrays]
        # 長さの異なる配列が含まれていた場合
        if len(set(array_lengths)) != 1:
            raise ArrayLengthValidationError("配列の長さが異なっています")

    @classmethod
    def validate_exclusion(cls, exclusion, target_name, *targets):
        for i in targets:
            if i == exclusion:
                raise ExclusionError(target_name + cls.messages["exclusion"])

    @classmethod
    def validate_less_than(cls, less, more):
        if less > more:
            raise NotLessThanError(f"{less}は{more}以下の値にして下さい")

    @classmethod
    def validate_array_uniqueness(cls, array, array_name: str):
        if len(array) != len(set(array)):
            raise UniquenessValidationError(array_name + cls.messages["uniqueness"])

    @staticmethod
    def __all_the_same(array):
        return array[1:] == array[:-1]
