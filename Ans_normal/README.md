# Ans_normal 完全解説

`Ans_normal/` の解答だけを対象に、**アルゴリズムを完璧に理解する**ための解説をまとめたファイルです。

`Ans/`（最速・暗記重視）や `Ans_short/`（制約無視の最短版）とは違い、`Ans_normal/` は **`set` や `sorted()` などの「魔法の1行」に頼らず、処理そのものを手で書き下した版** です。「なぜそのコードで答えが出るのか」を追いやすいので、アルゴリズムの理屈を体に入れたい今のフェーズに向いています。理屈が入ったら、速い版（`Ans/`）を暗記する、という順番がおすすめです。

---

## 1. Constellation Mapper（Level 1）

> 座標リストから size×size の星空グリッドを作る。範囲外座標・重複座標は無視する。

```python
def constellation_mapper(stars: list[tuple[int, int]], size: int) -> list[str]:
    grid = []
    for r in range(size):
        row = []
        for c in range(size):
            row.append(".")
        grid.append(row)

    for r, c in stars:
        if 0 <= r < size and 0 <= c < size:
            grid[r][c] = "*"

    result = []
    for row in grid:
        result.append("".join(row))
    return result
```

### アルゴリズムの流れ

1. **空のグリッドを先に作る**: `size` 行 × `size` 列、全マス `"."` の2次元リスト（リストのリスト）を二重ループで組み立てる。この時点でどの座標も星なしの状態。
2. **星を1つずつ置いていく**: `stars` を1個ずつ取り出し、`0 <= r < size and 0 <= c < size` で「グリッドの中に収まっているか」だけを確認する。収まっていれば `grid[r][c] = "*"` で直接上書きする。
   - 範囲外の座標は条件式が `False` になるので、何もせずスキップされる → 「範囲外は無視」を専用の分岐なしで満たしている。
   - 同じ座標が複数回来ても、同じマスに `"*"` を何度上書きしても結果は変わらない → 「重複は無視」も自動的に満たされる。
3. **文字列化**: `grid` は `list[list[str]]`（1文字ずつのリストの集まり）なので、各行を `"".join(row)` で1本の文字列に変換し、`result` に集める。

### 計算量

- グリッド生成: `O(size²)`
- 星の配置: `O(n)`（`n = len(stars)`、各座標の判定・書き込みは `O(1)`）
- 文字列化: `O(size²)`
- 合計 `O(size² + n)`、空間も `O(size²)`

### トレース例

`stars=[(0,0),(1,1)], size=2`
- grid初期化 → `[['.','.'], ['.','.']]`
- `(0,0)` → 範囲内 → `grid[0][0]="*"` → `[['*','.'], ['.','.']]`
- `(1,1)` → 範囲内 → `grid[1][1]="*"` → `[['*','.'], ['.','*']]`
- join → `["*.", ".*"]`

---

## 2. List Intersection Finder（Level 1）

> 複数リストすべてに共通する要素を、重複なく昇順で返す。

```python
def list_intersection_finder(lists: list[list[int]]) -> list[int]:
    if not lists:
        return []
    for lst in lists:
        if not lst:
            return []

    result = []
    for value in lists[0]:
        if value in result:
            continue  # すでに結果に入っている値は重複させない
        in_all = True
        for other in lists[1:]:
            if value not in other:
                in_all = False
                break
        if in_all:
            result.append(value)

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result
```

### アルゴリズムの流れ

このコードは2つのパートに分かれる。**「積集合を求めるパート」**と**「手動で並び替えるパート」**。`set` も `sorted()` も使わず、両方を自力で書いている。

**パート1: 積集合を求める（`lists[0]` を基準にする）**
1. `lists` が空、または中に空リストが1つでもあれば、その時点で積集合は空なので `[]` を返す（要件「いずれか1つでも空なら空」をここで満たす）。
2. 基準となる `lists[0]` を1個ずつ舐める。
3. すでに `result` に入っている値なら `continue` でスキップ（＝結果の重複を防ぐ。まだ `set` を使っていないので `value in result` という線形探索で確認している）。
4. `lists[1:]`（基準以外の全リスト）それぞれについて `value not in other` を確認し、1つでも含まれていなければ `in_all = False` にして即 `break`（無駄なチェックを打ち切る）。
5. 全リストに含まれていた（`in_all` が最後まで `True`）場合だけ `result` に追加する。

