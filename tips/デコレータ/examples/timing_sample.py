import time


def func_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} は実行に {end_time - start_time:.2f} 秒かかりました")
        return result
    return wrapper

@func_timer
def slow_function():
    time.sleep(2)
    return "終了"

print(slow_function())
