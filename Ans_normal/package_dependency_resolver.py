def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    if not packages:
        return []

    # graph[dep]には「depに依存しているパッケージ」を、
    # in_degree[name]には「nameがまだ待っている依存の数」を入れる
    graph = {name: [] for name in packages}
    in_degree = {name: 0 for name in packages}
    for name, deps in packages.items():
        for dep in deps:
            if dep in packages:
                graph[dep].append(name)
                in_degree[name] += 1

    # 依存が1つもない(=今すぐインストールできる)パッケージを集める
    ready = []
    for name in packages:
        if in_degree[name] == 0:
            ready.append(name)
    ready.sort()

    result = []
    while ready:
        next_ready = []
        for name in ready:
            result.append(name)
            for neighbor in graph[name]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    next_ready.append(neighbor)
        next_ready.sort()
        ready = next_ready

    if len(result) != len(packages):
        return []  # 全部処理しきれなかった = 循環依存がある
    return result
