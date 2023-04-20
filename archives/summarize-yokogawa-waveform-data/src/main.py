def main() -> None:
    import os
    import warnings

    from backend._csv import accessor
    from backend.excel.accessor import ExcelAccessor
    from backend.excel.types import Graph, References
    from common import utils
    from common.constants import (
        CHANNELS,
        COLUMN_ORDERS,
        CSV_READING_SETTING,
        DATA_FILE_EXTENSION,
        DATETIME_FORMAT,
        DECIMAL_PLACES_IN_TIME,
        DST_FOLDER,
        FORMAT_EXCEL_PATH,
        GRAPH_SETTINGS,
        GRAPH_VALUE_LOCATION,
        SAMPLING_RATE_VALUE_LOCATION,
        SETTING_EXCEL_LOCATIONS,
    )
    from frontend import cli
    from frontend.spinner import Spinner

    warnings.simplefilter("ignore")

    cli.print_section("設定ファイル入力")
    setting_excel_path = cli.get_filepath("設定用Excelファイルのパスを入力して下さい(ドラッグ&ドロップ可): ", ".xlsx")
    with Spinner("設定読み込み中...", "設定読み込み中...終了."):
        # Read settings.
        setting_excel = ExcelAccessor(setting_excel_path, first_active_sheet=1)
        correspondence_columns_and_channels = {}
        for ch in CHANNELS:
            column_name = setting_excel.read_cell_value_by_coordinate(SETTING_EXCEL_LOCATIONS[ch])
            if column_name is None:
                continue
            correspondence_columns_and_channels[column_name] = ch

        try:
            channel_orders = [correspondence_columns_and_channels[col] for col in COLUMN_ORDERS]
        except KeyError:
            cli.print_alerts("[Error] 設定ファイルに異常が検出されました.")
            raise ValueError("Detect Invalid Setting.")
        if len(channel_orders) != len(COLUMN_ORDERS):
            cli.print_alerts("[Error] 設定ファイルで必要なチャンネルが設定されていません.")
            raise ValueError("Detect Invalid Setting.")
        cli.print_notices("読み込んだチャンネル:", str(channel_orders))
        del setting_excel

    # Get CSV files.
    cli.print_section("フォルダ選択")
    csv_folder = cli.get_folder("ファイルが保存されたフォルダを入力して下さい(ドラッグ&ドロップ可): ", DATA_FILE_EXTENSION)
    csv_files = utils.get_files_from_folder(csv_folder, DATA_FILE_EXTENSION)
    csv_stems = utils.get_file_stems_from_folder(csv_folder, DATA_FILE_EXTENSION)
    cli.print_notices(f"読み込んだCSV: {csv_files}")

    cli.print_section("処理実行")

    with Spinner("フォーマットExcel読み込み中..."):
        output_excel = ExcelAccessor(FORMAT_EXCEL_PATH)
    cli.print_notices("フォーマットExcel読み込み終了.")

    spinner = Spinner("データの書き込み中...", "データの書き込み中...終了.")
    spinner.start()
    for csv_path, name in zip(csv_files, csv_stems):
        output_excel.copy_worksheet(name, 1, True)
        df = accessor.read_csv_values_as_matrix(csv_path)

        # Write h_resolution.
        # NOTE: sampling_rate (maybe)
        h_resolution = float(df[channel_orders[0]][CSV_READING_SETTING.h_resolution_row])
        output_excel.write_cell_by_coordinate(SAMPLING_RATE_VALUE_LOCATION, h_resolution)

        # Drop unnecessary indexes from df.
        df.drop(index=df.index[CSV_READING_SETTING.skip_indexes], inplace=True)

        # Write csv values.
        for i, ch in enumerate(channel_orders):
            output_excel.write_cell_by_index(1, i + 1, ch)
            output_excel.write_column(2, i + 1, values=df[ch].values.astype(float).tolist())

        # Calculate necessary values.
        max_row = GRAPH_VALUE_LOCATION.min_row + len(df)
        max_time_value = round(h_resolution * max_row, DECIMAL_PLACES_IN_TIME)

        # Create charts.
        primary_data_collection = [
            References(i, i, GRAPH_VALUE_LOCATION.min_row, max_row)
            for i in range(
                GRAPH_VALUE_LOCATION.primary_data_min_column,
                GRAPH_VALUE_LOCATION.primary_data_max_column + 1,
            )
        ]
        secondary_data = References(
            GRAPH_VALUE_LOCATION.secondary_data_min_column,
            GRAPH_VALUE_LOCATION.secondary_data_max_column,
            GRAPH_VALUE_LOCATION.min_row,
            max_row,
        )
        x_axis = References(
            GRAPH_VALUE_LOCATION.category_min_column,
            GRAPH_VALUE_LOCATION.category_max_column,
            GRAPH_VALUE_LOCATION.min_row + 1,
            max_row,
        )
        graph_src = Graph(
            title=name,
            x_axis_title=GRAPH_SETTINGS.x_axis_title,
            x_axis_max_value=max_time_value,
            primary_y_axis_title=GRAPH_SETTINGS.primary_y_axis_title,
            secondary_y_axis_title=GRAPH_SETTINGS.secondary_y_axis_title,
            primary_data_collection=primary_data_collection,
            secondary_data=secondary_data,
            x_axis=x_axis,
            address=GRAPH_SETTINGS.address,
            width=GRAPH_SETTINGS.width,
            height=GRAPH_SETTINGS.height,
            legend=GRAPH_SETTINGS.legend_position,
        )
        output_excel.add_scatter_chart(graph_src)
    spinner.stop()
    # Remove an unnecessary format sheet.
    output_excel.remove_worksheet(1)
    cli.print_notices("データの書き込み終了.")

    with Spinner("ファイル保存中...", "ファイル保存中...終了."):
        # Save excel.
        output_excel_path = os.path.abspath(os.path.join(DST_FOLDER, f"{utils.get_timestamp(DATETIME_FORMAT)}.xlsx"))
        output_excel.save_as(output_excel_path)

    cli.print_notices("ファイルの保存に成功しました.", f"保存先 : {output_excel_path}", "ファイルを開きます.")
    os.startfile(output_excel_path)


if __name__ == "__main__":
    main()
