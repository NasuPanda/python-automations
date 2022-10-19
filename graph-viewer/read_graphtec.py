from src.data.reader import CSVReader

"""
対象のデータ ※ 37行目~
CH20, , WV, TEMP, TC_K, 2000degC, Off, 2000, -200, ﾟC
測定値
番号, 日付 時間, ms, CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10, CH11, CH12, CH13, CH14, CH15, CH16, CH17, CH18, CH19, CH20, Alarm1, Alarm2, AlarmOut
NO., Time, ms, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, ﾟC, A1234567890, A1234567890, A123456789
1, 2022/9/27 9:55, 0, 137.05, 87.3, 80.55, 96.7, 93.75, 80.5,  BURNOUT,  BURNOUT,  BURNOUT,  BURNOUT, 24.7, 526.7, 512, 723.1, 605.1, 557.4,  BURNOUT,  BURNOUT,  BURNOUT,  BURNOUT, LLLLLLLLLL, LLLLLLLLLL, LLLLLLLLL
2, 2022/9/27 9:55, 0, 137.35, 87.45, 80.65, 96.9, 93.95, 80.75,  BURNOUT,  BURNOUT,  BURNOUT,  BURNOUT, 24.6, 526.7, 512.2, 723.4, 605.6, 557.7,  BURNOUT,  BURNOUT,  BURNOUT,  BURNOUT, LLLLLLLLLL, LLLLLLLLLL, LLLLLLLLL

TODOs
✓ 測定値が何行目か探し出す処理
✓ BURNOUT を欠損値(NaN)として扱う処理
    read_csvのオプションで可能
✓ 特定の行(ここでは単位)を削除する処理
★ ドメインによる分岐処理を減らす : コンポジションで作る???

References
    - [pandasでUnicodeDecodeError が出たときにやることまとめ - 私の備忘録がないわね...私の...](https://kamakuraviel.hatenablog.com/entry/2020/05/27/201155)
    - [Python Pandas 特定の文字列を指定してこれを欠損値として扱いたい。](https://teratail.com/questions/216283)
    - [pandas.DataFrameの行・列を指定して削除するdrop | note.nkmk.me](https://note.nkmk.me/python-pandas-drop/)
"""

MEASURED_VALUE_FLAG = "測定値"
NA_VALUES = [" BURNOUT"]
CSV_ENCODING = "cp932"
EXCLUDED_COLUMNS = ["番号", "日付 時間", "Alarm1", "Alarm2", "AlarmOut"]

filepath = "./graphtec.csv"

measured_value_header_row = CSVReader.find_row_by_flag(filepath, MEASURED_VALUE_FLAG)

if measured_value_header_row is None:
    exit(1)

reader = CSVReader(
    filepath,
    measured_value_header_row + 1,
    NA_VALUES,
    EXCLUDED_COLUMNS,
    CSV_ENCODING,
)
print(reader.df.head(3))
reader.drop_row_by_index(0)
print(reader.df.head(3))
