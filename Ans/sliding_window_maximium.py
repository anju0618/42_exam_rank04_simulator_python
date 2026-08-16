from collections import deque


def sliding_window_maximium(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []

    dq = deque()  # ウィンドウ内の「最大値になり得る候補」のインデックスを単調減少で保持
    res = []

    for i, num in enumerate(nums):
        # ウィンドウの範囲外になった古いインデックスを削除
        if dq and dq[0] <= i - k:
            dq.popleft()

        # これから追加する値以下の要素は、今後絶対に最大値にならないので削除
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            res.append(nums[dq[0]])

    return res
