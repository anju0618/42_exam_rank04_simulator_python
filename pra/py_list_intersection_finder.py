def list_intersection_finder(lists: list[list[int]]) -> list[int]:
    pass


def check(label: str, actual, expected) -> None:
    status = "OK" if actual == expected else "NG"
    print(f"[{status}] {label}")
    if status == "NG":
        print(f"    got:      {actual}")
        print(f"    expected: {expected}")


if __name__ == "__main__":
    cases = [
        (([[1, 2, 3], [2, 3, 4], [2, 3, 5]],), [2, 3]),
        (([[1, 2, 3, 4], [2, 4, 6, 8], [4, 8, 12]],), [4]),
        (([[1, 1, 2, 3], [1, 2, 2, 3], [1, 2, 3, 3]],), [1, 2, 3]),
        (([[1, 2, 3], [4, 5, 6]],), []),
        (([],), []),
        (([[1, 2, 3], []],), []),
        (([[5]],), [5]),
        (([[1, 2, 3], [1, 2, 3], [1, 2, 3]],), [1, 2, 3]),
        (([[3, 2, 1], [2, 3, 1]],), [1, 2, 3]),
        (([[1], [1], [1], [1]],), [1]),
        (([[1, 2], [3, 4], [1, 2]],), []),
        (([[-3, -1, 0, 2], [-3, 0, 2, 5], [-3, 0, 2]],), [-3, 0, 2]),
    ]
    for args, expected in cases:
        actual = list_intersection_finder(*args)
        check(f"list_intersection_finder{args}", actual, expected)
