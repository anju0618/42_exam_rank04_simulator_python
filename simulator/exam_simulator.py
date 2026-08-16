#!/usr/bin/env python3
"""42 Exam Rank 04 simulator.

Reads problem briefs from questions/level{1,2,3}/, generates stub files
to solve under simulator/workspace/, and grades them against the test
cases below with a tiny shell-like CLI (ls / cat / grade / help / exit).
"""
import os
import sys
import importlib.util

SIMULATOR_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SIMULATOR_DIR)
QUESTIONS_DIR = os.path.join(ROOT_DIR, "questions")
WORKSPACE_DIR = os.path.join(SIMULATOR_DIR, "workspace")

PROBLEMS = {
    "py_array_rotation_detector": {
        "level": 1,
        "func_name": "array_rotation_detector",
        "signature": "def array_rotation_detector(arr1: list, arr2: list) -> bool:",
        "tests": [
            (([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]), True),
            (([1, 2, 3, 4, 5], [5, 1, 2, 3, 4]), True),
            (([1, 2, 3], [3, 2, 1]), False),
            (([1, 2], [1, 2, 3]), False),
            (([], []), True),
        ],
    },
    "py_constellation_mapper": {
        "level": 1,
        "func_name": "constellation_mapper",
        "signature": "def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:",
        "tests": [
            (([(0, 0), (1, 1), (2, 2)], 3), ["*..", ".*.", "..*"]),
            (([(0, 0), (0, 1), (0, 2), (1, 1), (2, 2)], 3), ["***", ".*.", "..*"]),
            (([(0, 0), (5, 5), (2, 2)], 3), ["*..", "...", "..*"]),
            (([(0, 0), (5, 5)], 2), ["*.", ".."]),
        ],
    },
    "py_list_intersection_finder": {
        "level": 1,
        "func_name": "list_intersection_finder",
        "signature": "def list_intersection_finder(lists: list[list[int]]) -> list[int]:",
        "tests": [
            (([[1, 2, 3], [2, 3, 4], [2, 3, 5]],), [2, 3]),
            (([[1, 2, 3, 4], [2, 4, 6, 8], [4, 8, 12]],), [4]),
            (([[1, 1, 2, 3], [1, 2, 2, 3], [1, 2, 3, 3]],), [1, 2, 3]),
            (([[1, 2, 3], [4, 5, 6]],), []),
            (([],), []),
            (([[1, 2, 3], []],), []),
            (([[5]],), [5]),
        ],
    },
    "py_merge_sorted_list": {
        "level": 2,
        "func_name": "merge_sorted_list",
        "signature": "def merge_sorted_list(lists: list[list[int]]) -> list[int]:",
        "tests": [
            (([[1, 4, 5], [1, 3, 4], [2, 6]],), [1, 1, 2, 3, 4, 4, 5, 6]),
            (([[1, 2, 3], [], [0, 4]],), [0, 1, 2, 3, 4]),
            (([],), []),
            (([[], []],), []),
        ],
    },
    "py_palindrome_partitioner": {
        "level": 2,
        "func_name": "palindrome_partitioner",
        "signature": "def palindrome_partitioner(s: str) -> int:",
        "tests": [
            (("aab",), 1),
            (("aba",), 0),
            (("abc",), 2),
        ],
    },
    "py_sliding_window_maximium": {
        "level": 2,
        "func_name": "sliding_window_maximium",
        "signature": "def sliding_window_maximium(nums: list[int], k: int) -> list[int]:",
        "tests": [
            (([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]),
            (([4, 2, 12, 11, -5], 2), [4, 12, 12, 11]),
            (([], 3), []),
        ],
    },
    "package_dependency_resolver": {
        "level": 3,
        "func_name": "package_dependency_resolver",
        "signature": "def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:",
        "tests": [
            (({"app": ["database"], "database": ["driver"], "driver": []},), ["driver", "database", "app"]),
            (({"A": [], "B": ["A"], "C": ["A", "B"]},), ["A", "B", "C"]),
            (({},), []),
            (({"X": ["Y"], "Y": ["X"]},), []),
            (({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]},), ["api", "web", "backend", "frontend"]),
        ],
    },
}


def brief_path(name):
    p = PROBLEMS[name]
    return os.path.join(QUESTIONS_DIR, f"level{p['level']}", name)


def stub_path(name):
    p = PROBLEMS[name]
    return os.path.join(WORKSPACE_DIR, f"level{p['level']}", f"{name}.py")


def ensure_stub(name):
    path = stub_path(name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        signature = PROBLEMS[name]["signature"]
        with open(path, "w") as f:
            f.write(f"{signature}\n    # TODO: implement\n    pass\n")
    return path


def relpath(path):
    return os.path.relpath(path, ROOT_DIR)


def cmd_ls():
    for level in (1, 2, 3):
        names = sorted(n for n, p in PROBLEMS.items() if p["level"] == level)
        print(f"level{level}/  " + "  ".join(names))


def cmd_cat(name):
    if name not in PROBLEMS:
        print(f"cat: {name}: No such problem")
        return
    path = brief_path(name)
    print(f"--- {relpath(path)} ---")
    with open(path) as f:
        print(f.read().rstrip())
    print(f"\nWorkspace file: {relpath(ensure_stub(name))}")


def cmd_grade(name):
    if name not in PROBLEMS:
        print(f"grade: {name}: No such problem")
        return

    path = ensure_stub(name)
    p_info = PROBLEMS[name]
    func_name = p_info["func_name"]

    try:
        spec = importlib.util.spec_from_file_location("user_solution", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        func = getattr(mod, func_name)
    except Exception as e:
        print(f"[-] KO: Failed to load or compile {relpath(path)}")
        print(f"    Error: {e}")
        return

    passed = True
    for i, (args, expected) in enumerate(p_info["tests"]):
        try:
            result = func(*args)
            if result != expected:
                print(f"[-] Test {i + 1} KO")
                print(f"    Input:    {args}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                passed = False
            else:
                print(f"[+] Test {i + 1} OK")
        except Exception as e:
            print(f"[-] Test {i + 1} KO (Exception raised)")
            print(f"    Error: {e}")
            passed = False

    if passed:
        print(f"\n[+] SUCCESS: {name} passed all tests! CONGRATULATIONS!")
    else:
        print(f"\n[-] FAILURE: {name} failed some tests.")


def cmd_help():
    print("Available commands:")
    print("  ls                      : List all problems by level")
    print("  cat <name>              : View a problem's brief and signature")
    print("  grade <name>            : Test and grade your implementation")
    print("  help                    : Show this help message")
    print("  exit / quit             : Exit simulator")


def main():
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
        action, args = parts[0], parts[1:]

        if action in ("exit", "quit"):
            break
        elif action == "ls":
            cmd_ls()
        elif action == "cat" and args:
            cmd_cat(args[0])
        elif action == "grade" and args:
            cmd_grade(args[0])
        elif action == "help":
            cmd_help()
        else:
            print(f"zsh: command not found: {action}")


if __name__ == "__main__":
    main()
