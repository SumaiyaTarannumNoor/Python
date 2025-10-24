def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]


        merge_sort(left)
        merge_sort(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
   
    return arr

arr = [9, 16, 11, 14, 12]
sorted_arr = merge_sort(arr)
print(f"Merge Sort: {sorted_arr}")        

"""
Time Complexity: O(n log n) (Always)

Space Complexity: O(n) (Requires auxiliary space for merging.)
"""