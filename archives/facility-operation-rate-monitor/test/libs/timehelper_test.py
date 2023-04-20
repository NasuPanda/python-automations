from libs.timehelper import TimeShifter
from libs import timehelper


# time helper
print("*" * 50)
print("time helper module")
current = timehelper.current()
three_minutes_later = timehelper.shift_minutes(current, min=3)
first_day = timehelper.first_day_of_this_month()
last_day = timehelper.last_day_of_this_month()


print(f"current: {timehelper.format(current)}")
print(f"3 minutes later: {timehelper.format(three_minutes_later)}")
print(f"formatted first day: {timehelper.format(first_day)}")
print(f"formatted last day: {timehelper.format(last_day)}")

# TimeShifter
print("*" * 50)
print("TimeShifter class")

time_shifter = TimeShifter(current, 15)

for _ in range(5):
    print(timehelper.format(time_shifter.next_shift()))
