import re
text = "ab abb abbb abbbbbbbbbbbb"
pattern = r"ab{2,3}"
matches = re.findall(pattern, text)
print(matches)