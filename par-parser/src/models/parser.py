import csv
from pathlib import Path

from src.utils.exceptions import ParParseError


class ParParser():
    """parファイルをparseする。

    Class members
    ------
    IGNORE_COLUMNS: tuple[int, ...]
        結果に含まない行。
        削除するとindexが前にずれるため, 後ろから指定する。
    SEGMENT_NUMBER: int
        対象とするsegment number。
        下の例の [Definition=Segment]行の値。

    想定形式

    - 生データは<Segment1> ~ </Segment1> 内に存在する
    - データ部分の1行目に Segment Number が記録されている

    .
    .
    <Segment1>
    Type=2
    Version=3
    Definition=Segment #, Point #, E(V), I(A), Elapsed Time(s), ADC Sync Input(V), Current Range, Status, E Applied(V), Frequency(Hz), E Real, E Imag, I Real, I Imag, Z Real, Z Imag, E2 Status, E2(V), E2 Real, E2 Imag, Z2 Real, Z2 Imag, ActionId, AC Amplitude, 0
    0,0,0.0447793,0.0005161254,620,3.967346,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,52,0
    0,1,0.06931581,0.0007224161,640,3.967651,5,5,0.025,0,0,0,0,0,0,0,0,0,0,0,0,0,52,0
    .
    .

    Raises
    ------
    ParParseError
        parseに失敗した時に発生する。
    """
    # NOTE: 削除するとindexが前にずれるため, 後ろから指定する
    IGNORE_COLUMNS = (1, 0)
    SEGMENT_NUMBER = 0

    @classmethod
    def read_par(cls, file_path: str) -> list[str]:
        """.parファイルを読み込みリストとして返す。

        Parameters
        ----------
        file_path : str
            .parファイルのパス。

        Returns
        -------
        list[str]
            読み込んだ.parファイルの中身。(リスト)
        """
        with open(file_path, "r", encoding="utf-8", newline="") as input_file:
            # 末尾の改行/空白を削除しておく
            return [i.strip('\r\n') for i in input_file.readlines()]

    @classmethod
    def __split_and_normalize(cls, string: str, delimiter=",") -> list[str]:
        """文字列を delimiter 区切りで分割, 各要素を正規化(前後の空白/改行を削除)する。

        Parameters
        ----------
        string : str
            対象となる文字列。
        delimiter : str, optional
            区切り文字, by default ","

        Returns
        -------
        list[str]
            分割, 正規化後の文字列の配列。
        """
        return [i.strip() for i in string.split(delimiter)]

    @classmethod
    def __get_row_data_start_line_index(cls, par_lines: list[str], search_string="<Segment1>") -> int:
        """row data の開始インデックスを取得する

        Parameters
        ----------
        par_lines : list[str]
            リストとして読み込んだ.parファイル。
        search_string : str, optional
            row data の開始を示す文字列, by default "<Segment1>"

        Returns
        -------
        int
            取得した開始インデックス。

        Raises
        ------
        ParParseError
            開始インデックスの取得に失敗した場合。
            search_stringの変更が必要。
        """
        for i, line in enumerate(par_lines):
            if line == search_string:
                return i

        raise ParParseError("無効な形式のparファイルが渡されました。<Segment1>が含まれていません。")

    @classmethod
    def __get_headers(cls, row_data_lines: list[str], search_string="Definition") -> tuple[int, list[str]]:
        """ヘッダー列のインデックス, リストに変換したヘッダー要素を取得する

        Parameters
        ----------
        row_data_lines : list[str]
            読み込んだファイルの内 row data 部分のリスト。
        search_string : str, optional
            ヘッダー列であることを示す文字列, by default "Definition"

        Returns
        -------
        tuple[int, list[str]]
            ヘッダー列のインデックス, [,] 区切りでリストに変換したヘッダー。

        Raises
        ------
        ParParseError
            ヘッダー列の取得に失敗した場合。
            search_stringの変更が必要。
        """
        for i, line in enumerate(row_data_lines):
            if search_string in line:
                return i, cls.__split_and_normalize(line)

        raise ParParseError("無効な形式のparファイルが渡されました。Definition=から始まる行が含まれていません。")

    @classmethod
    def __get_segment_values(cls, row_data_lines: list[str], segment_number: int) -> list[str]:
        """対象のsegmentの値を取得する。

        Parameters
        ----------
        row_data_lines : list[str]
            読み込んだファイルの内 row data 部分 のリスト。
        segment_number : int
            対象の segment number。

        Returns
        -------
        list[str]
            取得したsegmentの値。

        Raises
        ------
        ParParseError
            指定されたsegmentに値が存在しない場合。
        """
        # フラグ変数
        is_target_segment = False
        values = []

        for line in row_data_lines:
            # lineの先頭が対象のsegment_numberであればフラグをTrueに
            if line[0] == str(segment_number):
                is_target_segment = True

            if is_target_segment:
                # lineの先頭が対象のsegment_numberで無ければ終了
                if line[0] != str(segment_number):
                    break
                values.append(cls.__split_and_normalize(line))

        if not values:
            raise ParParseError("指定されたsegmentに値は存在しません。")

        return values

    @classmethod
    def __pop_ignore_column(cls, ignore_columns: tuple[int, ...], *arrays):
        """不要な行を削除する。

        - 操作が破壊的なので注意。
        - 2次元配列であれば要素の配列を対象とする。(2次元以上は考慮しない)
        - 2次元以上を考慮するなら再帰的に判定する。

        Parameters
        ----------
        ignore_columns : tuple[int, ...]
            削除する行番号 (0から)
        """
        for array in arrays:
            if isinstance(array[0], list):
                [
                    [array_1dim.pop(i) for i in ignore_columns]
                    for array_1dim in array
                ]
            else:
                [array.pop(i) for i in ignore_columns]

    @classmethod
    def parse_par_to_csv(cls, from_file_path: str | Path, to_file_path: str):
        """.parファイルをparseしてCSVを出力する。

        Parameters
        ----------
        from_file_path : str
            対象とするparファイルのパス。
        to_file_path : str
            書き込み先CSVファイルのパス。

        Raises
        ------
        ParParseError
            CSVファイルへの書き込み, 保存で問題が生じた場合。
        """
        par_lines = cls.read_par(from_file_path)

        # row data が存在する箇所のみ抜き取る
        row_data_start_line_index = cls.__get_row_data_start_line_index(par_lines)
        row_data_lines = par_lines[row_data_start_line_index:]

        # row data からヘッダー, データを取得
        header_index, headers = cls.__get_headers(row_data_lines)
        values = cls.__get_segment_values(
            # sliceは [0:] の場合 0~ になる。 index=0 なら 1~ の値が欲しいので +1 する
            row_data_lines[header_index + 1:],
            cls.SEGMENT_NUMBER
        )

        cls.__pop_ignore_column(cls.IGNORE_COLUMNS, headers, values)

        try:
            with open(to_file_path, "w", encoding='utf-8', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(values)
        except OSError:
            raise ParParseError("CSVファイルへの書き込みで問題が発生しました。\nCSVファイルを開いている, 無効なパスが指定された可能性があります。")
