import re
text = "HelloWotldPython"
result = re.findall(r'[A-Z][a-z]*', text)
print(result)