def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    pass


if __name__ == "__main__":
    res = [
        package_dependency_resolver({"app": ["database"], "database": ["driver"], "driver": []}),
        package_dependency_resolver({"A": [], "B": ["A"], "C": ["A", "B"]}),
        package_dependency_resolver({}),
        package_dependency_resolver({"X": ["Y"], "Y": ["X"]}),
        package_dependency_resolver({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]})
    ]
    print(res)
