from functools import reduce
numbers = [1, 2, 3, 4, 5]

squared = list(map(lambda x: x**2, numbers))
print("Squared:", squared)

evens = list(filter(lambda x: x%2==0, numbers))
print("Evens:", evens)

total = reduce(lambda x, y: x+y, numbers)
print("Sum:", total)

print("Lenght:", len(numbers))
print("Min:", min(numbers))
print("Max:", max(numbers))
print("Sorted desc:", sorted(numbers, reverse=True))