n = int(input())
arr = list(map(int, input().split()))

seen = set()

for num in arr:
    if num in seen:
        print("NO")
    else:
        print("YES")
        seen.add(num)
