from abc import ABC, abstractmethod
from dataclasses import dataclass


class CellAddress(ABC):
    """セルアドレスの抽象基底クラス。
    """
    @property
    @abstractmethod
    def get_address(self):
        """アドレスを取得。
        """
        pass


@dataclass
class IndexCellAddress(CellAddress):
    """数値アドレス。CellAddressを継承。

    row: 列方向のインデックス。1以降の値。
    column: 行方向のインデックス。1以降の値。
    """
    row: int | tuple[int, int]
    column: int | tuple[int, int]

    @property
    def get_address(self) -> tuple[int | tuple[int, int], int | tuple[int, int]]:
        return self.row, self.column


@dataclass
class StringCellAddress(CellAddress):
    """文字列指定のアドレス。CellAddressを継承。

    address: アドレス。ex: A1, B2
    """
    address: str

    @property
    def get_address(self):
        return self.address