**パート2: 挿入ソート（insertion sort）で `result` を昇順に並べる**
6. `i` を `1` から `len(result)-1` まで動かし、「これから正しい位置に挿入する値」を `key = result[i]` として取り出す。
7. `j = i - 1` から左へ向かって、`result[j] > key` である限り、その値を1つ右にずらす（`result[j+1] = result[j]`）。これは「keyより大きい値をどんどん右にスライドさせて、keyの入る隙間を空けている」動き。
8. ループが止まった位置（`j+1`）に `key` を差し込む。
9. これを `i` を増やしながら繰り返すと、`result[0..i]` が常に昇順に保たれたまま最後まで進む＝挿入ソート。

### 計算量

- 積集合探索: 最悪 `O(len(lists[0]) × K × L)`（`K`=リスト数、`L`=各リストの平均長。`value in result` と `value not in other` がそれぞれ線形探索のため、`set` 版の `O(total)` より遅い）
- 挿入ソート: `O(m²)`（`m = len(result)`）
- `set` 版より理論上は遅いが、**「線形探索」と「挿入ソート」という基礎アルゴリズム2つを手で書ける**ことがこの版の価値。

### トレース例

`lists = [[1,2,3],[2,3,4],[2,3,5]]`
- 基準 `lists[0] = [1,2,3]`
- `value=1`: `other=[2,3,4]` に `1` がない → `in_all=False` → 追加しない
- `value=2`: `[2,3,4]` にある、`[2,3,5]` にもある → `in_all=True` → `result=[2]`
- `value=3`: 同様に両方にある → `result=[2,3]`
- 挿入ソート: すでに昇順なので並び替え不要 → `[2, 3]`

---

## 3. Array Rotation Detector（Level 1）

> `arr2` が `arr1` の回転（左右どちらか）になっているか判定する。

```python
def array_rotation_detector(arr1: list, arr2: list) -> bool:
    if len(arr1) != len(arr2):
        return False
    if not arr1:
        return True

    n = len(arr1)
    # arr1をずらす開始位置を1つずつ試して、arr2と完全一致するか調べる
    for start in range(n):
        match = True
        for i in range(n):
            if arr1[(start + i) % n] != arr2[i]:
                match = False
                break
        if match:
            return True
    return False
```

### アルゴリズムの流れ

`Ans/` 版が「`arr1 + arr1` を作って部分列を探す」方式だったのに対し、こちらは **配列を実際には連結せず、インデックス計算 `(start + i) % n` だけで「連結したのと同じ効果」を出す** アプローチ。

1. 長さが違えば即 `False`、両方空なら即 `True`（回転の判定をするまでもない自明ケースを先に処理）。
2. `start`（回転の開始位置の候補）を `0` から `n-1` まで全部試す。
3. その `start` について、`i` を `0` から `n-1` まで動かしながら `arr1[(start + i) % n]` と `arr2[i]` を比較する。
   - `% n`（剰余）を使うことで、`start + i` が `n` を超えたら自動的に配列の先頭に折り返る。これが「`arr1` を `start` だけ回転させたときの `i` 番目の要素」を、新しい配列を作らずに計算する方法。
4. 1つでも不一致があれば `match = False` にしてその `start` を諦め（`break`）、次の `start` へ。
5. 全要素が一致した `start` が見つかった時点で `True` を返す。全 `start` を試して1つも見つからなければ `False`。

### 計算量

- `n` 通りの `start` × 各 `n` 回の比較 = `O(n²)`
- `arr1 + arr1` のような配列コピーを作らないので、空間は `O(1)`（`Ans/` 版は `O(n)` の連結配列を作る分だけメモリを使う）

### トレース例

