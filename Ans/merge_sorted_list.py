def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    # (値, リスト番号, インデックス) を要素とする自前の二分ヒープでk-wayマージし、O(N log K) を実現する
    heap = []

    def push(item):
        heap.append(item)
        i = len(heap) - 1
        while i > 0:
            parent = (i - 1) // 2
            if heap[parent] <= heap[i]:
                break
            heap[parent], heap[i] = heap[i], heap[parent]
            i = parent

    def pop():
        top = heap[0]
        last = heap.pop()
        if heap:
            heap[0] = last
            i = 0
            n = len(heap)
            while True:
                left = 2 * i + 1
                right = 2 * i + 2
                smallest = i
                if left < n and heap[left] < heap[smallest]:
                    smallest = left
                if right < n and heap[right] < heap[smallest]:
                    smallest = right
                if smallest == i:
                    break
                heap[i], heap[smallest] = heap[smallest], heap[i]
                i = smallest
        return top

    for li, lst in enumerate(lists):
        if lst:
            push((lst[0], li, 0))

    result = []
    while heap:
        value, li, idx = pop()
        result.append(value)
        if idx + 1 < len(lists[li]):
            push((lists[li][idx + 1], li, idx + 1))

    return result
