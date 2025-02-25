# finding duplicate numbers in an array
'''This is a simple way to find duplicate numbers in an array, but it is not the most efficient way.'''
def find_duplicate(arr):
    seen = set()
    for num in arr:
        if num in seen:
            return num
        seen.add(num)
    return None

print(find_duplicate([3, 1, 3, 4, 2])) 

