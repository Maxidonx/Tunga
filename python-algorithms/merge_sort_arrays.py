#  Merge Two Sorted Arrays

def merge_sorted_arrays(arr1, arr2):
    return sorted(arr1 + arr2)

print(merge_sorted_arrays([0, 5, 3, 2, 8], [4, 6, 9, 1, 7])) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]