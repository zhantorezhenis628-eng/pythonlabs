n=int(input())
mylist=list(map(int, input().split()))
mylist.sort(reverse = True)


for i in mylist:
    print(i, end=" ")
