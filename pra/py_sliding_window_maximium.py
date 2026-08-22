def sliding_window_maximium(nums: list[int], k: int) -> list[int]:
    pass


def check(label: str, actual, expected) -> None:
    status = "OK" if actual == expected else "NG"
    print(f"[{status}] {label}")
    if status == "NG":
        print(f"    got:      {actual}")
        print(f"    expected: {expected}")


if __name__ == "__main__":
    cases = [
        (([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]),
        (([4, 2, 12, 11, -5], 2), [4, 12, 12, 11]),
        (([], 3), []),
        (([5], 1), [5]),
        (([1, 2, 3, 4, 5], 1), [1, 2, 3, 4, 5]),
        (([5, 4, 3, 2, 1], 5), [5]),
        (([2, 2, 2, 2], 2), [2, 2, 2]),
        (([-1, -3, -5, -2], 2), [-1, -3, -2]),
        (([1, 2, 3, 4, 5], 0), []),
    ]
    for args, expected in cases:
        actual = sliding_window_maximium(*args)
        check(f"sliding_window_maximium{args}", actual, expected)
