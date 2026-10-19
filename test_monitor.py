"""Tester för monitor.py. Kör med: python test_monitor.py"""

from datetime import datetime

from alarm import Alarm
from monitor import (Monitor, create_alarms, find_triggered_alarms, format_usage_report,
                     is_alarm_triggered, seconds_since)
from session_length import ITERATIONS, SessionLength

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

# format_usage_report visar användningen och att inga larm har slagit till
assert format_usage_report(1, {"cpu": 10.0, "ram": 20.0, "disk": 30.0}, []) == (
    "Varv 1: CPU 10.0% | RAM 20.0% | Disk 30.0%\n  Inga larm har slagit till.")

# format_usage_report visar varje larm som slår till och nuvarande användning
assert format_usage_report(3, usage, [cpu_alarm_50, disk_alarm_90]) == (
    "Varv 3: CPU 63.0% | RAM 70.0% | Disk 95.5%"
    "\n  LARM! CPU-larm: 50.0% överskrids (nu 63.0%)"
    "\n  LARM! DISK-larm: 90.0% överskrids (nu 95.5%)")

# seconds_since räknar sekunderna sedan en starttid
assert 0 <= seconds_since(datetime.now()) < 1


class FakeSystemUsage:
    """Låtsas vara SystemUsage i testerna, så att användningen alltid är densamma och inget mäts på riktigt."""

    def __init__(self, interrupt_after_iterations: int):
        """Sparar efter hur många varv testet ska låtsas att användaren trycker Ctrl+C (None betyder aldrig)."""
        self.interrupt_after_iterations = interrupt_after_iterations
        self.iterations_measured = 0

    def get_all_usage(self):
        """Returnerar samma användning varje gång, eller skickar KeyboardInterrupt som Ctrl+C."""
        if self.iterations_measured == self.interrupt_after_iterations:
            raise KeyboardInterrupt
        self.iterations_measured += 1
        return {"cpu": 63.0, "ram": 70.0, "disk": 95.5}


# run_session kör exakt så många varv som valts
session_monitor = Monitor("test_data/valid_alarms.json")
session_monitor.load_alarms()
fake_system_usage = FakeSystemUsage(None)
assert session_monitor.run_session(SessionLength(ITERATIONS, 3), fake_system_usage) == 3
assert fake_system_usage.iterations_measured == 3

# run_session avbryts av Ctrl+C utan att felet når resten av programmet
interrupted_system_usage = FakeSystemUsage(2)
try:
    iterations_done = session_monitor.run_session(SessionLength(ITERATIONS, 10), interrupted_system_usage)
    interrupt_reached_program = False
except KeyboardInterrupt:
    interrupt_reached_program = True
assert interrupt_reached_program == False
assert iterations_done == 2

print("Alla tester för monitor gick igenom")
