"""https://docs.python.org/ja/3/library/unittest.html
全てのアサーション : https://docs.python.org/ja/3/library/unittest.html#unittest.TestCase
"""
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

    # @unittest.skip("skip")
    @unittest.skipIf(RELEASE_NAME == "test", "skip")
    def test_add_num_and_double_skip(self):
        self.assertEqual(self.cal.add_num_and_double(2, 2), 8)

    def test_add_num_and_double_raise(self):
        # 例外処理にはwithステートメントを使う
        with self.assertRaises(ValueError):
            self.cal.add_num_and_double("1", "1")


# unittest.main()で実行
if __name__ == "__main__":
    unittest.main()

# CLIで実行することも出来る
# python -m unittest test_module_1.py test_module_2.py
