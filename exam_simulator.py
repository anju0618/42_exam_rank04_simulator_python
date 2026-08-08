#!/usr/bin/env python3
import os
import sys
import importlib.util

PROBLEMS = {
    "practice/level1/py_array_rotation_detector.py": {
        "level": 1,
        "name": "array_rotation_detector",
        "signature": "def array_rotation_detector(arr1: list, arr2: list) -> bool:",
        "description": "Determine if the second list is a rotation of the first list.",
        "tests": [
            (([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]), True),
            (([1, 2, 3, 4, 5], [5, 1, 2, 3, 4]), True),
            (([1, 2, 3], [3, 2, 1]), False),
            (([1, 2], [1, 2, 3]), False),
            (([], []), True),
        ]
    },
    "practice/level1/py_constellation_mapper.py": {
        "level": 1,
        "name": "constellation_mapper",
        "signature": "def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:",
        "description": "Map stars onto a grid of size x size.",
        "tests": [
            (([(0, 0), (1, 1), (2, 2)], 3), ["*..", ".*.", "..*"]),
            (([(0, 0), (0, 1), (0, 2), (1, 1), (2, 2)], 3), ["***", ".*.", "..*"]),
            (([(0, 0), (5, 5), (2, 2)], 3), ["*..", "...", "..*"]),
            (([(0, 0), (5, 5)], 2), ["*.", ".."]),
        ]
    },
    "practice/level1/py_list_intersection_finder.py": {
        "level": 1,
        "name": "list_intersection_finder",
        "signature": "def list_intersection_finder(lists: list[list[int]]) -> list[int]:",
        "description": "Find the intersection of multiple sorted lists.",
        "tests": [
            (([[1, 2, 3], [2, 3, 4], [2, 3, 5]],), [2, 3]),
            (([[1, 2, 3, 4], [2, 4, 6, 8], [4, 8, 12]],), [4]),
            (([[1, 1, 2, 3], [1, 2, 2, 3], [1, 2, 3, 3]],), [1, 2, 3]),
            (([[1, 2, 3], [4, 5, 6]],), []),
            (([],), []),
            (([[1, 2, 3], []],), []),
            (([[5]],), [5]),
        ]
    },
    "practice/level2/py_palindrome_partitioner.py": {
        "level": 2,
        "name": "palindrome_partitioner",
        "signature": "def palindrome_partitioner(s: str) -> int:",
        "description": "Find the minimum number of cuts needed to partition a string into palindromes.",
        "tests": [
            (("aab",), 1),
            (("aba",), 0),
            (("abc",), 2),
            (("",), 0),
            (("a",), 0),
        ]
    },
    "practice/level2/py_merge_sorted_list.py": {
        "level": 2,
        "name": "merge_sorted_list",
        "signature": "def merge_sorted_list(lists: list[list[int]]) -> list[int]:",
        "description": "Merge a list of sorted integer sublists into a single sorted list.",
        "tests": [
            (([[1, 4, 5], [1, 3, 4], [2, 6]],), [1, 1, 2, 3, 4, 4, 5, 6]),
            (([[1, 2, 3], [], [0, 4]],), [0, 1, 2, 3, 4]),
            (([],), []),
            (([[], []],), []),
        ]
    },
    "practice/level2/py_sliding_window_maximium.py": {
        "level": 2,
        "name": "sliding_window_maximium",
        "signature": "def sliding_window_maximium(nums: list[int], k: int) -> list[int]:",
        "description": "Find the maximum value in a sliding window of size k.",
        "tests": [
            (([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]),
            (([4, 2, 12, 11, -5], 2), [4, 12, 12, 11]),
            (([], 3), []),
        ]
    },
    "practice/level3/package_dependency_resolver.py": {
        "level": 3,
        "name": "package_dependency_resolver",
        "signature": "def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:",
        "description": "Determine valid package installation order using topological sorting.",
        "tests": [
            (({"app": ["database"], "database": ["driver"], "driver": []},), ["driver", "database", "app"]),
            (({"A": [], "B": ["A"], "C": ["A", "B"]},), ["A", "B", "C"]),
            (({},), []),
            (({"X": ["Y"], "Y": ["X"]},), []),
            (({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]},), ["api", "web", "backend", "frontend"]),
        ]
    }
}

def ensure_dirs():
    for path in PROBLEMS.keys():
        d = os.path.dirname(path)
        os.makedirs(d, exist_ok=True)

def main():
    ensure_dirs()
    print("=== 42 Exam Rank 04 Simulator ===")
    print("Type 'help' for available commands.\n")

    while True:
        try:
            cmd = input("amakino@42:exam4 (main)> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting exam simulator.")
            break

        if not cmd:
            continue

        parts = cmd.split()
        action = parts[0]

        if action == "exit" or action == "quit":
            break
        elif action == "ls":
            # Simple ls simulation
            if "-a" in parts or len(parts) == 1:
                files = list(PROBLEMS.keys())
                print("  ".join(files))
            else:
                print("ls: invalid option")
        elif action == "cat" and len(parts) > 1:
            target = parts[1]
            if target in PROBLEMS:
                p = PROBLEMS[target]
                print(f"--- {target} ---")
                print(f"Level: {p['level']}")
                print(f"Description: {p['description']}")
                print(f"Signature: {p['signature']}")
            else:
                print(f"cat: {target}: No such file or directory")
        elif action == "grade" and len(parts) > 1:
            target = parts[1]
            if target not in PROBLEMS:
                print(f"grade: {target}: No such problem file")
                continue
            
            if not os.path.exists(target):
                print(f"[-] {target} not found. Please create the file and implement the function.")
                continue

            # Load module dynamically
            p_info = PROBLEMS[target]
            func_name = p_info["name"]
            
            try:
                spec = importlib.util.spec_from_file_location("user_solution", target)
                mod = importlib.util.module_from_spec(spec)
                sys.modules["user_solution"] = mod
                spec.loader.exec_module(mod)
                
                func = getattr(mod, func_name)
            except Exception as e:
                print(f"[-] KO: Failed to load or compile {target}")
                print(f"    Error: {e}")
                continue

            # Run tests
            passed = True
            for i, (args, expected) in enumerate(p_info["tests"]):
                try:
                    result = func(*args)
                    if result != expected:
                        print(f"[-] Test {i+1} KO")
                        print(f"    Input:    {args}")
                        print(f"    Expected: {expected}")
                        print(f"    Got:      {result}")
                        passed = False
                    else:
                        print(f"[+] Test {i+1} OK")
                except Exception as e:
                    print(f"[-] Test {i+1} KO (Exception raised)")
                    print(f"    Error: {e}")
                    passed = False

            if passed:
                print(f"\n[+] SUCCESS: {target} passed all tests! CONGRATULATIONS!")
            else:
                print(f"\n[-] FAILURE: {target} failed some tests.")
        elif action == "help":
            print("Available commands:")
            print("  ls -a                   : List all problem files")
            print("  cat <filepath>          : View problem details and signature")
            print("  grade <filepath>        : Test and grade your implementation")
            print("  help                    : Show this help message")
            print("  exit / quit             : Exit simulator")
        else:
            print(f"zsh: command not found: {action}")

if __name__ == "__main__":
    main()
