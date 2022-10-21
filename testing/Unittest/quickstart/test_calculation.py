"""https://docs.python.org/ja/3/library/unittest.html
全てのアサーション : https://docs.python.org/ja/3/library/unittest.html#unittest.TestCase
"""
import unittest

import calculation


class CalTest(unittest.TestCase):
    """Testing Cal.

    - unittest.TestCase を継承する
    - メソッド名は test_method_name とする
    """

    def test_add_num_and_double(self):
        cal = calculation.Cal()
        self.assertEqual(cal.add_num_and_double(1, 1), 4)

    def test_add_num_and_double_raise(self):
        cal = calculation.Cal()
        # 例外処理にはwithステートメントを使う
        with self.assertRaises(ValueError):
            cal.add_num_and_double("1", "1")


# unittest.main()で実行
if __name__ == "__main__":
    unittest.main()

# CLIで実行することも出来る
# python -m unittest test_module_1.py test_module_2.py