`arr1=[1,2,3], arr2=[3,1,2]`
- `start=0`: `i=0` → `arr1[0]=1` vs `arr2[0]=3` 不一致 → 打ち切り
- `start=1`: `i=0` → `arr1[1]=2` vs `arr2[0]=3` 不一致 → 打ち切り
- `start=2`: `i=0` → `arr1[2]=3` vs `arr2[0]=3` 一致 / `i=1` → `arr1[(2+1)%3]=arr1[0]=1` vs `arr2[1]=1` 一致 / `i=2` → `arr1[(2+2)%3]=arr1[1]=2` vs `arr2[2]=2` 一致 → `match=True` → `True` を返す

---

## 4. Merge Sorted List（Level 2）

> 複数のソート済みリストを1つのソート済みリストにマージする。**`sorted()` / `.sort()` / `heapq.merge()` は禁止**。

```python
def merge_sorted_list(lists: list[list[int]]) -> list[int]:
    def merge_two(a, b):
        # ソート済みの2つのリストを先頭から比べながら1つにまとめる
        merged = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                merged.append(a[i])
                i += 1
            else:
                merged.append(b[j])
                j += 1
        merged.extend(a[i:])
        merged.extend(b[j:])
        return merged

    result = []
    for lst in lists:
        result = merge_two(result, lst)
    return result
```

### アルゴリズムの流れ

**「2つのソート済みリストを1つにマージする」という部品（2ポインタ・マージ）を作り、それをリストの数だけ繰り返し適用する**、という2階建ての構造。

**内側: `merge_two(a, b)`（2ポインタ・マージ）**
1. `i`（`a` を指すポインタ）と `j`（`b` を指すポインタ）を `0` から始める。
2. `a[i]` と `b[j]` を比較し、小さい方（同値なら `a` 優先）を `merged` に追加して、そちら側のポインタだけ進める。
3. これを「`a` か `b` のどちらかを最後まで見終わる」まで繰り返す（`while i < len(a) and j < len(b)`）。
4. 片方が先に尽きた時点で、もう片方には「まだマージしていない残り」がまとまって残っている。両方ともソート済みなので、その残り全部を末尾にそのまま `extend` すればよい（`a[i:]` と `b[j:]` はどちらか一方しか要素を持たない）。

**外側: 全リストへの適用（畳み込み）**
5. `result = []` から始め、`lists` の中身を1つずつ `merge_two(result, lst)` に渡して、その返り値で `result` を更新していく。
6. これは「これまでマージし終えた分」と「次のリスト」を毎回マージし直している状態で、最終的に全リストがマージされた1本の配列になる。

`sorted()` も `heapq` も一切使っていないので、禁止built-in制約を確実に満たせる。

### 計算量

- `merge_two` 1回の呼び出しは `O(len(a) + len(b))`
- リストが `K` 個、要素数の合計が `N` のとき、全体で `O(N × K)`（最悪、毎回 `result` が伸びていくため）
- `Ans/` の自前ヒープ版は `O(N log K)` まで縮められるが、まずはこの版を確実に書けるようにするのが優先。

### トレース例

`lists=[[1,4,5],[1,3,4],[2,6]]`
- `result=[]` と `[1,4,5]` をマージ → `result=[1,4,5]`
- `[1,4,5]` と `[1,3,4]` をマージ:
  - `i,j=0,0`: `1<=1` → `1`追加、`i=1`
  - `4 vs 3`: `3`が小さい → `3`追加、`j=1`
  - `4 vs 4`: `4<=4` → `1`側の`4`追加、`i=2`
  - `5 vs 4`: `4`が小さい → `4`追加、`j=2`
  - `a`側(`[1,4,5]`)が尽きる前に`b`側(`[1,3,4]`)が尽きた(`j=2=len(b)`) → ループ終了
  - 残り: `a[i:]=a[2:]=[5]` を extend → `result=[1,3,4,4,5]`
- `[1,3,4,4,5]` と `[2,6]` をマージ → `[1,2,3,4,4,5,6]`

---

## 5. Palindrome Partitioner（Level 2）

> 文字列を回文だけの部分文字列に分割するための最小カット数を求める。

