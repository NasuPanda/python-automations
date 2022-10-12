from src.common import utils
from src.data.graph.metadata import Metadata
from src.data.reader import CSVReader


# TODO名前変更
class DataStore:
    def __init__(self) -> None:
        self.plots: list[Metadata] = []
        self.csv_readers: dict[str, CSVReader] = {}
        self.headers: list[str] = []

    @property
    def number_of_headers(self) -> int:
        return len(self.headers)

    @property
    def number_of_csv_readers(self) -> int:
        return len(self.csv_readers)

    def _sync_plots(self) -> None:
        if not self.headers or not self.csv_readers.items():
            return

        # plots をクリアする
        self.plots = []

        # 重複を削除する
        headers_without_duplicate_words = utils.remove_duplicates(*self.headers)
        filenames = [utils.get_filename_from_path(path) for path in self.csv_readers.keys()]
        filenames_without_duplicate_words = utils.remove_duplicates(*filenames)

        for header, header_without_duplicate in zip(self.headers, headers_without_duplicate_words):
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
        self.headers.append(header)

        self._sync_plots()

    def _remove_header(self, header: str) -> None:
        self.headers.remove(header)

        self._sync_plots()

    def _add_csv_reader(self, filepath: str) -> None:
        self.csv_readers[filepath] = CSVReader(filepath)

        self._sync_plots()

    def _remove_csv_reader(self, header: str) -> None:
        del self.csv_readers[header]

        self._sync_plots()

    def _has_header(self, header: str) -> bool:
        return header in self.headers

    def _has_csv_reader(self, filepath: str) -> bool:
        return filepath in self.csv_readers.keys()

    def update_plots_by_filepaths(self, new_filepaths: list[str]) -> None:
        # NOTE: dir のパスは渡す前に除外しておくこと

        # 存在しなければクリアする
        if not new_filepaths:
            self.csv_readers = {}

        number_of_files = len(new_filepaths)
        if number_of_files == self.number_of_csv_readers:
            return

        if number_of_files > self.number_of_csv_readers:
            # 追加するパターン
            for path in new_filepaths:
                if not self._has_csv_reader(path):
                    self._add_csv_reader(path)
                    return
        else:
            # 削除するパターン
            for path in self.csv_readers.keys():
                if path not in new_filepaths:
                    self._remove_csv_reader(path)
                    return

    def update_plots_by_headers(self, new_headers: list[str]) -> None:
        if not new_headers:
            self.headers = []

        number_of_headers = len(new_headers)

        if number_of_headers == self.number_of_headers:
            return

        if number_of_headers > self.number_of_headers:
            # 追加するパターン
            for header in new_headers:
                if not self._has_header(header):
                    self._add_header(header)
                    return

        else:
            # 削除するパターン
            for header in self.headers:
                if header not in new_headers:
                    self._remove_header(header)
                    return
