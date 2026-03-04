import re
text = "a123b axxxxb ab cb"
pattern = r"a.*b"
matches = re.findall(pattern, text)
print(matches)
