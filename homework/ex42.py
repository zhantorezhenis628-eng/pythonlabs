def squares(a, n):
    for i in range(a, n + 1):
        yield i ** 2

a, n = map(int, input().split())

for num in squares(a, n):
    print(num)