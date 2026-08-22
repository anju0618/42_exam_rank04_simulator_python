def array_rotation_detector(arr1: list, arr2: list) -> bool:
    pass


def check(label: str, actual, expected) -> None:
    status = "OK" if actual == expected else "NG"
    print(f"[{status}] {label}")
    if status == "NG":
        print(f"    got:      {actual}")
        print(f"    expected: {expected}")


if __name__ == "__main__":
    cases = [
        (([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]), True),
        (([1, 2, 3, 4, 5], [5, 1, 2, 3, 4]), True),
        (([1, 2, 3], [3, 2, 1]), False),
        (([1, 2], [1, 2, 3]), False),
        (([], []), True),
        (([1, 2, 3], [1, 2, 3]), True),
        (([1, 1, 1], [1, 1, 1]), True),
        (([5], [5]), True),
        (([5], [6]), False),
        (([1, 2, 3, 4], [2, 3, 1, 4]), False),
    ]
    for args, expected in cases:
        actual = array_rotation_detector(*args)
        check(f"array_rotation_detector{args}", actual, expected)
