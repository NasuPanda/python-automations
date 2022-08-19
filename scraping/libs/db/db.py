"""
TODO docsの整備
"""

from __future__ import annotations

import sqlite3
from typing import Literal

from libs import common


class DBError(Exception):
    pass


class InvalidColumnError(DBError):
    pass


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    result = {}
    for i, column in enumerate(cursor.description):
        result[column[0]] = row[i]
    return result


class DataBase:
    """データベースを抽象化するクラス。

    table_info = \"\"\"
    id integer unique primary key autoincrement,
    title string unique,
    latest_episode_url string unique,
    latest_episode_title string unique
    "\"\"\

    db = DataBase(
        database_path,
        common.TONARINOYJ_TABLE_NAME,
        common.ALL_COLUMNS["tonarinoyj"],
        common.UPDATABLE_COLUMNS["tonarinoyj"],
        table_info,
    )

    db.insert(
        ("title", "latest_episode_url", "latest_episode_title"),
        {
            "title": "ワンパンマン",
            "latest_episode_url": "0123456789",
            "latest_episode_title": "[第XXX話] ワンパンマン",
        },
    )
    """

    def __init__(
        self,
        db_path: str,
        table_name: str,
        columns: tuple[str, ...],
        updatable_columns: tuple[str, ...],
        table_info: str | None = None,
    ) -> None:
        """インスタンスの初期化。

        Args:
            db_path (str): DBのパス。
            table_name (str): 対象テーブル名。
            create_table_query (str): テーブルの生成に使うクエリ。
        """
        self.table_name = table_name
        self.connection = sqlite3.connect(db_path)
        # select の結果を辞書に変更
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        self.columns = columns
        self.updatable_columns = updatable_columns

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
        # NOTE: 返り値は {クエリ: 値} の辞書
        return False if self.cursor.fetchone()["COUNT(*)"] == 0 else True

    def close(self) -> None:
        """接続を閉じる。"""
        self.cursor.close()
        self.connection.close()

    def _commit(self) -> None:
        """DBに加えた変更をコミットする。"""
        self.connection.commit()

    def select(
        self,
        columns: tuple[str, ...],
        where: dict[str, str | int] | None = None,
        limit: int | None = None,
        where_logical_operator: common.LOGICAL_OPERATOR = "AND",
    ) -> list[dict]:
        """対象カラムのデータ。

        Args:
            columns (tuple[str]): 対象カラム。
            limit (None | int, optional): 取得するデータ数。 デフォルトは None 。

        Returns:
            list[tuple]: 取得したデータ。
        """
        if where:
            self.verify_where_statements(where)

        query = f"SELECT {self.column_to_query(columns)} FROM {self.table_name}"
        # オプショナルな引数を渡されたていた場合queryに追加していく
        # NOTE: 間の空白を忘れないこと
        query = (
            query + f" WHERE {self.to_where_statements(where, where_logical_operator)}" if where is not None else query
        )
        query = query + f" LIMIT {limit}" if limit else query
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_last(self, columns: tuple[str, ...]) -> dict:
        """対象カラムの最後のデータを取得。

        Args:
            columns (str): 対象カラム。

        Returns:
            tuple: 取得したデータ。
        """
        return self.select(columns, limit=1)[0]

    def insert(self, to_insert_values: common.CHANGEABLE_VALUES) -> None:
        """データをDBに挿入する。

        Args:
            columns (tuple[str, ...]): 対象カラム名。
            values (dict[str, str]): 対象データ。
        """
        columns = tuple(to_insert_values.keys())

        # 対象カラムの数だけプレースホルダを用意 ex:(?, ?, ?)
        placeholders = ",".join("?" * len(columns))
        # query: INSERT INTO table(column1, column2, ...) VALUES(?, ?, ...)
        # NOTE: columns と placeholders に 括弧() を忘れないこと
        query = f"INSERT INTO {self.table_name}({self.column_to_query(columns)}) VALUES({placeholders})"

        insert_data = []
        for column in columns:
            try:
                insert_data.append(to_insert_values[column])
            except KeyError:
                raise sqlite3.ProgrammingError(f"The column '{column}' is doesn't exist in {to_insert_values}.")

        self.cursor.execute(query, insert_data)
        self._commit()

    def update(
        self,
        to_update: common.CHANGEABLE_VALUES,
        where: dict[str, str | int],
        where_logical_operator: common.LOGICAL_OPERATOR = "AND",
    ) -> None:
        self.verify_value_to_update(to_update)
        self.verify_where_statements(where)

        query = f"""
            UPDATE {self.table_name}
            SET {self.to_set_statements(to_update)}
            WHERE {self.to_where_statements(where, where_logical_operator)}
            """
        self.connection.execute(query)

        self._commit()

    def delete(self, where: dict[str, str | int], where_logical_operator: common.LOGICAL_OPERATOR = "AND") -> None:
        self.verify_where_statements(where)

        query = f"""
            DELETE FROM {self.table_name}
            WHERE {self.to_where_statements(where, where_logical_operator)}
            """
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
    def to_set_statements(cls, to_update: common.CHANGEABLE_VALUES) -> str:
        queries = []
        for key, value in to_update.items():
            # value が文字列型なら ''シングルクォーテーション で囲み、そうでないならそのまま
            query = f"{key}='{value}'" if type(value) == str else f"{key}={value}"
            queries.append(query)
        return ", ".join(queries)

    @classmethod
    def to_where_statements(
        cls, to_where: dict[str, str | int], where_logical_operator: Literal["AND", "OR"] = "AND"
    ) -> str:
        queries = []
        for key, value in to_where.items():
            query = f"{key}='{value}'" if type(value) == str else f"{key}={value}"
            queries.append(query)
        return f" {where_logical_operator} ".join(queries)

    def verify_columns(self, columns: tuple[str, ...]) -> None:
        for column in columns:
            if column not in self.columns:
                raise InvalidColumnError(f"This column is invalid {column}")

    def verify_where_statements(self, where_statements: dict[str, str | int]) -> None:
        for key in where_statements.keys():
            if key not in self.columns:
                raise InvalidColumnError(f"This column is invalid: {key}")

    def verify_value_to_update(self, to_update: common.CHANGEABLE_VALUES) -> None:
        for key in to_update.keys():
            if key not in self.updatable_columns:
                raise InvalidColumnError(f"This column is invalid: {key}")

    def verify_value_to_insert(self, to_insert: common.CHANGEABLE_VALUES) -> None:
        # update のエイリアスとして記入
        self.verify_value_to_update(to_insert)
