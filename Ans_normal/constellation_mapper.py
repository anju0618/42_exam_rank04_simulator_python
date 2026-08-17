def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:
    grid = []
    for r in range(size):
        row = []
        for c in range(size):
            row.append(".")
        grid.append(row)

    for r, c in stars:
        if 0 <= r < size and 0 <= c < size:
            grid[r][c] = "*"

    result = []
    for row in grid:
        result.append("".join(row))
    return result
