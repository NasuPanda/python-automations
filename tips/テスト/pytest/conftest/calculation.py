import os


class Cal(object):
    def add_num_and_double(self, x, y):
        """Add and double."""
        if type(x) is not int or type(y) is not int:
            raise ValueError
        result = x + y
        result *= 2
        return result

    def save(self, dir_path, filename):
        """テキストファイルを生成する"""
        os.makedirs(dir_path, exist_ok=True)
        filepath = os.path.join(dir_path, filename)

        with open(filepath, "w") as f:
            f.write("test")
