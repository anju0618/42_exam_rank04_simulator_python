def palindrome_partitioner(s: str) -> int:
    pass


def check(label: str, actual, expected) -> None:
    status = "OK" if actual == expected else "NG"
    print(f"[{status}] {label}")
    if status == "NG":
        print(f"    got:      {actual}")
        print(f"    expected: {expected}")


if __name__ == "__main__":
    cases = [
        (("aab",), 1),
        (("aba",), 0),
        (("abc",), 2),
        (("",), 0),
        (("a",), 0),
        (("aa",), 0),
        (("ab",), 1),
        (("racecar",), 0),
        (("abcd",), 3),
    ]
    for args, expected in cases:
        actual = palindrome_partitioner(*args)
        check(f"palindrome_partitioner{args}", actual, expected)
