def squares_up_to(n):
    for i in range(n+1):
        yield i ** 2
for value in squares_up_to(5):
    print(value)


def counter(n):
    for i in range(n+1):
        yield i
for x in counter(5):
    print(x)


def countdown(n):
    while n>=0:
        yield n
        n-=1
for x in countdown(10):
    print(x)


def divisible(n):
    for i in range(n+1):
        if i % 9 ==0:
            yield i
n = int(input())
result = ",".join(str(num) for num in divisible(n))
print(result)
for x in divisible(89):
    print(x)

