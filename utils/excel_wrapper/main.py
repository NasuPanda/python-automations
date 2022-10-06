from excel.accessor import ExcelAccessor


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


excel = ExcelAccessor(excel_path=TEST_FILE_PATH, first_active_sheet="3")
print(excel.read_current_sheet("row"))
print(excel.read_current_sheet("column"))
print(excel.read_all_sheets("row"))
print(excel.wb, excel.excel_path, excel.is_xlsm, excel.current_sheet_title)
excel.to_xlsm_if_xlsx()
print(excel.wb, excel.excel_path, excel.is_xlsm, excel.current_sheet_title)
excel.save_as(result_path(filename=get_timestamp()))
