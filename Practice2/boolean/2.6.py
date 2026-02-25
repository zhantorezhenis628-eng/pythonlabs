

a = int(input())
numbers = input().split()

# Start with a very small number or the first number in the list
biggest = int(numbers[0])

for x in numbers:
    current_number = int(x) # Convert string to integer
    if current_number > biggest:
        biggest = current_number

print(biggest)