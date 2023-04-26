import requests


class ThirdPartyBonusRestApi(object):
    """サードパーティのAPI"""

    def bonus_price(self, year):
        res = requests.get("http://localhost/bonus", params={"year": year})
        # ex: {"price": 10000000}
        return res.json()["price"]

    @classmethod
    def name(cls):
        return "Bonus API"


class Salary(object):
    def __init__(self, base=100, year=2017):
        self.bonus_api = ThirdPartyBonusRestApi()
        self.base = base
        self.year = year

    def calculation_salary(self):
        """APIを叩くコード"""
        try:
            bonus = self.bonus_api.bonus_price(year=self.year)
        except ConnectionRefusedError:
            bonus = 0
        return self.base + bonus
