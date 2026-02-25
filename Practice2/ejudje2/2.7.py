a = int(input())

for i in range(a): # Using a high range
    result = 2**i      # 2 to the power of i
    if result <= a:
        print(result, end=" ")
    else:
        break          # Stop the loop once we pass the limit

