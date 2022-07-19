from libs.log.reader import LogReader

# Get user input
# TODO GUI


# Read log
# TODO libs/log/ 配下に logger.py と reader.py を置くように変更
reader = LogReader(csv_path=r"logs\220701-220731_date_time_test.csv")
df = reader.extract_series_by_header("時刻")
print(df.head(5))
print(df.__class__)
extracted_df = reader.extract_df_by_time_series("2022-07-19")
print(extracted_df)
print(extracted_df.__class__)

# Split data by date
# TODO logs/extractor / reader に定義
# TODO I/O と データの加工 は別枠で扱うべきな気がするので、分けた方が良い気がする


# Flag to actual facility operation rate
# TODO こいつの役割 => データの加工、整形。であれば、Formatterがしっくり来るか？


# Write facility operation rate and date to excel
# TODO excel accessor を持ってくる
