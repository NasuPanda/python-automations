import itertools
from libs.excel.dataclasses.cell import CellDict
from libs.excel.dataclasses.column import Column, ColumnGroup
from utils.exceptions import GroupNotFoundError, InvalidRangeError


class VerticalExcel():
    def __init__(self, path: str, group_start_index_of_row: int) -> None:
        self.path = path
        self.group_start_index_of_row = group_start_index_of_row

        self.data_groups: list[ColumnGroup] = []
        self.columns: list[Column] = []

    def find_group_by(self, name: str | None = None, index: int | None = None):
        try:
            if name is not None:
                group = [group for group in self.data_groups if group.name == name][0]
            elif index is not None:
                group = self.data_groups[index]
            else:
                raise GroupNotFoundError
        except (IndexError, GroupNotFoundError) as e:
            print(e)
            print("指定されたグループが存在しません")
            raise GroupNotFoundError(f"invalid arguments name:{name}, index:{index}")

        return group

    def add_group(self, name: str, column_range: tuple[int, int]):
        self.data_groups.append(
            ColumnGroup(
                name=name,
                start_index_of_row=self.group_start_index_of_row,
                column_range=column_range
            )
        )
        self.__validate_column_rage_of_groups()

    def add_column_to_group(
        self,
        column_title: str,
        group_name: str | None = None,
        group_index: int | None = None
    ):
        group = self.find_group_by(name=group_name, index=group_index)
        group.add_column(column_title)

    def add_cell_to_column_belongs_to_group(
        self,
        value: int | float | str | None,
        group_name: str | None = None,
        group_index: int | None = None,
        column_title: str | None = None,
        column_index: int | None = None
    ):
        group = self.find_group_by(name=group_name, index=group_index)
        column = group.find_column_by(title=column_title, index=column_index)
        column.add_cell(value)

    def add_column(self, title: str, column_index: int, start_index_of_row: int):
        self.columns.append(
            Column(
                title=title,
                column_index=column_index,
                start_index_of_row=start_index_of_row
            )
        )

    def __group_last_added(self) -> ColumnGroup | None:
        if not self.__has_group:
            return

        return self.data_groups[-1]

    def __validate_column_rage_of_groups(self):
        ranges = []
        for group in self.data_groups:
            # ex: column_range=(1, 5)
            # from=1, to=5
            _from, to = group.column_range
            # range(from, to)=(1,2,3,4,5)
            [ranges.append(i) for i in range(_from, to)]

        # 重複する範囲が含まれていた場合
        if len(set(ranges)) != len(ranges):
            raise InvalidRangeError("列の範囲が重複しています:", ranges)

    def __has_group(self):
        return bool(self.data_groups)

    @property
    def all_cells(self) -> list[CellDict]:
        """すべてのセル。
        """
        all_cells_belongs_to_group = [group.all_cells for group in self.data_groups]
        data_cells_belongs_to_column = [column.data_cells for column in self.columns]
        title_cells_belongs_to_column = [column.title_cell_member_dict for column in self.columns]

        all_cells_belongs_to_group.append(data_cells_belongs_to_column)  # type: ignore
        all_cells_belongs_to_group.append(title_cells_belongs_to_column)

        return list(itertools.chain.from_iterable(all_cells_belongs_to_group))
