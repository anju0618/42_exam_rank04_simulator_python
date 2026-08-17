def list_intersection_finder(lists: list[list[int]]) -> list[int]:
    if not lists:
        return []
    for lst in lists:
        if not lst:
            return []

    # 最初のリストの値をキーにした辞書を作り、以降のリストと突き合わせながら残る値を絞り込む(O(1)判定のため)
    present = {}
    for value in lists[0]:
        present[value] = True

    for lst in lists[1:]:
        matched = {}
        for value in lst:
            if value in present:
                matched[value] = True
        present = matched

    result = []
    for value in present:
        result.append(value)

    # 挿入ソートで昇順に並べ替える
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key

    return result
