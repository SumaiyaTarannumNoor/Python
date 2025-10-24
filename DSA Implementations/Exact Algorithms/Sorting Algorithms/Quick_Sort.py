def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

arr = [9, 16, 11, 14, 12]
sorted_arr = quick_sort(arr)
print(f"Insertion Sort: {sorted_arr}")        

"""
Time Complexity: 
Best/Average Case: O(n log n)
Worst Case: O(n^2) (If pivot is poorly chosen, e.g., smallest/largest element)

Space Complexity: O(log n) (recursion stack)
"""     