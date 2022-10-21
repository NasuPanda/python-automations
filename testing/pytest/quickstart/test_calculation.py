"""https://docs.pytest.org/en/7.1.x/
"""
import calculation


# test_ から始まる関数は全てテストとして認識される
def test_add_num_and_double():
    cal = calculation.Cal()
    # assert 何らかの式 と書く
    assert cal.add_num_and_double(1, 1) == 4


# クラス名は Test から始めれば良い
class TestCal(object):
    def test_add_num_and_double(self):
        cal = calculation.Cal()
        assert cal.add_num_and_double(1, 1) == 4
