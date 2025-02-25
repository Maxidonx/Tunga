#finding the maximum number in an array
'''This is a simple way to find the maximum number in an array, but it is not the most efficient way.'''
def find_max(arr):
    return max(arr)

print(find_max([3, 1, 7, 4, 9, 2, 11]))


'''This is a more efficient way to find the maximum number in an array.'''
# def find_max(arr):
#     max_num = arr[0]
#     for num in arr:
#         if num > max_num:
#             max_num = num
#     return max_num

# print(find_max([3, 1, 7, 4, 9, 2]))