def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    def merge_two(a, b):
        # ソート済みの2つのリストを先頭から比べながら1つにまとめる
        merged = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                merged.append(a[i])
                i += 1
            else:
                merged.append(b[j])
                j += 1
        merged.extend(a[i:])
        merged.extend(b[j:])
        return merged

    result = []
    for lst in lists:
        result = merge_two(result, lst)
    return result


def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    res = []
    for lst in lists:
        res.extend(lst)

    for _ in range(len(res) - 1):
        a = 0
        b = 1
        while b < len(res):
            if res[a] > res[b]:
                res[a], res[b] = res[b], res[a]
            a += 1
            b += 1

    return res