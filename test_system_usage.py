"""Tester för system_usage.py. Kör med: python test_system_usage.py"""

from system_usage import SystemUsage, get_root_directory

system_usage = SystemUsage()

# root directory är C:\ på Windows och / på Mac och Linux
assert get_root_directory() in ("C:\\", "/")
assert system_usage.root_directory == get_root_directory()

# cpu-användningen är ett tal mellan 0 och 100 procent
cpu_usage = system_usage.get_cpu_usage()
assert type(cpu_usage) is float
assert 0 <= cpu_usage <= 100

# ram-minnesanvändningen är ett tal mellan 0 och 100 procent
ram_usage = system_usage.get_ram_usage()
assert type(ram_usage) is float
assert 0 <= ram_usage <= 100

# diskanvändningen är ett tal mellan 0 och 100 procent
disk_usage = system_usage.get_disk_usage()
assert type(disk_usage) is float
assert 0 <= disk_usage <= 100

# all användning har samma kategorier som larmen: cpu, ram och disk
all_usage = system_usage.get_all_usage()
assert list(all_usage.keys()) == ["cpu", "ram", "disk"]
for usage in all_usage.values():
    assert 0 <= usage <= 100

print("Alla tester för system_usage gick igenom")
