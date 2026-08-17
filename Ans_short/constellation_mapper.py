def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:
    s = set(stars)
    return ["".join("*" if (r, c) in s else "." for c in range(size)) for r in range(size)]
