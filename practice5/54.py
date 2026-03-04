import re
text = "Hello world Test Python JAVA"
pattern = r"[A-Z][a-z]+"
matches = re.findall(pattern, text)
print(matches)
