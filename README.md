# Exam Rank 04 - Python Solutions & Explanations

このリポジトリは、Exam Rank 04 の各問題に対するPythonでの解答、詳細な解説、および別解（よりシンプルだが低速なアプローチなど）をまとめたものです。解答は3段階のフォルダに分かれています。

- **`Ans/`**: 本番moulinetteの制約（禁止built-inなど）を守った上で、最速かつ暗記しやすいバランスの良い解法。
- **`Ans_normal/`**: 同じく制約は守りつつ、読みやすさ・分かりやすさを優先した解法（変数名や処理を明示的に）。
- **`Ans_short/`**: 制約を無視して良いなら最短で書ける解法。1行で書けて理解確認や別環境での練習には便利ですが、`merge_sorted_list` のように**本番では使えないもの（`sorted()`使用など）が含まれる**ので注意してください。

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
入次数（in-degree）0のパッケージを「波（frontier）」としてまとめて取り出し、波の中はアルファベット順に処理します。ある波を処理し終えてから初めて次の波（新たに入次数0になったパッケージ）に進むので、後の波のパッケージが先の波のパッケージを追い越すことがありません。計算量は頂点数・辺数に対して `O(V log V + E)`（各波でのソートを含む）で、処理できるパッケージが尽きた時点で全パッケージを消化できていなければ循環依存として `[]` を返します。他の実装（`min()` 逐次選択や単一の優先度付きキュー）はどちらも波の概念を持たないため、上記のタイブレーク問題を起こします。

---

## 2. Palindrome Partitioner
文字列を回文のみのサブ文字列に分割するための、最小カット数を求める問題。

### 解答（回文判定テーブル + DPによる `O(n²)` 解法）
```python
def palindrome_partitioner(s: str) -> int:
    n = len(s)
    if n <= 1:
        return 0

    # is_pal[i][j]: s[i:j+1] が回文かどうかをO(1)で引けるように事前計算
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = s[i] == s[j] and (length == 2 or is_pal[i + 1][j - 1])

    dp = [0] * n
    for i in range(n):
        if is_pal[0][i]:
            continue  # 先頭からi文字目までがすでに回文ならカット不要
        # j=iは常にis_pal[i][i]=Trueなので、この内包表記が空になることはない
        dp[i] = min(dp[j - 1] + 1 for j in range(1, i + 1) if is_pal[j][i])
    return dp[-1]
```

### 解説
まず `is_pal[i][j]` に「`s[i]` から `s[j]` までが回文かどうか」を短い部分文字列から順にボトムアップで埋めていきます（`is_pal[i][j]` は `s[i] == s[j]` かつ内側 `is_pal[i+1][j-1]` が回文であれば真）。これにより、以降のDPで毎回スライス・反転して回文判定する必要がなくなり、`O(1)` で判定できます。次に `dp[i]` に「先頭から `i` 文字目までの最小カット数」を記録し、`s[j:i+1]` が回文であれば `dp[i]` を `dp[j-1] + 1` で更新できます。

事前計算テーブルを使わずに毎回 `s[j:i] == s[j:i][::-1]` でスライス・反転して判定すると、判定1回が `O(n)` かかるため全体で `O(n³)` になってしまいます。テーブル化することで判定が `O(1)` になり、全体の計算量が真の `O(n²)`（時間・空間とも）に落ちるのがこの解法のポイントです。

### 別解1（毎回スライス比較するシンプルなDP、`O(n³)`）
書きやすさを優先するならこちらでも正解は得られます。
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

### 別解2（メモ化再帰、`O(n³)` 相当 + 文字列ハッシュのオーバーヘッド）
トップダウンのほうが直感的な場合はこちら。ただし `lru_cache` が部分文字列そのものをキーにするため、ハッシュ計算とスライス生成のオーバーヘッドが大きく、実用上は最も遅くなりがちです。
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

### 解答（連結配列アプローチ）
`arr1` を2つ繋げたもの（`arr1 + arr1`）の中に、`arr2` が部分配列として含まれていれば、それは回転であると言えます。
```python
def array_rotation_detector(arr1: list, arr2: list) -> bool:
    if len(arr1) != len(arr2):
        return False
    if not arr1:
        return True
    n = len(arr1)
    doubled = arr1 + arr1  # 連結を1回だけ行い、部分列としてarr2を探す
    return any(doubled[i:i + n] == arr2 for i in range(n))
```

