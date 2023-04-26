# Utils

- [Utils](#utils)
  - [re](#re)
    - [参考](#参考)
  - [pathlib](#pathlib)
    - [参考](#参考-1)
  - [datetime](#datetime)
    - [参考](#参考-2)
  - [sqlite3](#sqlite3)
    - [参考](#参考-3)

## re
Pythonで正規表現の処理を行うには標準ライブラリのreモジュールを使う.

正規表現パターンによる文字列の抽出や置換、分割などができる.

### 参考
公式:
- [re --- 正規表現操作 — Python 3.11.3 ドキュメント](https://docs.python.org/ja/3/library/re.html)
わかりやすい:
- [Pythonの正規表現モジュールreの使い方（match, search, subなど） | note.nkmk.me](https://note.nkmk.me/python-re-match-search-findall-etc/)
- [Pythonの正規表現マッチオブジェクトでマッチした文字列や位置を取得 | note.nkmk.me](https://note.nkmk.me/python-re-match-object-span-group/)
- [Pythonで文字列を検索（〜を含むか判定、位置取得） | note.nkmk.me](https://note.nkmk.me/python-str-search/)

## pathlib
Pythonでパスの操作をするときはpathlibモジュールを使うと便利.

```python
# NOTE: `Path` オブジェクトは文字列型ではないため注意. 文字列を引数として期待するメソッドにそのまま渡しても機能しない.
p_file = pathlib.Path('temp/file.txt')

print(p_file)
# temp/file.txt

print(type(p_file))
# <class 'pathlib.PosixPath'>
```

### 参考
公式:
- [pathlib — Object-oriented filesystem paths — Python 3.11.3 documentation](https://docs.python.org/3/library/pathlib.html)
わかりやすい:
- [Python, pathlibの使い方（パスをオブジェクトとして操作・処理） | note.nkmk.me](https://note.nkmk.me/python-pathlib-usage/)
- [Python, pathlibでファイル名・拡張子・親ディレクトリを取得 | note.nkmk.me](https://note.nkmk.me/python-pathlib-name-suffix-parent/)

## datetime
Pythonでdatetime(日時)の操作をするときに使うモジュール.

### 参考
- [Pythonのdatetimeで日付や時間と文字列を変換（strftime, strptime） | note.nkmk.me](https://note.nkmk.me/python-datetime-usage/)

## sqlite3
PythonでSQLiteを操作するときに使うモジュール.

### 参考
[sqlite3 — DB-API 2.0 interface for SQLite databases — Python 3.11.3 documentation](https://docs.python.org/3/library/sqlite3.html)
