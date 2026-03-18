names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

# enumerate()
for i, name in enumerate(names):
    print(f"{i}: {name}")

# zip()
for name, score in zip(names, scores):
    print(f"{name} scored {score}")

# Tupe conversion
num_str = "123"
num_int = int(num_str)
print(type(num_int), num_int)

#Combine zip + enumerate

for i, (name, score) in enumerate(zip(names, scores)):
    print(f"{i}: {name}  -> {score}")

