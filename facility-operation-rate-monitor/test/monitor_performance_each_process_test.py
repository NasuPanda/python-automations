import psutil

# https://psutil.readthedocs.io/en/latest/#processes


def get_cpu_usage(process, count: int = 10):
    cpu_usages = []
    for _ in range(count):
        cpu_usages.append(
            process.cpu_percent(interval=0.1)
        )
    return float(sum(cpu_usages) / len(cpu_usages))


processes = psutil.process_iter()
pids = []
cpu_usages = []
names = []
memories = []

for process in processes:
    pids.append(process.pid)
    cpu_usages.append(get_cpu_usage(process))
    names.append(process.name())
    memories.append(process.memory_percent(memtype="rss"))

for pid, name, cpu_usage, memory in zip(pids, names, cpu_usages, memories):
    print(str(pid).ljust(10), end="")
    print(name.ljust(30), end="")
    print(str(cpu_usage).ljust(10), end="")
    print(str(memory).ljust(30), end="\n")
