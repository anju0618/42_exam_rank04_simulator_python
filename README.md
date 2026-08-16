# Exam Rank 04 - Python Solutions & Explanations

このリポジトリは、Exam Rank 04 の各問題に対するPythonでの解答、詳細な解説、および別解（より効率的なアプローチなど）をまとめたものです。

---

## 1. Package Dependency Resolver
依存関係を解決し、インストール順序を決定する関数（トポロジカルソート）。

> **注意（タイブレークの罠）**: `min()` で1つずつ拾う方式や、`heapq` に見つかり次第push/popするグローバルな優先度付きキュー方式は、**独立した依存チェーンが複数ある場合に公式の例と結果がズレます**。
> 例: `{"web": [], "api": [], "frontend": ["web"], "backend": ["api"]}` の期待値は `["api", "web", "backend", "frontend"]` ですが、上記2方式はどちらも `["api", "backend", "web", "frontend"]` を返してしまいます（`api` の後、次に解禁される `backend` の方が `web` よりアルファベット順で早いため、先に選ばれてしまう）。
> 正しくは「同じ深さ（波）で依存解決済みになったパッケージをまとめてアルファベット順に処理し、次の波にはまだ進まない」という**層（BFS）単位のタイブレーク**が必要です。

### 解答（層ごとのKahnのアルゴリズム）
```python
def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    if not packages:
        return []

    graph = {p: [] for p in packages}
    in_degree = {p: 0 for p in packages}
    for p, deps in packages.items():
        for d in deps:
            if d in packages:
                graph[d].append(p)
                in_degree[p] += 1

    res = []
    # 同じ波（深さ）のパッケージをまとめてアルファベット順に処理する
    frontier = sorted(p for p, deg in in_degree.items() if deg == 0)
    while frontier:
        next_frontier = set()
        for node in frontier:
            res.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    next_frontier.add(neighbor)
        frontier = sorted(next_frontier)

    return res if len(res) == len(packages) else []
```

### 解説
入次数（in-degree）0のパッケージを「波（frontier)」としてまとめて取り出し、波の中はアルファベット順に処理します。ある波を処理し終えてから初めて次の波（新たに入次数0になったパッケージ）に進むので、後の波のパッケージが先の波のパッケージを追い越すことがありません。処理できるパッケージが尽きた時点で全パッケージを消化できていなければ循環依存として `[]` を返します。

---

## 2. Palindrome Partitioner
文字列を回文のみのサブ文字列に分割するための、最小カット数を求める問題。

### 解答（DPによる解法）
```python
def palindrome_partitioner(s: str) -> int:
    if not s or s == s[::-1]: return 0
    dp = [i - 1 for i in range(len(s) + 1)]
    for i in range(1, len(s) + 1):
        for j in range(i):
            if s[j:i] == s[j:i][::-1]:
                dp[i] = min(dp[i], dp[j] + 1)
    return dp[-1]
```

### 解説
`dp[i]` に「文字列の `i` 文字目までの最小カット数」を記録します。部分文字列 `s[j:i]` が回文であれば、`dp[i]` は `dp[j] + 1` で更新できる可能性があります。

### 別解（メモ化再帰による解法）
場合によってはトップダウンのほうが直感的なことがあります。
```python
from functools import lru_cache

def palindrome_partitioner(s: str) -> int:
    @lru_cache(None)
    def dfs(string):
        if not string or string == string[::-1]:
            return 0
        res = float('inf')
        for i in range(1, len(string)):
            if string[:i] == string[:i][::-1]:
                res = min(res, 1 + dfs(string[i:]))
        return res
    return dfs(s)
```

---

## 3. Array Rotation Detector
配列 `arr2` が `arr1` を回転させたものかどうかを判定する問題。

### 解答（スライスを使った直感的な解法）
```python
def array_rotation_detector(arr1: list, arr2: list) -> bool:
    if len(arr1) != len(arr2): return False
    if not arr1: return True
    return any(arr1[i:] + arr1[:i] == arr2 for i in range(len(arr1)))
```

### 解説
`arr1[i:] + arr1[:i]` で、配列を `i` 個分ずらした新しいリストを作成し、それが `arr2` と一致するかを `any()` で探します。

