def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    res = []
    while len(res) < len(packages):
        # 未処理かつ、依存先が「存在しない」か「解決済み」のものを探す
        ready = [p for p, deps in packages.items() if p not in res and all(d not in packages or d in res for d in deps)]
        if not ready: return [] # 循環依存などで処理可能なものがない場合
        res.append(min(ready)) # アルファベット順で処理
    return res
