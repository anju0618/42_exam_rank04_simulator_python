def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    res = []
    while len(res) < len(packages):
        ready = [p for p, deps in packages.items() if p not in res and all(d not in packages or d in res for d in deps)]
        if not ready: return []
        res.append(min(ready))
    return res


if __name__ == "__main__":
    res = [
        package_dependency_resolver({"app": ["database"], "database": ["driver"], "driver": []}),
        package_dependency_resolver({"A": [], "B": ["A"], "C": ["A", "B"]}),
        package_dependency_resolver({}),
        package_dependency_resolver({"X": ["Y"], "Y": ["X"]}),
        package_dependency_resolver({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]})
    ]
    print(res)