```python
def palindrome_partitioner(s: str) -> int:
    if not s:
        return 0

    n = len(s)
    dp = [i - 1 for i in range(n + 1)]  # dp[i]: 先頭i文字を回文だけに分けるのに必要な最小カット数
    for i in range(1, n + 1):
        for j in range(i):
            sub = s[j:i]
            if sub == sub[::-1]:  # s[j:i]が回文なら、そこで区切れる
                candidate = dp[j] + 1
                if candidate < dp[i]:
                    dp[i] = candidate
    return dp[-1]
```

### アルゴリズムの流れ（動的計画法 / DP）

`dp[i]` を **「先頭 `i` 文字（`s[0:i]`）を回文だけに分割するのに必要な最小カット数」** と定義する。これがこの問題のDPの核心。

1. **初期化**: `dp = [i - 1 for i in range(n + 1)]` により `dp[0] = -1, dp[1] = 0, dp[2] = 1, dp[3] = 2, ...` となる。これは「1文字ずつ全部バラバラに切った場合」の最悪値（`i` 文字を `i` 個の部分文字列に切るには `i-1` 回のカットが要る）を、最初にワースト値として仕込んでおく初期値。`dp[0] = -1` は「まだ何も無い状態」を表す番兵で、後述の漸化式が `j=0` のときに `dp[0]+1=0` と正しく計算できるようにするための工夫。
2. **二重ループでDPを埋める**: 外側 `i` は「今どこまでの文字列を確定させたいか」、内側 `j` は「その中でどこからどこまでを1つの回文ブロックとして切り出すか」の候補。
3. `sub = s[j:i]` を切り出し、`sub == sub[::-1]`（スライスを反転したものと元が同じ＝回文）かどうかをその場で判定する。
4. もし `s[j:i]` が回文なら、「`s[0:j]` は `dp[j]` 回のカットで既に回文分割済み」＋「`s[j:i]` をもう1ブロックとして追加する（+1カット）」で `s[0:i]` を分割できる、という意味で `candidate = dp[j] + 1`。
5. `candidate` が今の `dp[i]` より小さければ更新する（＝より少ないカット数の分割方法が見つかった）。
6. 全ての `i, j` の組を試し終えると、`dp[i]` には「`s[0:i]` を回文分割する最小カット数」の最終値が入っている。`dp[-1]`（＝`dp[n]`）が文字列全体に対する答え。

`Ans/` 版は事前に `is_pal[i][j]` テーブルを作って回文判定を `O(1)` にしていたが、この版はその場で `sub[::-1]` を作って比較するため、判定1回に `O(n)` かかり全体で `O(n³)` になる。その分、コードは短く「DPの本質」だけが見えやすい。

### 計算量

`O(n³)`（`i, j` の二重ループ `O(n²)` × 各ループでのスライス＆反転比較 `O(n)`）

### トレース例（`s = "aab"`, `n = 3`）

初期 `dp = [-1, 0, 1, 2]`

- `i=1`（`s[0:1]="a"`）: `j=0` → `sub="a"` 回文 → `candidate=dp[0]+1=0`。`0 < dp[1]=0` は偽なので更新なし。`dp=[-1,0,1,2]`
- `i=2`（`s[0:2]="aa"`）:
  - `j=0` → `sub="aa"` 回文 → `candidate=dp[0]+1=0`。`0 < dp[2]=1` → 更新 `dp[2]=0`
  - `j=1` → `sub="a"`（`s[1:2]`）回文 → `candidate=dp[1]+1=1`。`1 < dp[2]=0` は偽 → 更新なし
  - `dp=[-1,0,0,2]`
- `i=3`（`s[0:3]="aab"`）:
  - `j=0` → `sub="aab"` は回文でない → スキップ
  - `j=1` → `sub="ab"`（`s[1:3]`）は回文でない → スキップ
  - `j=2` → `sub="b"`（`s[2:3]`）回文 → `candidate=dp[2]+1=1`。`1 < dp[3]=2` → 更新 `dp[3]=1`
  - `dp=[-1,0,0,1]`

