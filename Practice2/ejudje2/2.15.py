# 1. Ask how many names there are
n = int(input())

# 2. Create an empty set to store unique names
unique_names = set()

# 3. Loop exactly 'n' times to get each name
for i in range(n):
    name = input()
    unique_names.add(name)

# 4. Print the total count of unique names
print(len(unique_names))