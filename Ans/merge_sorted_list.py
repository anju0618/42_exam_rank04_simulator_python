import heapq


def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    # 各リストがソート済みであることを利用し、O(N log K) でマージする
    return list(heapq.merge(*lists))
