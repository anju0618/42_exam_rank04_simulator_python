def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:
    S = set(stars) # 検索をO(1)にするためセット化
    return ["".join("*" if (r, c) in S else "." for c in range(size)) for r in range(size)]
