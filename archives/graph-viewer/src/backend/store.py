"""TODO docs の記述
"""
from src.backend._csv import CSVReader
from src.backend.graph import Metadata
from src.common import utils
from src.common.constants import TIME_AXIS_HEADER_REGEX


class DataStore:
    def __init__(self) -> None:
        self.plots: list[Metadata] = []
        self.csv_readers: dict[str, CSVReader] = {}
        self.selected_headers: list[str] = []

    @property
    def number_of_headers(self) -> int:
        return len(self.selected_headers)

    @property
    def number_of_csv_readers(self) -> int:
        return len(self.csv_readers)

    @property
    def headers_of_csv_reader(self) -> list[str]:
        # NOTE csv ヘッダは一意である前提なので、csv_readersから1つだけ使う
        reader = self._get_csv_reader_by_index(0)
        if reader:
            return reader.columns
        return []

    @property
    def values_of_csv_time_axis(self) -> list[int | float]:
        # csv が読み込まれていない or ヘッダが選択されていない
        if not self.headers_of_csv_reader or not self.selected_headers:
            return []

        # ヘッダーの中に `time` という文字列が含まれれば次に進む
        # NOTE : 大文字/小文字を区別しないように正規表現を使用
        for header in self.headers_of_csv_reader:
            try:
                TIME_AXIS_HEADER_REGEX.findall(header)[0]
                time_axis_name = header
                break
            except IndexError:
                pass
        else:
            return []

        return self._get_csv_reader_by_index(0).get_column_values(time_axis_name)  # type: ignore : self.csv_headers で None にならないことが確定するため

    def _get_csv_reader_by_index(self, index: int) -> CSVReader | None:
        try:
            return list(self.csv_readers.values())[index]
        except IndexError:
            return None

    def _sync_plots(self) -> None:
        # plots をクリアする
        self.plots = []

        # どちらかが存在しない場合
        if not self.selected_headers or not self.csv_readers.items():
            return

        # 重複を削除する
        headers_without_duplicate_words = utils.remove_duplicates(*self.selected_headers)
        filenames = [utils.get_filename_from_path(path) for path in self.csv_readers.keys()]
        filenames_without_duplicate_words = utils.remove_duplicates(*filenames)

        for header, header_without_duplicate in zip(self.selected_headers, headers_without_duplicate_words):
            for csv_reader, filename_without_duplicate in zip(
                self.csv_readers.values(), filenames_without_duplicate_words
            ):
                data = csv_reader.get_column_values(header)
                if data is None:
                    raise ValueError(f"存在しないCSVヘッダが指定されました header: {header}")
                # インスタンス変数の値と同期させる
                self.plots.append(
                    Metadata(
                        data=data,
                        label=f"{filename_without_duplicate}_{header_without_duplicate}",
                    )
                )

    def _add_header(self, header: str) -> None:
        self.selected_headers.append(header)

    def _remove_header(self, header: str) -> None:
        self.selected_headers.remove(header)

    def _add_csv_reader(self, filepath: str) -> None:
        self.csv_readers[filepath] = CSVReader(filepath)

    def _remove_csv_reader(self, header: str) -> None:
        del self.csv_readers[header]

    def _has_header(self, header: str) -> bool:
        return header in self.selected_headers

    def _has_csv_reader(self, filepath: str) -> bool:
        return filepath in self.csv_readers.keys()

    def update_plots_by_filepaths(self, new_filepaths: list[str]) -> None:
        # NOTE: dir のパスは渡す前に除外しておくこと

        # 存在しなければクリアする
        if not new_filepaths:
            self.csv_readers = {}
            self._sync_plots()
            return

        # 変化なし
        number_of_new_filepaths = len(new_filepaths)
        if number_of_new_filepaths == self.number_of_csv_readers:
            return

        if number_of_new_filepaths > self.number_of_csv_readers:
            # 追加するパターン
            for path in new_filepaths:
                if not self._has_csv_reader(path):
                    self._add_csv_reader(path)
                    self._sync_plots()
                    return
        else:
            # 削除するパターン
            for path in self.csv_readers.keys():
                if path not in new_filepaths:
                    self._remove_csv_reader(path)
                    self._sync_plots()
                    return

    def update_plots_by_headers(self, new_headers: list[str]) -> None:
        # 存在しなければクリアする
        if not new_headers:
            self.selected_headers = []
            self._sync_plots()
            return

        # 変化なし
        number_of_new_headers = len(new_headers)
        if number_of_new_headers == self.number_of_headers:
            return

        if number_of_new_headers > self.number_of_headers:
            # 追加するパターン
            for header in new_headers:
                if not self._has_header(header):
                    self._add_header(header)
                    self._sync_plots()
                    return

        else:
            # 削除するパターン
            for header in self.selected_headers:
                if header not in new_headers:
                    self._remove_header(header)
                    self._sync_plots()
                    return
