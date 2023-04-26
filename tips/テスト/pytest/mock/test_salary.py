import unittest
from unittest import mock
from unittest.mock import MagicMock

import salary


class TestSalary(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch("salary.ThirdPartyBonusRestApi.bonus_price")
        self.mock_bonus = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_calculation_salary(self):
        s = salary.Salary(base=100, year=2017)
        s.bonus_api.bonus_price = MagicMock(return_value=1)

        self.assertEqual(s.calculation_salary(), 101)

        s.bonus_api.bonus_price.assert_called()
        s.bonus_api.bonus_price.assert_called_once()
        s.bonus_api.bonus_price.assert_called_with(year=2017)

        self.assertEqual(s.bonus_api.bonus_price.call_count, 1)

    @mock.patch("salary.ThirdPartyBonusRestApi.bonus_price")
    def test_calculation_salary_patch(self, mock_bonus):
        """デコレータで patch"""
        mock_bonus.return_value = 1

        s = salary.Salary(base=100, year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        mock_bonus.assert_called()

    def test_calculation_salary_patch_with_statement(self):
        """with で patch"""
        with mock.patch("salary.ThirdPartyBonusRestApi.bonus_price") as mock_bonus:
            mock_bonus.return_value = 1

            s = salary.Salary(base=100, year=2017)
            salary_price = s.calculation_salary()

            self.assertEqual(salary_price, 101)
            mock_bonus.assert_called()

    def test_calculation_salary_patch_patcher(self):
        """patcher で patch"""
        # start
        patcher = mock.patch("salary.ThirdPartyBonusRestApi.bonus_price")
        mock_bonus = patcher.start()
        mock_bonus.return_value = 1

        s = salary.Salary(base=100, year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        mock_bonus.assert_called()

        # stop
        patcher.stop()

    def test_calculation_salary_patch_by_side_effect(self):
        """side effect で patch"""

        def f(year):
            return 1

        self.mock_bonus.side_effect = f
        s = salary.Salary(base=100, year=2017)

        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        self.mock_bonus.assert_called()

    @mock.patch("salary.ThirdPartyBonusRestApi", spec=True)
    def test_calculation_salary_class(self, mock_rest):
        """クラスごとモックに"""
        # return_value メソッドはでモックを返す
        mock_rest = mock_rest.return_value
        mock_rest.bonus_price.return_value = 1

        s = salary.Salary(base=100, year=2017)
        salary_price = s.calculation_salary()

        self.assertEqual(salary_price, 101)
        mock_rest.bonus_price.assert_called()


if __name__ == "__main__":
    unittest.main()
