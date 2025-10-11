def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
         if n % i == 0:
             return False
    return True

print(is_prime(12))     
print(is_prime(16))     
print(is_prime(17))     

# Time Complexity : O((log n)^6+e)
# Space Complexity: O(log n)