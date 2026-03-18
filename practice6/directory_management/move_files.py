import shutil
from pathlib import Path

# Create directories
Path("source").mkdir(exist_ok=True)
Path("destination").mkdir(exist_ok=True)

# Create sample file
file = Path("source/exe.txt")
file.write_text("Moving this file")

# Move file
shutil.move(str(file), "destination/exe.txt")

print("File moved successfully")