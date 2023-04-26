class Cal(object):
    def add_num_and_double(self, x, y):
        """Add and double.

        - 本格的なテストというより、ドキュメント + テスト というイメージ
        - 対話型シェル形式で記述
            - `>>>` から記述
        - 例外が出ることを確認したい場合は下のように記述
            - ... で省略

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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
