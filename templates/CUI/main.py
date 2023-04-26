import os
from common import utils
from common.constants import (
    DATA_FILE_EXTENSION,
    DATETIME_FORMAT,
    SETTING_FILE_EXTENSION,
)
from cui import cui
from cui.spinner import Spinner

import time

def main() -> None:
    cui.print_section("設定ファイル入力")
    setting_excel_path = cui.get_filepath("設定用Excelファイルのパスを入力して下さい(ドラッグ&ドロップ可): ", SETTING_FILE_EXTENSION)
    with Spinner("設定読み込み中...", "設定読み込み中...終了."):
        # setting_excel = setting_parser(setting_excel_path)
        settings = ["設定1", "設定2", "設定3"]
        time.sleep(3)
    cui.print_notices("設定:", *["\t" + i for i in settings])

    cui.print_section("フォルダ選択")
    csv_folder = cui.get_folder("ファイルが保存されたフォルダを入力して下さい(ドラッグ&ドロップ可): ", DATA_FILE_EXTENSION)
    csv_files = utils.get_files_from_folder(csv_folder, DATA_FILE_EXTENSION)
    csv_stems = utils.get_file_stems_from_folder(csv_folder, DATA_FILE_EXTENSION)
    cui.print_notices("読み込んだCSV:", *[f"\t{i}.csv" for i in csv_stems])

    cui.print_section("データ書き込み")
    spinner = Spinner("データの書き込み中...", "データの書き込み中...終了.")
    spinner.start()
    time.sleep(5)
    spinner.stop()

    output_excel_path = f"{utils.get_timestamp(DATETIME_FORMAT)}.xlsx"
    cui.print_notices("ファイルの保存に成功しました.(デモのため実際には保存されていません)", f"保存先 : {output_excel_path}", "ファイルを開きます.")
    # ファイルを開く
    # os.startfile(output_excel_path)


if __name__ == "__main__":
    main()
