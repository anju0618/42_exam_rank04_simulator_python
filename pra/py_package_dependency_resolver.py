def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    pass


def check(label: str, actual, expected) -> None:
    status = "OK" if actual == expected else "NG"
    print(f"[{status}] {label}")
    if status == "NG":
        print(f"    got:      {actual}")
        print(f"    expected: {expected}")


if __name__ == "__main__":
    cases = [
        (({"app": ["database"], "database": ["driver"], "driver": []},), ["driver", "database", "app"]),
        (({"A": [], "B": ["A"], "C": ["A", "B"]},), ["A", "B", "C"]),
        (({},), []),
        (({"X": ["Y"], "Y": ["X"]},), []),
        (({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]},), ["api", "web", "backend", "frontend"]),
        (({"A": ["B"], "B": ["C"], "C": ["A"]},), []),
        (({"A": ["A"]},), []),
        (({"A": [], "B": [], "C": []},), ["A", "B", "C"]),
        (({"lib": ["missing_pkg"]},), ["lib"]),
        (({"web": [], "zebra": [], "apple": ["web"]},), ["web", "zebra", "apple"]),
    ]
    for args, expected in cases:
        actual = package_dependency_resolver(*args)
        check(f"package_dependency_resolver{args}", actual, expected)
