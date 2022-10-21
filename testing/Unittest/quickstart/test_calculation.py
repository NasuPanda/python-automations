"""https://docs.python.org/ja/3/library/unittest.html
"""
import unittest

import calculation


# unittest.TestCase を継承する
class CalTest(unittest.TestCase):
    # test_method_name とする
    def test_add_num_and_double(self):
        cal = calculation.Cal()
        # その他のアサーション : https://docs.python.org/ja/3/library/unittest.html#unittest.TestCase
        self.assertEqual(cal.add_num_and_double(1, 1), 4)


# unittest.main()で実行
if __name__ == "__main__":
    unittest.main()

# CLIで実行することも出来る
# python -m unittest test_module_1.py test_module_2.py
