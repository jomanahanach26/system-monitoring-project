"""Tester för monitor.py. Kör med: python test_monitor.py"""

from alarm import Alarm
from monitor import Monitor, create_alarms, find_triggered_alarms, is_alarm_triggered

# create_alarms gör om larmdata till Alarm-objekt
alarm_data_list = [
    {"category": "cpu", "level": 80.0},
    {"category": "disk", "level": 90},
]
alarms = create_alarms(alarm_data_list)
assert len(alarms) == 2
assert alarms[0].category == "cpu"
assert alarms[0].level == 80.0
assert alarms[1].category == "disk"
assert alarms[1].level == 90.0

# create_alarms är en pure function: listan som skickas in ändras inte
assert alarm_data_list == [
    {"category": "cpu", "level": 80.0},
    {"category": "disk", "level": 90},
]

# create_alarms med en tom lista ger inga larm
assert create_alarms([]) == []

# create_alarms med en ogiltig kategori ger ValueError från Alarm-klassen
try:
    create_alarms([{"category": "network", "level": 50}])
    raised_value_error = False
except ValueError:
    raised_value_error = True
assert raised_value_error

# Monitor har inga larm innan larmen laddas
monitor = Monitor("test_data/valid_alarms.json")
assert monitor.alarms == []

# load_alarms laddar alla larm från en giltig larmfil
message = monitor.load_alarms()
assert message == "3 larm har laddats från test_data/valid_alarms.json."
assert len(monitor.alarms) == 3
assert monitor.alarms[1].category == "ram"
assert monitor.alarms[1].level == 70.5

# load_alarms ger ett meddelande och inga larm när larmfilen inte finns
missing_file_monitor = Monitor("test_data/finns_inte.json")
message = missing_file_monitor.load_alarms()
assert message == ("Hittade ingen larmfil (test_data/finns_inte.json). "
                   "Skicka larm från larm-konfigurationssystemet först.")
assert missing_file_monitor.alarms == []

# load_alarms behåller de laddade larmen när larmfilen är trasig
monitor.alarm_file_path = "test_data/broken_alarms.json"
message = monitor.load_alarms()
assert message == "Fel: Larmfilen test_data/broken_alarms.json kunde inte läsas, larmen laddades inte."
assert len(monitor.alarms) == 3

# load_alarms behåller de laddade larmen när ett larm har en ogiltig nivå
monitor.alarm_file_path = "test_data/invalid_level_alarms.json"
message = monitor.load_alarms()
assert message == "Fel: Larmfilen test_data/invalid_level_alarms.json kunde inte läsas, larmen laddades inte."
assert len(monitor.alarms) == 3

# larm och användning som används i testerna för larm som slår till
cpu_alarm_50 = Alarm("cpu", 50)
cpu_alarm_80 = Alarm("cpu", 80)
ram_alarm_70 = Alarm("ram", 70)
disk_alarm_90 = Alarm("disk", 90)
test_alarms = [cpu_alarm_50, cpu_alarm_80, ram_alarm_70, disk_alarm_90]
usage = {"cpu": 63.0, "ram": 70.0, "disk": 95.5}

# is_alarm_triggered är True när användningen överskrider larmets nivå
assert is_alarm_triggered(cpu_alarm_50, usage) == True
assert is_alarm_triggered(disk_alarm_90, usage) == True

# is_alarm_triggered är False när användningen är lägre än larmets nivå
assert is_alarm_triggered(cpu_alarm_80, usage) == False

# is_alarm_triggered är False när användningen är lika med larmets nivå, eftersom den inte överskrids
assert is_alarm_triggered(ram_alarm_70, usage) == False

# find_triggered_alarms returnerar alla larm som slår till, i samma ordning som larmen
assert find_triggered_alarms(test_alarms, usage) == [cpu_alarm_50, disk_alarm_90]

# find_triggered_alarms är en pure function: listan med larm ändras inte
assert test_alarms == [cpu_alarm_50, cpu_alarm_80, ram_alarm_70, disk_alarm_90]

# find_triggered_alarms returnerar en tom lista när inga larm slår till
assert find_triggered_alarms(test_alarms, {"cpu": 10.0, "ram": 20.0, "disk": 30.0}) == []

# find_triggered_alarms returnerar en tom lista när det inte finns några larm
assert find_triggered_alarms([], usage) == []

print("Alla tester för monitor gick igenom")
