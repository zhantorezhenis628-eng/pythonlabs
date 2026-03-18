import shutil
from pathlib import Path

src = Path("exe.txt")
backup = Path("backup_sample.txt")

# Copy file
shutil.copy(src, backup)
print("File copied.")


# Delete file safely
if backup.exists():
    backup.unlink()
    print("Backup file deleted.")
else:
    print("File does not exist.")