def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    pass


def check(label: str, actual, expected) -> None:
    status = "OK" if actual == expected else "NG"
    print(f"[{status}] {label}")
    if status == "NG":
        print(f"    got:      {actual}")
        print(f"    expected: {expected}")


if __name__ == "__main__":
    cases = [
        (([[1, 4, 5], [1, 3, 4], [2, 6]],), [1, 1, 2, 3, 4, 4, 5, 6]),
        (([[1, 2, 3], [], [0, 4]],), [0, 1, 2, 3, 4]),
        (([],), []),
        (([[], []],), []),
        (([[5], [3], [1]],), [1, 3, 5]),
        (([[1, 1, 1], [1, 1], [1]],), [1, 1, 1, 1, 1, 1]),
        (([[-5, -3, 0], [-4, -2, 1]],), [-5, -4, -3, -2, 0, 1]),
        (([[1, 2, 3]],), [1, 2, 3]),
        (([[2, 4, 6], [1, 3, 5], [0]],), [0, 1, 2, 3, 4, 5, 6]),
    ]
    for args, expected in cases:
        actual = merge_sorted_list(*args)
        check(f"merge_sorted_list{args}", actual, expected)
