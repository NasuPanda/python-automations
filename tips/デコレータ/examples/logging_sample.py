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
