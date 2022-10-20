import pathlib
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


def resolve(filepath: str) -> str:
    return str(pathlib.Path(filepath).resolve())


excel = ExcelAccessor(
    src_filepath=resolve(TEST_FILE_PATH),
    dst_filepath=resolve(result_path(filename=get_timestamp())),
    first_active_sheet="2",
)
excel.write_cell_by_coordinate("A2", "=1!A1")
excel.add_reference(1, 1, 1, "A", "1")
excel.overwrite()
