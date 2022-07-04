from libs.timehelper import TimeHelper


current = TimeHelper.current()
three_minutes_later = TimeHelper.shift_minutes(current, min=3)

print(f"current: {TimeHelper.format(current)}")
print(f"3 minutes later: {TimeHelper.format(three_minutes_later)}")

time_helper = TimeHelper(current, 15)

for _ in range(5):
    print(TimeHelper.format(time_helper.next_shift()))
