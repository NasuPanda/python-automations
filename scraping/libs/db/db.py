from __future__ import annotations

import sqlite3


class DataBase:
    """データベースを抽象化するクラス。

    Example Usage:

    db_path = "TEST.db"
    table_name = "users"
    table_info = "id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, email STRING"

    model = DataBase(db_path, table_name, table_info)

    model.insert(
        ("name", "email"),
        {"name": "alice", "email": "alice@email.com"},
        {"name": "bob", "email": "bob@gmail.com"},
    )
    model.select(("name", "email"))

    model.close()
    """

    def __init__(self, db_path: str, table_name: str, table_info: str | None = None) -> None:
        """インスタンスの初期化。

        Args:
            db_path (str): DBのパス。
            table_name (str): 対象テーブル名。
            create_table_query (str): テーブルの生成に使うクエリ。
        """
        self.table_name = table_name
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

        self.create_table_if_not_exists(table_name, table_info)

    def create_table_if_not_exists(self, table_name: str, table_info: str | None = None) -> None:
        """テーブルが存在しなければ作成する。

        Args:
            table_name (str): テーブル名。
            table_info (str | None, optional): 作成するテーブルのカラム情報を持つクエリ。デフォルトは None 。
        """
        if self.table_exists(table_name):
            return

        query = (
            f"CREATE TABLE IF NOT EXISTS {table_name}({table_info})"
            if table_info
            else f"CREATE TABLE IF NOT EXISTS {table_name}"
        )
        self.cursor.execute(query)
        self._commit()

    def table_exists(self, table_name: str) -> bool:
        self.cursor.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='{table_name}'")
        return False if self.cursor.fetchone()[0] == 0 else True

    def close(self) -> None:
        """接続を閉じる。"""
        self.cursor.close()
        self.connection.close()

    def _commit(self) -> None:
        """DBに加えた変更をコミットする。"""
        self.connection.commit()

    def select(self, columns: tuple[str, ...], where: str | None = None, limit: int | None = None) -> list[tuple]:
        """対象カラムのデータ。

        Args:
            columns (tuple[str]): 対象カラム。
            limit (None | int, optional): 取得するデータ数。 デフォルトは None 。

        Returns:
            list[tuple]: 取得したデータ。
        """
        query = f"SELECT {self.column_to_query(columns)} FROM {self.table_name}"
        query = query + f"WHERE {where}" if where is not None else query
        query = query + f"LIMIT {limit}" if limit else query
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        number_of_data = len(rows) - limit if limit else 0
        return rows[number_of_data:]

    def select_last(self, columns: tuple[str, ...]) -> tuple:
        """対象カラムの最後のデータを取得。

        Args:
            columns (str): 対象カラム。

        Returns:
            tuple: 取得したデータ。
        """
        return self.select(columns, limit=1)[0]

    def insert(self, columns: tuple[str, ...], *values: dict[str, str | int]) -> None:
        """データをDBに挿入する。

        Args:
            columns (tuple[str, ...]): 対象カラム名。
            values (dict[str, str]): 対象データ。
        """
        # 対象カラムの数だけプレースホルダを用意 ex:(?, ?, ?)
        placeholders = ",".join("?" * len(columns))
        # query: INSERT INTO table(column1, column2, ...) VALUES(?, ?, ...)
        # NOTE: columns と placeholders に 括弧() を忘れないこと
        query = f"INSERT INTO {self.table_name}({self.column_to_query(columns)}) VALUES({placeholders})"

        for value_dict in values:
            insert_data = []
            for column in columns:
                try:
                    insert_data.append(value_dict[column])
                except KeyError:
                    raise sqlite3.ProgrammingError(f"The column '{column}' is doesn't exist in {value_dict}.")
            self.cursor.execute(query, insert_data)

        self._commit()

    def update(self, updated: dict[str, str | int], where: str) -> None:
        set_statements = self.to_set_statements(updated)
        query = f"UPDATE {self.table_name} SET {set_statements} WHERE {where}"
        self.connection.execute(query)

        self._commit()

    def delete(self, where: str) -> None:
        query = f"DELETE FROM {self.table_name} WHERE {where}"
        self.connection.execute(query)

        self._commit()

    @classmethod
    def column_to_query(cls, columns: tuple[str, ...]) -> str:
        """Tuple形式のカラムをSQLクエリで使える文字列にフォーマットする。
        NOTE: 括弧() を含まない。

        Args:
            columns (tuple[str, ...]): Tuple形式のカラム。

        Returns:
            str: column or (column1, column2, ...) 形式の文字列。
        """
        # str(columns)の挙動
        # 長さ1の時      : (column1, )
        # 長さ2以上のとき : (column1, column2, ...)
        # 無効な形式にならないように長さ1の時はそのまま返す。
        query = str(columns) if len(columns) != 1 else f"({columns[0]})"
        # NOTE: ' と () は削除しておく。
        # SELECT は カラム名が ' で囲われているとエラーが出るため。
        return query.translate(str.maketrans({"'": None, "(": None, ")": None}))

    @classmethod
    def to_set_statements(cls, to_update: dict[str, str | int]) -> str:
        queries = []
        for key, value in to_update.items():
            # value が文字列型なら ''シングルクォーテーション で囲み、そうでないならそのまま
            query = f"{key}='{value}'" if type(value) == str else f"{key}={value}"
            queries.append(query)
        return ", ".join(queries)
