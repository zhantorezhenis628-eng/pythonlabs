import re
text = "Hello, world. Python is hard"
pattern = r"[ ,.]"
result = re.sub(pattern, ":", text)
print(result)
