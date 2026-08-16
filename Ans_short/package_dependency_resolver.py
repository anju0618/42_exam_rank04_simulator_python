def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    deg = {p: 0 for p in packages}
    graph = {p: [] for p in packages}
    for p, deps in packages.items():
        for d in deps:
            graph[d].append(p)
            deg[p] += 1

    res, wave = [], sorted(p for p in deg if deg[p] == 0)
    while wave:
        res += wave
        nxt = set()
        for p in wave:
            for n in graph[p]:
                deg[n] -= 1
                if deg[n] == 0:
                    nxt.add(n)
        wave = sorted(nxt)
    return res if len(res) == len(packages) else []
