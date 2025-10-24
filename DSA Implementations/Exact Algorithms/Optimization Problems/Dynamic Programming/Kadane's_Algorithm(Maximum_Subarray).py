def max_subarray(arr):
    max_current = max_global = arr[0]

    for num in arr[1:]:
        max_current = max(num, max_current + num)
        if max_current > max_global:
            max_global = max_current

    return max_global

arr = [14, -20, 21, 22, 20, -14, -16, 11, 9, 6, 29, -19]
max_sum = max_subarray(arr)
print(f"Maximum Subarray Sum (Kadane's): {max_sum}")        

"""
Time Complexity: O(n)

Space Complexity: O(1) (Constant extra space)
"""