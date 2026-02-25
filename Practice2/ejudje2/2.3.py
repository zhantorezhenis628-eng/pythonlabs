n = input() # Read the first line (not actually needed for this logic)
numbers = input().split() # Split the line into a list

total = 0
for x in numbers:
    total = total + int(x)

print(total)