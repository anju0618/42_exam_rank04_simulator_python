def list_intersection_finder(lists: list[list[int]]) -> list[int]:
    if not lists or not all(lists): return [] # 空の入力や空のリストが含まれる場合
    return sorted(set(lists[0]).intersection(*lists))
