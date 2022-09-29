from excel.excel import ExcelAccessor


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


excel = ExcelAccessor(excel_path=TEST_FILE_PATH, first_active_sheet="1")
excel.write_row(1, 3, ["3行目からwrite_row", 1, 2, 3, 4, 5, 6, 7, 8, 9])
excel.change_active_worksheet(3)
excel.write_column(3, 1, ["3列目からwrite_column", 1, 2, 3, 4, 5, 6, 7, 8, 9])
excel.save_as(result_path(filename=get_timestamp()))
