def sliding_window_maximium(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []

    result = []
    for start in range(len(nums) - k + 1):
        window_max = nums[start]
        for i in range(start + 1, start + k):
            if nums[i] > window_max:
                window_max = nums[i]
        result.append(window_max)
    return result
