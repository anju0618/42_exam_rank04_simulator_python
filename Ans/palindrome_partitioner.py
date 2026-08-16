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
