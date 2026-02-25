from datetime import datetime, timedelta
date1 = datetime(2025, 1, 1, 12, 0, 0)
date2 = datetime(2025, 1, 2, 12, 0, 0)
difference = date2 - date1
seconds = difference.total_seconds()
print("Difference in seconds:", seconds)