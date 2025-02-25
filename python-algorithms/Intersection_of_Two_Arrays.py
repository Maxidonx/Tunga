# Intersection of Two Arrays

def intersection_of_two_arrays(arr1, arr2):
    return list(set(arr1) & set(arr2)) 

print(intersection_of_two_arrays([1, 2, 3, 4, 1], [2, 3, 4, 7, 2])) # [2]
