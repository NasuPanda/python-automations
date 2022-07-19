import pathlib
from libs.log.reader import LogReader
from libs.log.analyzer import LogAnalyzer
from libs.excel.excel import VerticalExcel
from libs.excel.accessor import ExcelAccessor


def iter_range(first_range: tuple[int, int] = (1, 3), space: int = 1):
    start = first_range[0]
    end = first_range[1]
    between = end - start
    while True:
        yield start, end
        start = end + space + 1
        end = start + between


def extract_facility_name_from_path(path: str, sep: str = "_") -> str:
    """Extract facility name from filepath.

    Parameters
    ----------
    path : str
        The file path.
    sep : str, optional
        The delimiter, by default "_"

    Returns
    -------
    str
        Extracted facility name.
        If underscore doesn't exist, returns path.stem as it as.
    """
    path_name = pathlib.Path(path).stem
    try:
        # Remove before the first `_`
        facility_names = path_name.split(sep)[1:]
    # If underscore doesn't exist, returns path.stem as it as.
    except IndexError:
        return path_name
    return sep.join(facility_names)


# Get user input
# TODO GUI


# Get date range
# TODO timehelperにfrom~toのdateを返すメソッドを実装する


# Read log
reader = LogReader(csv_path=r"logs\220701-220731_date_time_test.csv")
extracted_df = reader.extract_df_by_time_series("2022-07-17")

# Flag to actual facility operation rate
analyzer = LogAnalyzer(extracted_df)
analyzer.perform()

# Write facility operation rate and date to excel
excel_path = "./test.xlsx"
facility_name = extract_facility_name_from_path(r"logs\220701-220731_date_time_test.csv")

excel = VerticalExcel(excel_path, group_start_index_of_row=1)
range_generator = iter_range((1, 3), 1)

for column_range, i in zip(range_generator, range(2)):
    group_name = facility_name + str(i)
    excel.add_group(group_name, column_range)
    excel.add_column_to_group("日付", group_name=group_name)
    excel.add_column_to_group("実作業時間", group_name=group_name)
    excel.add_column_to_group("マシンタイム", group_name=group_name)

    excel.add_cell_to_column_belongs_to_group(
        value="2022-07-17", group_name=group_name, column_title="日付"
    )
    excel.add_cell_to_column_belongs_to_group(
        value=analyzer.man_hour_min, group_name=group_name, column_title="実作業時間"
    )
    excel.add_cell_to_column_belongs_to_group(
        value=analyzer.machine_time_min, group_name=group_name, column_title="マシンタイム"
    )

writer = ExcelAccessor(excel.path)
for cell in excel.all_cells:
    writer.write_cell(**cell)
writer.overwrite()