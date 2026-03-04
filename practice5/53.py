import re
text = "hello_world test_string Hello_world"
pattern = r"[a-z]+_[a-z]+"
matches = re.findall(pattern, text)
print(matches)
