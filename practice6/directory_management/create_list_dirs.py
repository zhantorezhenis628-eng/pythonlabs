import os
# Create directory
os.mkdir("test_dir")

# Create nested directories
os.makedirs("parent/child/grandchild, exist_ok=True")

#Current working directory
print("Current directory:", os.getcwd())

#List files
print("Directory contents:", os.listdir())

# Remove directory
os.rmdir("test_dir")
