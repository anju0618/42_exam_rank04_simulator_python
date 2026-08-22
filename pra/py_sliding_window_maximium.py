def sliding_window_maximium(nums: list[int], k: int) -> list[int]:
    pass


if __name__ == "__main__":
    res = [
        sliding_window_maximium([1, 3, -1, -3, 5, 3, 6, 7], 3),
        sliding_window_maximium([4, 2, 12, 11, -5], 2),
        sliding_window_maximium([], 3)
    ]
    print(res)