`dp[-1] = dp[3] = 1` → 正解の `1` と一致（`"aa" | "b"` の1カット）。

---

## 6. Sliding Window Maximum（Level 2）

> サイズ `k` の窓を左から右にスライドさせ、各位置での最大値を返す。

```python
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
```

### アルゴリズムの流れ

`Ans/` 版が単調 `deque` で `O(N)` まで最適化していたのに対し、こちらは **「各窓ごとに、その中身を実際に全部見て最大値を探す」総当たり** 版。仕組みがそのまま見えるので、まずはこの理解を先に固めるのが良い。

1. 窓の開始位置 `start` は `0` から `len(nums) - k` まで動く（＝窓の総数は `len(nums) - k + 1` 個、これは問題文の制約通り）。
2. 各 `start` について、窓の最初の要素 `nums[start]` をひとまず `window_max` の初期値にする。
3. 窓の残りの要素（`start+1` から `start+k-1` まで、ちょうど `k-1` 個）を1つずつ見て、`window_max` より大きければ更新する。
4. 窓を最後まで見終わったら、その `window_max` が「この窓での最大値」なので `result` に追加する。
5. 次の `start` に進み、また窓の中身を「ゼロから」全部見直す（前の窓の情報は再利用しない）。

「前の窓の情報を使い回さない」のがこの版の弱点（＝計算量が悪くなる原因）で、単調 `deque` 版はここを「候補だけを持ち越す」ことで解消している。まずはこの総当たり版で「窓の中の最大値を求める」という要求そのものを正しくコードにできるようにする。

### 計算量

各窓ごとに `k` 要素を見るので `O((len(nums) - k + 1) × k)`、大まかに `O(N × K)`。

### トレース例

`nums=[4,2,12,11,-5], k=2`
- `start=0`: `window_max=nums[0]=4`、`i=1`→`nums[1]=2`は`4`より小さいので更新なし → `4`
- `start=1`: `window_max=nums[1]=2`、`i=2`→`nums[2]=12>2` → `window_max=12` → `12`
- `start=2`: `window_max=nums[2]=12`、`i=3`→`nums[3]=11`は`12`より小さい → `12`
- `start=3`: `window_max=nums[3]=11`、`i=4`→`nums[4]=-5`は`11`より小さい → `11`
- 結果 `[4, 12, 12, 11]`

---

## 7. Package Dependency Resolver（Level 3）

> 依存関係を解決し、パッケージのインストール順序をトポロジカルソート（Kahnのアルゴリズム）で決定する。同時に選択可能な複数パッケージがある場合はアルファベット順。

```python
def package_dependency_resolver(packages: dict[str, list[str]]) -> list[str]:
    if not packages:
        return []

    # graph[dep]には「depに依存しているパッケージ」を、
    # in_degree[name]には「nameがまだ待っている依存の数」を入れる
    graph = {name: [] for name in packages}
    in_degree = {name: 0 for name in packages}
    for name, deps in packages.items():
        for dep in deps:
            if dep in packages:
                graph[dep].append(name)
                in_degree[name] += 1

    # 依存が1つもない(=今すぐインストールできる)パッケージを集める
    ready = []
    for name in packages:
        if in_degree[name] == 0:
            ready.append(name)
    ready.sort()

    result = []
    while ready:
        next_ready = []
        for name in ready:
            result.append(name)
            for neighbor in graph[name]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    next_ready.append(neighbor)
        next_ready.sort()
        ready = next_ready

    if len(result) != len(packages):
        return []  # 全部処理しきれなかった = 循環依存がある
    return result
```

### アルゴリズムの流れ（Kahnのアルゴリズム、波＝BFS層ごとの処理）

**準備: 逆向きグラフと入次数（in-degree）を作る**

1. `graph[dep]` に「`dep` を必要としている側（`dep` を待っている側）」のリストを持たせる。つまり通常の依存関係（`name` が `dep` に依存する）とは**逆向き**のグラフ。こうしておくと「`dep` がインストールされ終わったとき、誰の待ち人数を減らせるか」がすぐ分かる。
2. `in_degree[name]` は「`name` がまだ待っている残り依存数」。`name` の依存リスト `deps` を舐めて、`packages` に実在する依存（`if dep in packages`）だけをカウントする。存在しない依存は無視する要件をここで満たしている。

