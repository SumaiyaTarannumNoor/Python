def insertion_sort(arr):
    for i in range (1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key <arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

arr = [9, 16, 11, 14, 12]
sorted_arr = insertion_sort(arr)
print(f"Insertion Sort: {sorted_arr}")        

"""
Time Complexity: 
Best Case: O(n)
Worst Case: O(n^2)

Space Complexity: O(1)
"""