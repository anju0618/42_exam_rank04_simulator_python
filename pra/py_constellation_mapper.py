def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:
    pass


def check(label: str, actual, expected) -> None:
    status = "OK" if actual == expected else "NG"
    print(f"[{status}] {label}")
    if status == "NG":
        print(f"    got:      {actual}")
        print(f"    expected: {expected}")


if __name__ == "__main__":
    cases = [
        (([(0, 0), (1, 1), (2, 2)], 3), ["*..", ".*.", "..*"]),
        (([(0, 0), (0, 1), (0, 2), (1, 1), (2, 2)], 3), ["***", ".*.", "..*"]),
        (([(0, 0), (5, 5), (2, 2)], 3), ["*..", "...", "..*"]),
        (([(0, 0), (5, 5)], 2), ["*.", ".."]),
        (([], 2), ["..", ".."]),
        (([(0, 0)], 1), ["*"]),
        (([(-1, 0), (0, 0)], 2), ["*.", ".."]),
        (([(1, 1), (1, 1), (1, 1)], 2), ["..", ".*"]),
        (([(0, 0), (0, 1), (1, 0), (1, 1)], 2), ["**", "**"]),
    ]
    for args, expected in cases:
        actual = constellation_mapper(*args)
        check(f"constellation_mapper{args}", actual, expected)
