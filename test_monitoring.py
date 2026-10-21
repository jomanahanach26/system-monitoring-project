"""Tester för monitoring.py. Kör med: python test_monitoring.py"""

from fakes import FakeLogger, FakeSystemUsage
from monitor import LOG_ERROR, LOG_FUNCTION, LOG_USER_CHOICE
from monitoring import (MonitoringProgram, format_length_question, format_menu,
                        format_startup_choices, parse_startup_choices)
from session_length import ITERATIONS, SECONDS

# format_menu visar antalet laddade larm och alla menyval
assert format_menu(3) == ("\n--- Monitoreringssystem ---\n"
                          "Laddade larm: 3\n"
                          "1. Ladda alarm\n"
                          "2. Starta monitorsession\n"
                          "3. Avsluta")

# format_length_question frågar efter varv eller sekunder
assert format_length_question(ITERATIONS) == "Ange antal varv (ett heltal från 1, eller 'oändligt'): "
assert format_length_question(SECONDS) == "Ange antal sekunder (ett heltal från 1, eller 'oändligt'): "

# parse_startup_choices tar bort filnamnet och returnerar användarvalen
assert parse_startup_choices(["monitoring.py", "2", "1", "5", "3"]) == ["2", "1", "5", "3"]
assert parse_startup_choices(["monitoring.py"]) == []

# parse_startup_choices är en pure function: sys.argv-listan ändras inte
arguments = ["monitoring.py", "3"]
parse_startup_choices(arguments)
assert arguments == ["monitoring.py", "3"]

# format_startup_choices visar användarvalen som en text
assert format_startup_choices(["2", "1", "5", "3"]) == "2 1 5 3"
assert format_startup_choices([]) == ""

# get_user_input returnerar användarvalen från start i tur och ordning och loggar dem
logger = FakeLogger()
program = MonitoringProgram("test_data/valid_alarms.json", ["2", " oändligt "], logger)
assert program.get_user_input("Välj: ") == "2"
assert program.get_user_input("Ange längd: ") == "oändligt"
assert program.startup_choices == []
assert logger.entries == [
    (LOG_USER_CHOICE, "Välj: 2   (valt vid start)"),
    (LOG_USER_CHOICE, "Ange längd: oändligt   (valt vid start)"),
]

# run laddar larmen automatiskt när programmet startar, och val 3 avslutar programmet och loggas
logger = FakeLogger()
program = MonitoringProgram("test_data/valid_alarms.json", ["3"], logger)
program.run()
assert len(program.monitor.alarms) == 3
assert program.is_running == False
assert (LOG_FUNCTION, "Laddar larm från test_data/valid_alarms.json.") in logger.entries
assert (LOG_FUNCTION, "Avslutar monitoreringssystemet.") in logger.entries

# ett ogiltigt menyval avslutar inte programmet, och felet loggas
logger = FakeLogger()
program = MonitoringProgram("test_data/valid_alarms.json", ["9", "3"], logger)
program.run()
assert program.startup_choices == []
assert program.is_running == False
assert (LOG_ERROR, "Ogiltigt menyval: '9'.") in logger.entries

# val 1 laddar larmen igen från larmfilen
program = MonitoringProgram("test_data/finns_inte.json", [], FakeLogger())
program.monitor.alarm_file_path = "test_data/valid_alarms.json"
program.handle_choice("1")
assert len(program.monitor.alarms) == 3

# ask_length_type frågar igen tills valet är giltigt, och de ogiltiga valen loggas
logger = FakeLogger()
program = MonitoringProgram("test_data/valid_alarms.json", ["x", "3", "2"], logger)
assert program.ask_length_type() == SECONDS
assert program.startup_choices == []
assert (LOG_ERROR, "Ogiltig typ av längd: 'x'.") in logger.entries

# ask_length frågar igen tills längden är giltig, och de ogiltiga längderna loggas
logger = FakeLogger()
program = MonitoringProgram("test_data/valid_alarms.json", ["0", "fem", "4"], logger)
assert program.ask_length(ITERATIONS) == 4
assert program.startup_choices == []
assert (LOG_ERROR, "Ogiltig längd: 'fem'.") in logger.entries

# användarvalen från start kör en hel monitorsession på 2 varv och avslutar sedan programmet
logger = FakeLogger()
program = MonitoringProgram("test_data/valid_alarms.json", ["2", "1", "2", "3"], logger)
program.system_usage = FakeSystemUsage(None)
program.run()
assert program.startup_choices == []
assert program.is_running == False
assert (LOG_FUNCTION, "Startar monitorsession som pågår i 2 varv.") in logger.entries

print("Alla tester för monitoring gick igenom")
