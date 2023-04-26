import warnings
from common.constants import CHANNELS, SETTING_EXCEL_LOCATIONS
from excel.accessor import ExcelAccessor

warnings.simplefilter("ignore")
# NOTE: 設定.xlsxの中身は以下
# シート1: 設定の中身
# シート2: 設定のマスター
SETTING_EXCEL_PATH = "./_sample_data/設定.xlsx"


def sample_read() -> None:
    setting_excel = ExcelAccessor(SETTING_EXCEL_PATH, first_active_sheet=2)

    # マスターから順番を読み取る
    column_orders = setting_excel.read_column_values(1, 1, setting_excel.max_row)

    # 設定読み取り(アクティブなウィンドウを変更→設定読み取り)
    setting_excel.change_active_worksheet(1)

    columns_and_channels = {}
    for ch in CHANNELS:
        column_name = setting_excel.read_cell_value_by_coordinate(
            SETTING_EXCEL_LOCATIONS[ch]
        )
        if column_name is None:
            continue
        columns_and_channels[column_name] = ch

    channel_orders = []
    for col in column_orders:
        try:
            channel_orders.append(columns_and_channels[col])
        except KeyError:
            # NOTE: 存在しない場合はNONEを追加
            channel_orders.append(None)

    print(columns_and_channels)

    del setting_excel


def sample_write() -> None:
    excel = ExcelAccessor("./_sample_data/output.xlsx")
    # NOTE: フォーマットを参照して書き込んでも良い
    # FORMAT_EXCEL_PATH = "./format.xlsx"
    # excel = ExcelAccessor(FORMAT_EXCEL_PATH)

    # 新しいシートを作成、アクティブなシートを変更
    excel.copy_worksheet("新しいシート", 1, change_active_sheet=True)
    # アクティブなシートを変更
    # excel.change_active_worksheet("新しいワークシート") # タイトル指定
    # excel.change_active_worksheet(2)                  # インデックス指定

    # 値の書き込み
    excel.write_cell_by_coordinate("A1", "A1")
    excel.write_cell_by_index(2, 1, "A2")
    column_values = ["B2", "B3", "B4", "B5", "B6"]
    excel.write_column(2, 2, column_values)  # 2行目スタートで2列目に書き込む(縦方向)
    row_values = ["C2", "D2", "E2"]
    excel.write_row(2, 3, row_values)  # 3行目スタートで2列目に書き込む(横方向)

    # 上書き保存
    excel.overwrite()
    # 名前をつけて保存
    # excel.save_as("./another_name.xlsx")


def main() -> None:
    print("*" * 20)
    print("サンプル: 設定読み込み")
    sample_read()
    print("*" * 20)

    print("*" * 20)
    print("サンプル: 書き込み")
    sample_write()
    print("*" * 20)


if __name__ == "__main__":
    main()
