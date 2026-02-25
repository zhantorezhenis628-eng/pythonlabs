n = input() # Read the first line (not actually needed for this logic)
numbers = input().split() # Split the line into a list
cnt = 0

for x in numbers:
    if int(x) > 0:
        cnt = cnt + 1
print(cnt)