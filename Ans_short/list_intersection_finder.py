def list_intersection_finder(lists: list[list[int]]) -> list[int]:
    if not lists or not all(lists):
        return []
    return sorted(set(lists[0]).intersection(*lists))
