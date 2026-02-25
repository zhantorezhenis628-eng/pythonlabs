n, l, r = map(int, input().split())
mylist = list(map(int, input().split()))
result = mylist[:l-1]+mylist[l-1:r][::-1]+mylist[r:]
print(*result)