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
