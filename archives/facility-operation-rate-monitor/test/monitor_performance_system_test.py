import psutil


# https://psutil.readthedocs.io/en/latest/#system-related-functions

# CPU usage
print(psutil.cpu_percent(1))           # => 13.3
# Memory usage
print(psutil.virtual_memory().percent) # => 85.5
print(psutil.swap_memory().percent)    # => 49.4
