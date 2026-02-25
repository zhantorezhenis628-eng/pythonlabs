a = int(input())
numbers = [int(x) for x in input().split()]

# Start with a very small number or the first number in the list
pos = 0

for i in range(1, a):
    if numbers[i] > numbers[pos]:
        pos = i

print(pos+1)

