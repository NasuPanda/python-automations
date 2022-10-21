# doctest

- 本格的なテストというより、ドキュメント + テスト というイメージ
- 対話型シェル形式で記述
    - `>>>` から記述
- 例外が出ることを確認したい場合は下のように記述
    - ... で省略可能

```py
class Cal(object):
    def add_num_and_double(self, x, y):
        """Add and double.

        >>> c = Cal()
        >>> c.add_num_and_double(1, 1)
        4

        >>> c.add_num_and_double("1", "1")
        Traceback (most recent call last):
        ...
        ValueError
        """
        if type(x) is not int or type(y) is not int:
            raise ValueError
        result = x + y
        result *= 2
        return result
```

# Unittest

pytest より機能は少ないが、Pythonに最初から組み込まれている。

- https://docs.python.org/ja/3/library/unittest.html
- 全てのアサーション : https://docs.python.org/ja/3/library/unittest.html#unittest.TestCase

```python
import unittest

import calculation

RELEASE_NAME = "test"


class CalTest(unittest.TestCase):
    """Testing Cal.

    - unittest.TestCase を継承する
    - メソッド名は test_method_name とする
    """

    def setUp(self):
        print("setup")
        self.cal = calculation.Cal()

    def tearDown(self) -> None:
        print("clean up")
        del self.cal

    def test_add_num_and_double(self):
        self.assertEqual(self.cal.add_num_and_double(1, 1), 4)

    # @unittest.skipIf(RELEASE_NAME == "test", "skip")
    @unittest.skip("skip")
    def test_add_num_and_double_skip(self):
        self.assertEqual(self.cal.add_num_and_double(2, 2), 8)

    def test_add_num_and_double_raise(self):
        # 例外処理にはwithステートメントを使う
        with self.assertRaises(ValueError):
            self.cal.add_num_and_double("1", "1")


# unittest.main()で実行
if __name__ == "__main__":
    unittest.main()
```

CLIから `python -m unittest test_module_1.py test_module_2.py` のように実行することも可能。

# pytest

## 実行

```shell
pytest

# 標準出力を見たい時
pytest -s
```

## 基本的な書き方

### 関数として

`test_` から始まる関数は全てテストとして認識される。

```py
def test_add_num_and_double():
    cal = calculation.Cal()
    # assert 何らかの式 と書くだけで良い
    assert cal.add_num_and_double(1, 1) == 4
```

### クラスとして

クラス名は `Test` から始めれば良い。

```py
import calculation

class TestCal(object):
    def test_add_num_and_double(self):
        cal = calculation.Cal()
        assert cal.add_num_and_double(1, 1) == 4
```

### 例外処理

```py
def test_raise(self):
    with pytest.raises(ValueError):
        raise ValueError
```

### setup / teardown

`setup / teardown _method` とすることでメソッド実行前後に処理を定義出来る。

```py
class TestCal(object):
    def setup_method(self, method):
        print("setup", method)
        self.cal = calculation.Cal()

    def teardown_method(self, method):
        print("tear down", method)
        del self.cal
```

上のような例であれば、 `setup / teardown _class` を使ったほうが良い。

```py
class TestCal(object):
    @classmethod
    def setup_class(cls):
        print("start")
        cls.cal = calculation.Cal()

    @classmethod
    def teardown_class(cls):
        print("end")
        del cls.cal
```

## fixture

https://rinatz.github.io/python-book/ch08-02-pytest/#_7

### pytest の fixture

あらかじめ設定された引数をテストメソッドから受け取れるようになる。

```py
def test_save(self, tmpdir):
    self.cal.save(tmpdir, self.test_filename)
    created_filepath = os.path.join(tmpdir, self.test_filename)

    assert os.path.exists(created_filepath) is True
```

### 独自の fixture

定義。pytestの fixture を受け取ることも出来る。

```py
@pytest.fixture
def csv_file(tmpdir):
    return "csv file fixture"
```

呼び出し。

```py

class TestCal(object):
    def test_add_num_and_double(self, csv_file):
        print(csv_file)
        assert self.cal.add_num_and_double(1, 1) == 4
```

#### `yield`

`yield` を使うと、Testの前後に処理を挟むことが出来る。

ファイル操作をする場合などに便利。(Test側で `with open` したり `close` したりする必要がなくなる)

```py
@pytest.fixture
def csv_file(tmpdir):
    with open(os.path.join(tmpdir, "test.csv"), "w+") as c:
        print("before test")
        yield c
        print("after test")
```

### conftest

https://rinatz.github.io/python-book/ch08-02-pytest/#conftestpy

複数のファイルを跨いで共通の fixture を共有したい時は、`conftest.py` という名前のファイルを使う。

#### `addoption`

`conftest.py` に `pytest_〇〇` とすると fixture を追加出来る。

```py
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--os-name", default="linux", help="os name")
```

`request.config.getoption("option-name")` とすると受け取ることが出来る。

```py
def test_add_num_and_double(self, request):
    os_name = request.config.getoption("--os-name")
    print(os_name)

    if os_name == "mac":
        print("ls")
    elif os_name == "windows":
        print("dir")
    assert self.cal.add_num_and_double(1, 1) == 4
```

`pytest --help` で定義したオプションを見ることが出来る。

```shell
$ pytest --help

usage: pytest [options] [file_or_dir] [file_or_dir] [...]
...
custom options:
  --os-name=OS_NAME     os name
```

## カバレッジ

テストのカバレッジを調べる。

```shell
pip install pytest-cov pytest-xdist
```

### 使い方

`pytest --cov=module_name` とする。

```shell
pytest --cov=calculation

Name             Stmts   Miss  Cover
------------------------------------
calculation.py      13      1    92%
------------------------------------
TOTAL               13      1    92%
```

カバーできていない箇所を調べるには `--cov-report term-missing` を付ける。

```shell
pytest -s --cov=calculation --cov-report term-missing

Name             Stmts   Miss  Cover   Missing
----------------------------------------------
calculation.py      13      1   92%       12
----------------------------------------------
TOTAL               13      1   92%       12
```

### どこまでテストする?

- 100% は難しい
- 会社のルールに従えばいい
  - 「80%以上にしよう」
  - 「ユニットテストは書かない」

