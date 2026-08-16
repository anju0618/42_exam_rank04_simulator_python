def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:
    star_set = set(stars)
    grid = []
    for r in range(size):
        row = []
        for c in range(size):
            if (r, c) in star_set:
                row.append("*")
            else:
                row.append(".")
        grid.append("".join(row))
    return grid
