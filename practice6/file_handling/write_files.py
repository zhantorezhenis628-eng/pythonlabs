from pathlib import Path
file_path = Path("exe.txt")

#Write to file (overwrites)
with open(file_path, "w") as f:
    f.write("Hello, this is line 1\n")
    f.write("Hello, this is line 2\n")

# Append to file
with open(file_path, "a") as f:
    f.write("This is an appended line\n")
print("File written and appended successfully")
    
    