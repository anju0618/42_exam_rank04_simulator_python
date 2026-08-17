def array_rotation_detector(arr1: list, arr2: list) -> bool:
    if len(arr1) != len(arr2):
        return False
    if not arr1:
        return True
    n = len(arr1)
    doubled = arr1 + arr1  # 連結を1回だけ行い、部分列としてarr2を探す
    return any(doubled[i:i + n] == arr2 for i in range(n))
