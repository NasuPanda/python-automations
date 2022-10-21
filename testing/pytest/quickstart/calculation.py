class Cal(object):
    def add_num_and_double(self, x, y):
        """Add and double."""
        if type(x) is not int or type(y) is not int:
            raise ValueError
        result = x + y
        result *= 2
        return result
