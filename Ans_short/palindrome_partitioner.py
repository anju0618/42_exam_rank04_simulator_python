def palindrome_partitioner(s: str) -> int:
    if not s or s == s[::-1]:
        return 0
    dp = [i - 1 for i in range(len(s) + 1)]
    for i in range(1, len(s) + 1):
        for j in range(i):
            if s[j:i] == s[j:i][::-1]:
                dp[i] = min(dp[i], dp[j] + 1)
    return dp[-1]
