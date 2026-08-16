def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    if not packages:
        return []

    graph = {p: [] for p in packages}
    in_degree = {p: 0 for p in packages}
    for p, deps in packages.items():
        for d in deps:
            if d in packages:
                graph[d].append(p)
                in_degree[p] += 1

    res = []
    # 同じ深さ（波）のパッケージをまとめてアルファベット順に処理する。
    # min()で毎回1つずつ拾う方式だと、後の波で解禁されたパッケージが
    # 先行する波のパッケージより先に選ばれてしまう場合がある。
    frontier = sorted(p for p, deg in in_degree.items() if deg == 0)
    while frontier:
        next_frontier = set()
        for node in frontier:
            res.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    next_frontier.add(neighbor)
        frontier = sorted(next_frontier)

    return res if len(res) == len(packages) else []
