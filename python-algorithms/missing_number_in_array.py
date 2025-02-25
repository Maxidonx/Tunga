def missing_number(arr, n):
    total = n * (n+1)//2
    return total - sum(arr)

arr = [1, 2, 3, 4, 5, 7, 8]
print(missing_number(arr, 8)) # 9
