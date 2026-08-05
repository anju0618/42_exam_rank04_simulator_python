def list_intersection_finder(lists: list[list[int]]) -> list[int]:
    if not lists or not all(lists): return []
    return sorted(set(lists[0]).intersection(*lists))


if __name__ == "__main__":
    res = [
        list_intersection_finder([[1, 2, 3], [2, 3, 4], [2, 3, 5]]),
        list_intersection_finder([[1, 2, 3, 4], [2, 4, 6, 8], [4, 8, 12]]),
        list_intersection_finder([[1, 1, 2, 3], [1, 2, 2, 3], [1, 2, 3, 3]]),    
        list_intersection_finder([[1, 2, 3], [4, 5, 6]]),
        list_intersection_finder([]),
        list_intersection_finder([[1, 2, 3], []]),
        list_intersection_finder([[5]])
    ]
    print(res)