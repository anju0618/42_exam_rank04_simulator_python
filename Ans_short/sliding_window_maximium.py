def sliding_window_maximium(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]
