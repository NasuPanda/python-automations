import time
from typing import TypedDict

import pyautogui


class Order(TypedDict):
    key: str
    wait_time_sec: int


def send_key(key: str) -> str:
    """Send a target key.

    Args:
        key (str): A target key.

    Returns:
        str: Sent key.
    """
    pyautogui.press(key)
    return key


def delay_sec(wait_time_sec: int) -> float:
    """Stop process for seconds.

    Args:
        wait_time_sec (int): Wait time(sec).

    Returns:
        float: Actual wait time.
    """
    start_at = time.perf_counter()

    while True:
        if time.perf_counter() - start_at > wait_time_sec:
            return time.perf_counter() - start_at


def exec_order(order: Order) -> str:
    """Execute order.

    Args:
        order (Order): Dict contains key and wait time.
    """
    result = f"Wait for: {delay_sec(order['wait_time_sec'])} [s]\n"
    result += f"Sent key: {send_key(order['key'])}"
    return result


def main() -> None:
    """Main."""
    # NOTE: 変更するのはここ
    order = Order(key="esc", wait_time_sec=840)
    print(exec_order(order))


if __name__ == "__main__":
    main()
