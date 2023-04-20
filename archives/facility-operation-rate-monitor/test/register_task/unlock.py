import datetime

date_now = datetime.datetime.now()

with open("log.txt", "a") as f:
    f.write(f"\nUnlock : {date_now.strftime('%Y-%m-%d %H:%M:%S')}")
