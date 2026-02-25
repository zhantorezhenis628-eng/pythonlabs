












n=int(input())
counts={}
for i in range(n):
    phone = input()
    if phone in counts:
        counts[phone] += 1
    else:
        counts[phone] = 1
result = 0
for phone in counts:
    if counts[phone] == 3:
        result+=1

print(result)