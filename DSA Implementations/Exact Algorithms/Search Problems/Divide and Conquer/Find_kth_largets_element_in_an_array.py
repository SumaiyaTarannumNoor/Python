def kth_largest(nums, k):
    k_index = len(nums) - k

    def quickselect(left, right):
        pivot = nums[right]
        p = left 
        for i in range(left, right):
            if nums[i] <= pivot:
                nums[i], nums[p] = nums[p], nums[i]
                p += 1

        nums[p], nums[right] = nums[right], nums[p]

        if p == k_index:
            return nums[p]
        elif p < k_index:
            return quickselect(p + 1, right)
        else:        
            return quickselect(left, p-1)

    return quickselect(0, len(nums) - 1)


print(kth_largest([18, 8, 3, 2, 1, 5, 6, 12, 4, 7, 10, 14, 16, 17], 6))


# Best Case:
# Time Complexity: O(n)
# Space Complexity: O(log n)   # recursion stack

# Average Case:
# Time Complexity: O(n)
# Space Complexity: O(log n)   # recursion stack

# Worst Case:
# Time Complexity: O(n^2)
# Space Complexity: O(n)       # recursion stack