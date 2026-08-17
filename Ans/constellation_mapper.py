def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:
    # size x size のグリッドを"."で初期化し、範囲内の星だけ"*"に書き換える(重複座標は上書きされるだけなので自然に無視される)
    grid = [["."] * size for _ in range(size)]
    for r, c in stars:
        if 0 <= r < size and 0 <= c < size:
            grid[r][c] = "*"
    return ["".join(row) for row in grid]
