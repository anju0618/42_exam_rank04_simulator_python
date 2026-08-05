#!/usr/bin/env python3
def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:
    S = set(stars)
    return ["".join("*" if (r, c) in S else "." for c in range(size)) for r in range(size)]


if __name__ == "__main__":
    res = [
        constellation_mapper([(0, 0), (1, 1), (2, 2)], 3),
        constellation_mapper([(0, 0), (0, 1), (0, 2), (1, 1), (2, 2)], 3),
        constellation_mapper([(0, 0), (5, 5), (2, 2)], 3),
        constellation_mapper([(0, 0), (5, 5)], 2)
    ]

    print(res)