**Kahnのアルゴリズム本体（波＝frontierごとのBFS）**

3. 最初に「依存が0個＝今すぐインストール可能」なパッケージを `ready` に集め、`ready.sort()` でアルファベット順にする。これが「第1波」。
4. `while ready:` の間、**波ごとに丸ごと処理する**:
   - `ready`（今の波）の中身を **1つずつ順番に** `result` に積んでいく（すでにアルファベット順にソート済みなので、そのまま積むだけで順序が正しい）。
   - 各パッケージ `name` について、`graph[name]`（`name` を待っていた人たち）の `in_degree` を1つずつ減らす。誰かの `in_degree` が `0` になったら、その人は「次の波」の候補として `next_ready` に入れる。
   - 今の波を全部処理し終えてから、`next_ready.sort()` でアルファベット順にし、`ready = next_ready` として次のループへ進む。
5. **ここが最大のポイント**: 「波の中の全メンバーを処理し終える前に、次の波のメンバーが割り込んでくることは絶対にない」。もし `min()` で1つずつグローバルに拾う方式や、1本の優先度付きキューに全候補を混ぜて積む方式だと、後の波のパッケージ（アルファベット順が早いだけ）が先の波のパッケージを追い越してしまうことがある（`README.md` の「タイブレークの罠」参照）。この版は `ready` と `next_ready` を明確に分けることで、その追い越しを構造的に防いでいる。
6. ループが終わったとき（`ready` が空になったとき）、`result` の長さが `packages` 全体の数と一致していなければ、依存が0にならないまま残ったパッケージがある＝循環依存がある、ということなので `[]` を返す。

### 計算量

- グラフ構築: `O(V + E)`（`V`=パッケージ数、`E`=依存関係の総数）
- 各波での `sort()`: 波の合計サイズは最大 `V` なので、全体で最悪 `O(V log V)`
- 合計 `O(V log V + E)`

### トレース例

`{"web": [], "api": [], "frontend": ["web"], "backend": ["api"]}`

1. `in_degree`: `web=0, api=0, frontend=1(待ちwebを待つ), backend=1(apiを待つ)`
2. 第1波 `ready = ["api", "web"]`（両方0、アルファベット順）
3. `api` を `result` に追加 → `graph["api"] = ["backend"]` → `backend` の `in_degree` を `1→0` → `next_ready=["backend"]`
4. `web` を `result` に追加 → `graph["web"] = ["frontend"]` → `frontend` の `in_degree` を `1→0` → `next_ready=["backend","frontend"]`
5. 波1終了。`next_ready.sort()` → `["backend", "frontend"]`。これが第2波。
6. 第2波を処理 → `result` に `"backend"`, `"frontend"` の順で追加。
7. 最終結果: `["api", "web", "backend", "frontend"]` ✅ 期待値と一致。

（もし `backend` が `web` を追い越して先に処理されていたら `["api", "backend", "web", "frontend"]` になってしまい不正解。波を分けているからこそ、これが起きない。）

---

## まとめ: 覚えておくべき「型」

| 問題 | 型 |
|---|---|
| Constellation Mapper | グリッドを先に作り、境界判定しながら直接書き込む |
| List Intersection Finder | 基準リストを1周＋他リストを`in`で確認、その後に挿入ソート |
| Array Rotation Detector | `(start + i) % n` でインデックスを回して比較（連結配列を作らない） |
| Merge Sorted List | 2ポインタの`merge_two`を部品化し、リストの数だけ畳み込む |
| Palindrome Partitioner | `dp[i]` = 先頭i文字の最小カット数、`dp[0]=-1`の番兵から漸化式を回す |
| Sliding Window Maximum | 窓ごとに中身を総当たりで見て最大値を探す |
| Package Dependency Resolver | 入次数0のノードを「波」単位でまとめて処理するKahnのアルゴリズム |
