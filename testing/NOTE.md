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
