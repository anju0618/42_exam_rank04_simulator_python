def array_rotation_detector(arr1: list, arr2: list) -> bool:



if __name__ == "__main__":
    res =[
        array_rotation_detector([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]),
        array_rotation_detector([1, 2, 3, 4, 5], [5, 1, 2, 3, 4]),
        array_rotation_detector([1, 2, 3], [3, 2, 1]),
        array_rotation_detector([1, 2], [1, 2, 3]),
        array_rotation_detector([], [])
    ]

    print(res)