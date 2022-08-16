import sqlite3

db_name = "TEST.db"
table_name = "providers"
query = "id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, url STRING"


def create_db(db_name: str, table_name: str, query: str) -> sqlite3.Connection:
    # DBが存在しなければ作成して接続、存在すれば接続
    connection = sqlite3.connect(db_name)
    # SQLiteを操作するカーソルオブジェクトを生成
    cursor = connection.cursor()

    # テーブル作成
    cursor.execute(f"CREATE TABLE {table_name}({query})")
    # DBへコミット 変更が反映される
    connection.commit()

    return connection


con = create_db(db_name, table_name, query)
con.close()
