from typing import Optional

#
# 変数
#
number: int = 1
text: str = "hello"

fruits: list[str] = ["apple", "banana", "lemon"]
address: dict[str, str] = {
    "user1": "xxx県 xxx市 xxx町",
    "user2": "zzz県 zzz市 zzz町",
}

value: int
names: list[str] = []
# ︙
value = 1
names.append("name")

#
# 関数
#
def hello(name: str) -> None:
    print(f"Hello, {name}!")


def multiple(number: int) -> int:
    return number * 2


#
# クラス
#
class Cell:
    """疑似Excelセル"""

    def __init__(self, location: str, value: str | int) -> None:
        self.location = location
        self.value = value


class Sheet:
    """疑似Excelシート"""

    def __init__(self, title: str) -> None:
        self.title = title
        self.cells: list[Cell] = []

    def read_cell(self, index: int) -> str | int:
        cell = self.cells[index]
        return cell.value


# Union / Optional
# OR条件
year: int | str

# オプショナル
age: Optional[int]
