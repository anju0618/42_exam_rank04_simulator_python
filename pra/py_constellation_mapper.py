def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:



if __name__ == "__main__":
    a = constellation_mapper([(0, 0), (1, 1), (2, 2)], 3)
    b = constellation_mapper([(0, 0), (0, 1), (0, 2), (1, 1), (2, 2)], 3)
    c = constellation_mapper([(0, 0), (5, 5), (2, 2)], 3)
    d = constellation_mapper([(0, 0), (5, 5)], 2)
    print(a)
    print(b)
    print(c)
    print(d)