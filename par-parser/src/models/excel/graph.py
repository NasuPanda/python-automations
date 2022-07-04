from dataclasses import dataclass


@dataclass
class References:
    min_column: int
    max_column: int
    min_row: int
    max_row: int

    @property
    def members_as_dict(self):
        # openpyxlのメソッドに合わせた形にしておく
        return {
            "min_col": self.min_column,
            "max_col": self.max_column,
            "min_row": self.min_row,
            "max_row": self.max_row
        }


@dataclass
class Graph:
    title: str
    x_axis_title: str
    y_axis_title: str
    width: int | float
    height: int | float
    x_references: References
    y_references: References
    address: str
    legend: None | str
