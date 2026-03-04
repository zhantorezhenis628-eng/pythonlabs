import re
text = "ab abb abbbb a ac"
pattern = r"ab*"
matches = re.findall(pattern, text)
print(matches)