### 別解（リスト結合アプローチ）
実は `arr1` を2つ繋げたもの（`arr1 + arr1`）の中に、`arr2` が部分配列として含まれていれば、それは回転であると言えます。これを応用すると高速に判定できます。
```python
def array_rotation_detector(arr1: list, arr2: list) -> bool:
    if len(arr1) != len(arr2): return False
    if not arr1: return True
    # 文字列などに変換して検索するテクニック（要素の型に注意が必要）
    # Pythonではリストの部分一致判定は自前でやる必要があるため、少し工夫
    n = len(arr1)
    double_arr = arr1 + arr1
    for i in range(n):
        if double_arr[i:i+n] == arr2:
            return True
    return False
```

---

## 4. Constellation Mapper
座標リストから指定サイズのグリッド状の星空マップを作成する問題。

### 解答（内包表記の一行解法）
```python
def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:
    S = set(stars) # 検索をO(1)にする
    return ["".join("*" if (r, c) in S else "." for c in range(size)) for r in range(size)]
```

### 解説
指定された座標を `set` に変換することで、「その座標に星があるか？」というチェックを高速化します。あとは `size` 回の二重ループ（内包表記）でグリッドを作ります。

### 別解（標準的なforループ）
初心者に優しく、副作用を気にせず拡張しやすい書き方。
```python
def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:
    grid = []
    star_set = set(stars)
    for r in range(size):
        row = []
        for c in range(size):
            if (r, c) in star_set:
                row.append("*")
            else:
                row.append(".")
        grid.append("".join(row))
    return grid
```

---

## 5. List Intersection Finder
複数リストの積集合（すべてに含まれる要素）を抽出してソートする問題。

### 解答（Setを使った最速解法）
```python
def list_intersection_finder(lists: list[list[int]]) -> list[int]:
    if not lists or not all(lists): return []
    return sorted(set(lists[0]).intersection(*lists))
```

### 解説
Pythonの組み込み機能である `set.intersection()` は、可変長引数（`*lists`）を受け取ることができます。これを利用すると、C言語レベルで最適化された高速な積集合計算が行われます。

### 別解（Counterを使った解法）
もし `set` が使えない縛りがある場合は、カウントを使います。
```python
from collections import Counter

def list_intersection_finder(lists: list[list[int]]) -> list[int]:
    if not lists or not all(lists): return []
    
    # 各リスト内の重複を排除してからカウント
    counter = Counter()
    for lst in lists:
        counter.update(set(lst))
        
    num_lists = len(lists)
    return sorted([num for num, count in counter.items() if count == num_lists])
```

---

## 6. Merge Sorted List
複数のソート済みリストを1つのソート済みリストにマージする問題。

### 解答（フラット化 + ソート）
```python
def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    return sorted(x for l in lists for x in l)
```

### 解説
二重の内包表記 `x for l in lists for x in l` は、2次元リストを1次元に平坦化する定番の書き方です。それに `sorted()` をかけるだけで要件を満たせます。

### 別解（heapq.merge を使ったメモリ効率最強版）
すでに各リストがソート済みであることを最大限に活かすなら、Python標準ライブラリの `heapq.merge` が最適です。これはメモリを節約しながら $O(N \log K)$ （Nは全要素数、Kはリスト数）でマージします。
```python
import heapq

def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    # heapq.mergeはイテレータを返すのでリスト化する
    return list(heapq.merge(*lists))
```

---

## 7. Sliding Window Maximum
スライディングウィンドウ内の最大値を順次取得する問題。

### 解答（スライス + maxのシンプル版）
```python
def sliding_window_maximium(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0: return []
    return [max(nums[i:i+k]) for i in range(len(nums) - k + 1)]
```

### 解説
可読性と短さを極限まで高めたアプローチです。実用上はこれでも動きますが、計算量は $O(N \times K)$ となるため、巨大な配列だと遅くなります。

### 別解（Dequeを使った $O(N)$ の最強版）
アルゴリズム面で高い評価を得るためには、単調減少キュー（Monotonic Queue）を使います。ウィンドウ内の「最大値の候補」のみをインデックスで保持するため計算量は $O(N)$ になります。
```python
from collections import deque

def sliding_window_maximium(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0: return []
    
    dq = deque()
    res = []
    
    for i in range(len(nums)):
        # ウィンドウの範囲外になった古いインデックスを削除
        if dq and dq[0] < i - k + 1:
            dq.popleft()
            
        # これから追加する値よりも小さい要素は、今後絶対に最大値にならないので削除
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
            
        dq.append(i)
        
        # ウィンドウのサイズがkに達したら結果に追加
        if i >= k - 1:
            res.append(nums[dq[0]])
            
    return res
```
