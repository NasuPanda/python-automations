"""https://docs.pytest.org/en/7.1.x/
"""
import os

import calculation
import pytest


class TestCal(object):
    @classmethod
    def setup_class(cls):
        cls.cal = calculation.Cal()
        cls.test_filename = "test.txt"

    def test_add_num_and_double(self, csv_file):
        print(csv_file)
        assert self.cal.add_num_and_double(1, 1) == 4

    def test_add_num_and_double_raise_if_receive_strings(self):
        with pytest.raises(ValueError):
            self.cal.add_num_and_double("1", "1")

    def test_save(self, tmpdir):
        self.cal.save(tmpdir, self.test_filename)
        created_filepath = os.path.join(tmpdir, self.test_filename)

        assert os.path.exists(created_filepath) is True
