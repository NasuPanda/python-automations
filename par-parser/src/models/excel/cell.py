from dataclasses import dataclass


@dataclass
class Cell:
    value: str | int | float
    row: int
    column: int

    @property
    def members_as_dict(self) -> dict:
        return {
            "value": self.value,
            "row": self.row,
            "column": self.column
        }
