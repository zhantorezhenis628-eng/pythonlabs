from datetime import datetime, timedelta
now = datetime.now()
without_miliseconds = now.replace(microsecond=0)
print("Original:", now)
print("Without miliseconds:", without_miliseconds)