def greedy_coin_change(coins, amount):
    coins.sort(reverse=True)
    count = 0
    for coin in coins:
        while amount >= coin:
            amount -= coin
            count += 1
    return count

coins = [1, 2, 6, 10, 20, 60]
print(greedy_coin_change(coins, 66))  

# Time Complexity: O(n)
# Space Complexity: O(1)