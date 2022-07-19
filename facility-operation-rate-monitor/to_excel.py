from libs.log.reader import LogReader
from libs.log.analyzer import LogAnalyzer


# Get user input
# TODO GUI


# Read log
reader = LogReader(csv_path=r"logs\220701-220731_date_time_test.csv")
extracted_df = reader.extract_df_by_time_series("2022-07-17")
print(extracted_df)
print(extracted_df.__class__)

# Flag to actual facility operation rate
analyzer = LogAnalyzer(extracted_df)
analyzer.perform()
print(analyzer.man_hour_min, analyzer.machine_time_min)

# Write facility operation rate and date to excel
# TODO excel accessor を持ってくる
