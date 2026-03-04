class Counter:
    def __init__(self, max_value):
        self.max = max_value
        self.current = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.max:
            self.current +=1
            return self.current
        else:
            raise StopIteration
    
counter = Counter(3)
for nim in counter:
    print(nim)

