n=int(input())
mylist=list(map(int, input().split()))
squares=[]
for i in mylist:
    i = i**2
    squares.append(i)
print(*squares)