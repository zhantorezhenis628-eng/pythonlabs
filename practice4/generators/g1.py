def squares_up_to(n):
    for i in range(n+1):
        yield i ** 2
for value in squares_up_to(5):
    print(value)
