from datetime import datetime

timestamp = 1528797322
date_time = datetime.fromtimestamp(timestamp)

print("Date time object:", date_time)

d = date_time.strftime("%m/%d/%Y, %H:%M:%S")
print("Output 2:", d)	

d = date_time.strftime("%d %b, %Y")
print("Output 3:", d)

d = date_time.strftime("%d %B, %Y")
print("Output 4:", d)

d = date_time.strftime("%I%p")
print("Output 5:", d)

date_string = '31-Jan-2019'
format1 = "%d-%b-%Y"

# print '2019-01-30'

format2 = "%Y-%m-%d"
actual_date = datetime.strptime(date_string, format1).strftime(format2)

print actual_date