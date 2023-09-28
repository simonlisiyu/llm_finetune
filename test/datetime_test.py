from datetime import datetime

current_datetime = datetime.now()
print(current_datetime)


current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
print(formatted_datetime)
