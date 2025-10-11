def knapsack(values, weights, capacity):
    n = len(values)
    dp =[[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i-1][w-weights[i-1]])
            else:
                dp[i][w] = dp[i - 1][w] 
    return dp[n][capacity]

values = [60, 100, 160]
weights = [10, 30, 30]
capacity = 60 
print(knapsack(values, weights, capacity))  

# Time Complexity: O(nW)
# Space Complexity: O(nW)