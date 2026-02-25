def numbers(*args):
    total = 0
    for num in args:
        total += num
    return total
print(numbers(1,2,3))