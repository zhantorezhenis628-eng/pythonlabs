from datetime import datetime, timedelta
current_date = datetime.now()
new_date = current_date - timedelta(days=5)
print("Current date:", current_date)
print("Five days ago:", new_date)