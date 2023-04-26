"""https://docs.pytest.org/en/7.1.x/
"""
import calculation
import pytest


def test_add_num_and_double():
    cal = calculation.Cal()
    assert cal.add_num_and_double(1, 1) == 4


class TestCal(object):
    @classmethod
    def setup_class(cls):
        print("start")
        cls.cal = calculation.Cal()

    @classmethod
    def teardown_class(cls):
        print("end")
        del cls.cal

    def setup_method(self, method):
        print("setup", method)
        # self.cal = calculation.Cal()

    def teardown_method(self, method):
        print("tear down", method)
        # del self.cal

    def test_add_num_and_double(self):
        assert self.cal.add_num_and_double(1, 1) == 4

    def test_add_num_and_double_raise(self):
        with pytest.raises(ValueError):
            self.cal.add_num_and_double("1", "1")

    # @pytest.mark.skipif(IS_RELEASE==True, reason="skip")
    @pytest.mark.skip(reason="skip!")
    def test_skip(self):
        assert self.cal.add_num_and_double(2, 2) == 8
