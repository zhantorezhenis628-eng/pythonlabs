from datetime import datetime, timedelta
now = datetime.now()
without_miliseconds = now.replace(microsecond=0)
print("Original:", now)
print("Without miliseconds:", without_miliseconds)




from datetime import datetime, timedelta
now = datetime.now()
without_miliseconds = now.replace(microsecond=0)
print(now)
print(without_miliseconds)
tomorrow = datetime.now().date()+timedelta(days=1)
yesterday = datetime.now().date()-timedelta(days=1)
print(tomorrow)
print(yesterday)
fivedaysago = datetime.now().date()-timedelta(days=5)
print(fivedaysago)