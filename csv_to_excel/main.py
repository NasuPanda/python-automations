from libs.excel.accessor import ExcelAccessor
from libs._csv.reader import CSVReader

TEST_FILE_PATH = "./tests/test.xlsx"
RESULT_FOLDER_PATH = "./tests/log"


def get_timestamp() -> str:
    import datetime

    t_delta = datetime.timedelta(hours=9)
    jst = datetime.timezone(t_delta, "JST")
    now = datetime.datetime.now(jst)
    return now.strftime("%Y%m%d%H%M%S")


def result_path(filename: str) -> str:
    return f"{RESULT_FOLDER_PATH}/{filename}.xlsx"


# test excel
# excel = ExcelAccessor(excel_path=TEST_FILE_PATH, first_active_sheet="1")
# print(excel.read_row_values(3, 1, 5))
# print(excel.read_row_values(3, "A", "E"))
# print(excel.read_column_values(3, 1, 5))
# print(excel.read_column_values("C", 1, 5))
# excel.save_as(result_path(filename=get_timestamp()))

reader = CSVReader("./tests/test.csv")
print(reader.columns)
print(reader.exists_column("header1"))
print(reader.exists_column("header11"))
print(reader.get_column_values("header1"))
print(reader.get_column_values("header6"))