### 解説
配列の連結（`arr1 + arr1`）を1回だけ行い、そこから長さ `n` のウィンドウを `n` 通り切り出して `arr2` と比較します。判定自体はどちらの解法でも最悪 `O(n²)`（比較 `n` 回 × 各比較 `O(n)`）ですが、下記の別解のように毎回 `arr1[i:] + arr1[:i]` で新しいリストを作り直すのに比べて、連結を1回にまとめている分メモリ確保の回数が少なく、意図も読み取りやすくなっています。

> 補足: 要素の型が固定でハッシュ可能なら、文字列に変換して `in` 演算子（CPythonの高速な部分文字列探索）に載せることで平均 `O(n)` まで縮められますが、要素の `repr` 表現が衝突しないことを保証する必要があり、汎用性とのトレードオフになるためここでは採用していません。

### 別解（毎回スライスして比較するシンプルな解法）
```python
def array_rotation_detector(arr1: list, arr2: list) -> bool:
    if len(arr1) != len(arr2): return False
    if not arr1: return True
    return any(arr1[i:] + arr1[:i] == arr2 for i in range(len(arr1)))
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
指定された座標を `set` に変換することで、「その座標に星があるか？」というチェックを `O(1)` に高速化します。あとは `size` 回の二重ループ（内包表記）でグリッドを作るので、全体の計算量は `O(size² + len(stars))` となり、これ以上の改善余地はありません。

### 別解（標準的なforループ）
初心者に優しく、副作用を気にせず拡張しやすい書き方。計算量は解答と同じです。
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
Pythonの組み込み機能である `set.intersection()` は、可変長引数（`*lists`）を受け取ることができます。これを利用すると、C言語レベルで最適化された積集合計算が行われるため、Python側でループを書くよりも高速です。

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

> **注意（禁止built-in）**: 本番のmoulinetteでは `sorted()` / `.sort()` / `heapq.merge()` が**禁止**されており、手動でマージアルゴリズムを実装する必要があります（`questions/level2/py_merge_sorted_list` に明記）。`Ans/` と `Ans_normal/` はこの制約を満たす手動実装、`Ans_short/` はあえて制約を無視した最短版です。

### おすすめ暗記版（`Ans_normal`：ペアワイズマージ、シンプルで確実）
本番で緊張していても書ける・思い出せることを優先するなら、まずはこちらを覚えるのがおすすめです。
```python
def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    def merge_two(a, b):
        merged, i, j = [], 0, 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                merged.append(a[i]); i += 1
            else:
                merged.append(b[j]); j += 1
        merged.extend(a[i:])
        merged.extend(b[j:])
        return merged

    result = []
    for lst in lists:
        result = merge_two(result, lst)
    return result
```

**考え方**: 2つのソート済みリストをマージする定番`merge_two`（両方の先頭を比較して小さい方を取る、片方が尽きたら残りを丸ごと`extend`）を、リストを1つずつ`result`に統合しながら繰り返し使うだけです。`sorted`も`heapq`も一切使わないので確実に制約を満たせます。空リストが混ざっても`merge_two`が自然に処理してくれます。

計算量は`O(N×K)`（下記のヒープ版の`O(N log K)`より劣る）ですが、シンプルさと再現性を優先するならこちらで十分です。

### 発展版（`Ans`：自前の二分ヒープによる `O(N log K)`）
時間に余裕があれば、もう少し速い自前ヒープ版も見ておくと安心です。`push`/`pop`を手書きするので長めですが、典型的な二分ヒープの型そのものなので、一度書き方を覚えておくと他の問題にも応用できます。
```python
def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    heap = []

    def push(item):
        heap.append(item)
        i = len(heap) - 1
        while i > 0:
            parent = (i - 1) // 2
            if heap[parent] <= heap[i]:
                break
            heap[parent], heap[i] = heap[i], heap[parent]
            i = parent

    def pop():
        top = heap[0]
        last = heap.pop()
        if heap:
            heap[0] = last
            i, n = 0, len(heap)
            while True:
                l, r, smallest = 2 * i + 1, 2 * i + 2, i
                if l < n and heap[l] < heap[smallest]:
                    smallest = l
                if r < n and heap[r] < heap[smallest]:
                    smallest = r
                if smallest == i:
                    break
                heap[i], heap[smallest] = heap[smallest], heap[i]
                i = smallest
        return top

    for li, lst in enumerate(lists):
        if lst:
            push((lst[0], li, 0))

    result = []
    while heap:
        value, li, idx = pop()
        result.append(value)
        if idx + 1 < len(lists[li]):
            push((lists[li][idx + 1], li, idx + 1))
    return result
