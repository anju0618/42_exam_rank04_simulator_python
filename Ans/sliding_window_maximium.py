def sliding_window_maximium(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []

    idx = []  # ウィンドウ内で最大値になり得るインデックスを単調減少で保持する自前の両端キュー
    head = 0
    res = []

    for i, num in enumerate(nums):
        # ウィンドウの範囲外になった古いインデックスは先頭ポインタを進めて無視する
        if idx and idx[head] <= i - k:
            head += 1

        # これから追加する値以下の要素は、今後絶対に最大値にならないので末尾から取り除く
        while len(idx) > head and nums[idx[-1]] < num:
            idx.pop()

        idx.append(i)

        if i >= k - 1:
            res.append(nums[idx[head]])

    return res
