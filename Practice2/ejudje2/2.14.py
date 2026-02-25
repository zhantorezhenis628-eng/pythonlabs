n = int(input())
mylist = list(map(int, input().split()))

# 1. Create a "Tally Sheet" (Dictionary)
counts = {}

for num in mylist:
    if num in counts:
        counts[num] += 1  # Add to existing tally
    else:
        counts[num] = 1   # Start new tally

# 2. Find the highest frequency
max_frequency = max(counts.values())

# 3. Find which numbers have that frequency
candidates = []
for num in counts:
    if counts[num] == max_frequency:
        candidates.append(num)

# 4. If there's a tie, pick the smallest number
print(min(candidates))