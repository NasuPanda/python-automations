# デコレータについて
## 何が便利なのか
- コードの再利用性 ↑
- コードの読みやすさ ↑

## 前提
### クロージャ
関数の内部で定義された別の関数のこと。

クロージャは親関数のスコープ内の変数にアクセス出来る。

下の `times_two` 関数の処理結果はクロージャの結果を返します。
```py
def make_multiplier(x):
    def multiplier(n):
        return x * n
    return multiplier

times_two = make_multiplier(2)
print(times_two(3))  # 6
```

### デコレータの基本構造

```py
def my_decorator(func):
    def wrapper():
        print("関数実行前の処理")
        result = func()
        print("関数実行後の処理")
        return result

    return wrapper
```

デコレータは、関数定義の上に `@` 記号とともに記述することで適用出来る。
```py
@my_decorator
def greet():
    return "Hello, World!"

print(greet())  # `@my_decorator` が適用された greet関数 が実行される
```

## 例
### 実行時間測定
```py
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
```

### ロギング
```py
import logging

def logging_decorator(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__} with arguments {args} and {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result}")
        return result
    return wrapper

@logging_decorator
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
```
