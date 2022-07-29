import os
import pathlib

import PySimpleGUI as sg

from libs.log.reader import LogReader
from libs.log.analyzer import LogAnalyzer
from libs.excel.excel import VerticalExcel
from libs.excel.accessor import ExcelAccessor
from libs import timehelper


def iter_range(first_range: tuple[int, int] = (1, 3), space: int = 1):
    """Range generator.

    Parameters
    ----------
    first_range : tuple[int, int], optional
        First range, by default (1, 3)
    space : int, optional
        Space between ranges, by default 1

    Yields
    ------
    tuple[int, int]
        Generated range.
    """
    start = first_range[0]
    end = first_range[1]
    between = end - start
    while True:
        yield start, end
        start = end + space + 1
        end = start + between


def split_path_into_timestamp_and_name(path: str, sep: str = "_") -> tuple[str, str, str]:
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
    splits = path_name.split(sep)
    timestamp, facility_name = splits[0], sep.join(splits[1:])
    from_timestamp, to_timestamp = timestamp.split("-")
    return from_timestamp, to_timestamp, facility_name


def classify_and_split_paths_into_timestamp_and_name(paths: list[str]) -> dict[str, list[tuple[str, str, str]]]:
    """Classify and split paths into timestamp and filename.

    Parameters
    ----------
    paths : list[str]
        Paths.

    Returns
    -------
    dict[str, list[tuple[str, str, str]]]
        filename: {from timestamp, to timestamp, filepath}
    """
    result = {}
    for path in paths:
        from_timestamp, to_timestamp, facility_name = split_path_into_timestamp_and_name(path)
        # If facility_name key doesn't exist, initialize an array
        if not result.get(facility_name):
            result[facility_name] = []
        result[facility_name].append((from_timestamp, to_timestamp, path))

    [i.sort for i in result.values()]
    return result


def format_timestamp(timestamp: int) -> str:
    """Format timestamp for df.

    Parameters
    ----------
    timestamp : int
        The timestamp.
        ex: 220730

    Returns
    -------
    str
        Formatter timestamp.
    """
    ts_as_str = str(timestamp)

    year = "20" + ts_as_str[:2]
    month = ts_as_str[2:4]
    day = ts_as_str[4:6]
    return f"{year}-{month}-{day}"


def write_excel(
    excel_path: str,
    csv_folder: str | None,
    csv_paths: list[str],
):
    excel = VerticalExcel(excel_path, group_start_index_of_row=1)
    range_generator = iter_range((1, 3), 1)
    oldest_timestamp: int = 10000000
    most_recent_timestamp: int = -1

    # Set csv paths
    if csv_folder:
        p = pathlib.Path(csv_folder)
        csv_paths = list(map(str, p.glob("*.csv")))
    if not csv_paths:
        sg.popup_error("CSVが存在しません")
        raise ValueError("CSV doesn't exist")

    # Classify and split paths
    file_info_dict = classify_and_split_paths_into_timestamp_and_name(csv_paths)

    for facility_name, timestamps_and_paths in file_info_dict.items():
        # Initializes the group and columns belongs to group in excel
        if not excel.find_group_by(name=facility_name):
            column_range = range_generator.__next__()
            excel.add_group(facility_name, column_range)
            excel.add_column_to_group("日付", group_name=facility_name)
            excel.add_column_to_group("実作業時間", group_name=facility_name)
            excel.add_column_to_group("マシンタイム", group_name=facility_name)

        for from_timestamp, to_timestamp, path in timestamps_and_paths:
            # Read log as df
            reader = LogReader(csv_path=path)
            # Update timestamp if needed
            if int(from_timestamp) < oldest_timestamp:
                oldest_timestamp = int(from_timestamp)
            if int(to_timestamp) < most_recent_timestamp:
                most_recent_timestamp = int(to_timestamp)

            # Perform each timestamp, set data to excel.
            for timestamp in range(int(from_timestamp), int(to_timestamp) + 1):
                formatted_timestamp = format_timestamp(timestamp)

                extracted_df = reader.extract_df_by_time_series(formatted_timestamp)
                if extracted_df is None:
                    continue

                man_hour_min, machine_time_min = LogAnalyzer.perform(extracted_df)

                excel.add_cell_to_column_belongs_to_group(
                    value=formatted_timestamp, group_name=facility_name, column_title="日付"
                )
                excel.add_cell_to_column_belongs_to_group(
                    value=man_hour_min, group_name=facility_name, column_title="実作業時間"
                )
                excel.add_cell_to_column_belongs_to_group(
                    value=machine_time_min, group_name=facility_name, column_title="マシンタイム"
                )

    # Write excel
    writer = ExcelAccessor(excel.path)
    [writer.write_cell(**cell) for cell in excel.all_cells]
    writer.overwrite()


def main():
    window = sg.Window(
        "ログ => Excel",
        layout=[
            [
                sg.Input(key="-SRC-", enable_events=True),
                sg.FilesBrowse("複数ファイル選択", key="-SRC_FILES-", target="-SRC-", file_types=[("CSV", "*.csv", )]),
                sg.FolderBrowse("フォルダ選択", key="-SRC_FOLDER-", target="-SRC-"),
            ],
            [sg.Text("", size=(5, 1)), sg.Text("複数ファイル選択 / フォルダ選択が利用可能です\n※ 後で入力した方が優先されます")],
            [sg.Text("")],
            [sg.Text("Excelファイル名"), sg.Input(key="-DIST_EXCEL-"), sg.Text(".xlsx")],
            [sg.Text("", size=(5, 1)), sg.Text("※ 入力しなかった場合は自動的に「YYMMDD_設備稼働率ログ解析.xlsx」となります")],
            [sg.Text("")],
            [sg.Checkbox("生成したファイルを開く", default=True, key="-OPEN_FILE-")],
            [sg.Submit("実行", key="-SUBMIT-")]
        ]
    )

    excel_path = ""
    csv_folder = ""
    csv_paths = []

    while True:
        event, values = window.read()

        if event is None:
            break

        if event == "-SRC-":
            # Files
            if ";" in values["-SRC-"]:
                csv_folder = ""
                csv_paths = values["-SRC-"].split(";")
            # Folder
            else:
                csv_paths = []
                csv_folder = values["-SRC-"]

        if event == "-SUBMIT-":
            if not csv_paths and not csv_folder:
                sg.popup_error("CSVが入力されていません")

            else:
                # Set excel path
                if values["-DIST_EXCEL-"]:
                    excel_path = f"../解析結果出力先/{values['-DIST_EXCEL-']}.xlsx"
                else:
                    excel_path = f"../解析結果出力先/{timehelper.format(timehelper.current())}_設備稼働率ログ解析.xlsx"

                try:
                    write_excel(excel_path=excel_path, csv_folder=csv_folder, csv_paths=csv_paths)
                    sg.popup("処理に成功しました")
                    if values["-OPEN_FILE-"]:
                        os.startfile(excel_path)
                except Exception as e:
                    sg.popup_error(
                        "何らかのエラーが発生しました",
                        "解決方法が不明な場合、下のメッセージとともに開発者へ連絡して下さい",
                        str(e)
                    )


if __name__ == "__main__":
    main()
