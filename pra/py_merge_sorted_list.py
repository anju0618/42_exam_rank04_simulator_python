def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    pass


if __name__ == "__main__":
    res = [
        merge_sorted_list([[1, 4, 5], [1, 3, 4], [2, 6]]),
        merge_sorted_list([[1, 2, 3], [], [0, 4]]),
        merge_sorted_list([]),
        merge_sorted_list([[], []])
    ]
    print(res)
