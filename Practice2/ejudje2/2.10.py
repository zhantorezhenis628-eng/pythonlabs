import re
n = input()
res = re.match("Hello", n)
if res:
    print("Yes")
else:
    print("No")
