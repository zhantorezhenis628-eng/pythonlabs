
num = int(input("Enter a number: "))

# A prime number must be greater than 1
if num > 1:
    # Check every number from 2 up to num
    for i in range(2, num):
        if (num % i) == 0:
            print(num, "is NOT a prime number")
            break
    else:
        # If the loop finished without finding a factor
        print(num, "is a prime number")
else:
    print(num, "is NOT a prime number")