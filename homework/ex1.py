n = input()
count = 0

for x in n:            # Iterate through the ACTUAL digits (characters)
    if int(x) % 2 == 0: # Check if the digit itself is even
        count += 1

if count == len(n):    # After the loop, check if every digit was even
    print("Valid")
else:
    print("Not valid")