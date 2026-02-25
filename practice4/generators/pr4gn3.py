def divisible_by_3_and_4(n):
    for i in range(n+1):
        if i % 12 == 0:
            yield i
for number in divisible_by_3_and_4(100):
    print(number)