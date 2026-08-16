def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    return sorted(x for l in lists for x in l)