```

**解説**: `heapq` モジュール自体は禁止されているので、push/popの二分ヒープ操作を自前で書きます。各リストの「今見えている先頭要素」だけをヒープに積み、popした要素の次の要素を代わりに積み直すことで、全体を`O(N log K)`（`N`は全要素数、`K`はリスト数）でマージできます。

### 別解（`Ans_short`、制約無視の最短版・**本番では使用不可**）
```python
def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    return sorted(x for l in lists for x in l)
```
1行で書けますが `sorted()` を使っているため、本番moulinetteの禁止built-in制約に違反します。理解確認や別環境での練習用と割り切ってください。

---

## 7. Sliding Window Maximum
スライディングウィンドウ内の最大値を順次取得する問題。

### 解答（Dequeを使った `O(N)` の最強版）
単調減少キュー（Monotonic Queue）を使い、ウィンドウ内の「最大値の候補」のみをインデックスで保持することで計算量を `O(N)` に抑えます。
```python
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
```

### 解説
各要素は高々1回ずつ `dq` に追加され、高々1回ずつ取り除かれる（`popleft` または `pop`）ため、ループ全体では償却 `O(N)` で動作します。キューの先頭 `dq[0]` は常にウィンドウ内の最大値のインデックスになるように保たれます。

### 別解（スライス + maxのシンプル版、`O(N × K)`）
可読性と短さを極限まで高めたアプローチです。実用上はこれでも正しく動きますが、ウィンドウの数 `N - K + 1` それぞれで `max()` を計算し直すため、巨大な配列だと遅くなります。
```python
def sliding_window_maximium(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0: return []
    return [max(nums[i:i+k]) for i in range(len(nums) - k + 1)]
```

---

## Simulator Usage / シミュレーターの使い方

### English

Run the simulator from the repo root:

```sh
python3 simulator/exam_simulator.py
```

On startup it asks you to pick a **mode**, which controls how `next` picks the next problem:

| # | Mode | Behavior |
|---|------|----------|
| 1 | `sequential` | Walks through every problem in a fixed order (level1 → level2 → level3, alphabetical within a level), wrapping back to the start at the end. Best for reviewing every problem in order, like a study pass. |
| 2 | `exam` (default) | Mimics the real exam: draws one problem at random, without repeats, from a shuffled bag that refills once every problem has come up. |
| 3 | `random` | Fully independent random pick each time — the same problem can come up twice in a row. Good for quick, unpredictable drilling. |

Press Enter with no input to accept the default (`exam`).

Available commands once running:

- `ls` — list all problems by level
- `cat <name>` — view a problem's brief and its stub file's path
- `grademe` — run the tests against your current exercise's stub file (under `simulator/workspace/`)
- `grade <name>` — run the tests against any specific problem's stub file
- `next` — move on to another exercise, following the active mode
- `mode` — show the current mode; `mode <sequential|exam|random>` switches it without restarting
- `help` — show the command list
- `exit` / `quit` — leave the simulator

Solve each exercise by editing its stub file under `simulator/workspace/level<N>/<name>.py`, then run `grademe` to check it.

### 日本語

リポジトリのルートから実行します。

```sh
python3 simulator/exam_simulator.py
```

起動すると **モード**選択を求められます。これは `next` コマンドで次にどの問題が出るかを決めます。

| # | モード | 動作 |
|---|--------|------|
| 1 | `sequential`（順番モード） | 全問題を固定順（level1→level2→level3、レベル内はアルファベット順）で1問ずつ出題し、最後まで行くと最初に戻ります。全問を順番に復習したいときに最適です。 |
| 2 | `exam`（本番モード・デフォルト） | 本番の試験を模して、シャッフルした問題の袋から重複なく1問ずつランダムに出題します。全問出し切ると袋が再シャッフルされます。 |
| 3 | `random`（ランダムモード） | 毎回完全に独立した抽選を行うので、同じ問題が連続で出ることもあります。短時間でランダムに解く練習向けです。 |

何も入力せずEnterを押すとデフォルト（`exam`）が選ばれます。

起動後に使えるコマンド:

- `ls` — レベルごとに全問題を一覧表示
- `cat <name>` — 問題文とスタブファイルのパスを表示
- `grademe` — 今出題されている問題のスタブファイル（`simulator/workspace/`配下）を採点
- `grade <name>` — 指定した問題のスタブファイルを採点
- `next` — 現在のモードに従って次の問題に進む
- `mode` — 現在のモードを表示。`mode <sequential|exam|random>` で再起動せずにモード変更
- `help` — コマンド一覧を表示
- `exit` / `quit` — シミュレーターを終了

各問題は `simulator/workspace/level<N>/<name>.py` のスタブファイルを編集して解答し、`grademe` で採点してください。
```
