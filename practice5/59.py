import re
text = "YelloWorldPython"
result = re.sub(r'([A-Z])', r' \1', text).strip()
print(result)