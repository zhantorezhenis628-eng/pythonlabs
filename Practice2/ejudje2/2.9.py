n = int(input())
dataline = input().split()

# 1. Convert strings to integers manually
numbers = []
for item in dataline:
    numbers.append(int(item))

# 2. Find the targets
biggest = max(numbers)
smallest = min(numbers)

# 3. Print the result with logic
for x in numbers:
    if x == biggest:
        print(smallest, end=" ")
    else:
        print(x, end=" ")

