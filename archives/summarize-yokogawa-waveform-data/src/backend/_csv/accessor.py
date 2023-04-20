import pandas as pd

from common.constants import CSV_READING_SETTING


def __get_encode(filepath):
    encs = "iso-2022-jp euc-jp shift_jis utf-8".split()
    for enc in encs:
        with open(filepath, encoding=enc) as fr:
            try:
                fr = fr.read()
            except UnicodeDecodeError:
                continue
        return enc


def read_csv_values_as_matrix(csv_path):
    """Read csv values as numpy 2d-array."""
    df = pd.read_csv(
        csv_path,
        header=CSV_READING_SETTING.ch_row,
        usecols=CSV_READING_SETTING.use_cols,
    )
    # NOTE Should remove spaces from columns.
    df.columns = df.columns.str.replace(" ", "")
    return df
