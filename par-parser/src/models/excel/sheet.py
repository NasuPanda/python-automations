from dataclasses import dataclass

from src.models.excel.cell import Cell


@dataclass
class Sheet:
    title: str
    cells: list[Cell]

    def add_cell(self, cell: Cell):
        self.cells.append(cell)

    def get_cells_as_dict(self):
        return [cell.members_as_dict for cell in self.cells]
