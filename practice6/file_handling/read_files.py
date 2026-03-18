from pathlib import Path
file_path = path =("exe.txt")

# Read entire file

with open(file_path, "r") as f:
    content = f.read()
    print("Full content:\n", content)

# Read line by line 

with open(file_path, "r") as f:
    print("Line by line:")
    for line in f:
        print(line.strip())
    
# Read lines into list

with open(file_path, "r") as f:
    lines = f.readlines()
    print("Lines list:", lines)
    