def list_intersection_finder(lists: list[list[int]]) -> list[int]:
    if not lists or not all(lists):
        return []

    result = []
    for value in lists[0]:
        if value in result:
            continue  # すでに結果に入っている値は重複させない
        in_all = True
        for other in lists[1:]:
            if value not in other:
                in_all = False
                break
        if in_all:
            result.append(value)
    return sorted(result)
