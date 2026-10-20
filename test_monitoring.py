"""Tester för monitoring.py. Kör med: python test_monitoring.py"""

from monitoring import MonitoringProgram, format_length_question, format_menu
from session_length import ITERATIONS, SECONDS


class ScriptedMonitoringProgram(MonitoringProgram):
    """Låtsas vara användaren genom att svara med förbestämda svar i stället för att fråga med input()."""

    def __init__(self, alarm_file_path: str, answers: list):
        """Sparar svaren som ska ges i tur och ordning."""
        super().__init__(alarm_file_path)
        self.answers = answers

    def get_user_input(self, prompt: str):
        """Returnerar nästa förbestämda svar."""
        return self.answers.pop(0)


class FakeSystemUsage:
    """Låtsas vara SystemUsage, så att sessionerna i testerna går snabbt och alltid ger samma användning."""

    def get_all_usage(self):
        """Returnerar samma användning varje gång."""
        return {"cpu": 63.0, "ram": 70.0, "disk": 95.5}


# format_menu visar antalet laddade larm och alla menyval
assert format_menu(3) == ("\n--- Monitoreringssystem ---\n"
                          "Laddade larm: 3\n"
                          "1. Ladda alarm\n"
                          "2. Starta monitorsession\n"
                          "3. Avsluta")

# format_length_question frågar efter varv eller sekunder
assert format_length_question(ITERATIONS) == "Ange antal varv (ett heltal från 1, eller 'oändligt'): "
assert format_length_question(SECONDS) == "Ange antal sekunder (ett heltal från 1, eller 'oändligt'): "

# run laddar larmen automatiskt när programmet startar, och val 3 avslutar programmet
program = ScriptedMonitoringProgram("test_data/valid_alarms.json", ["3"])
program.run()
assert len(program.monitor.alarms) == 3
assert program.is_running == False

# ett ogiltigt menyval avslutar inte programmet
program = ScriptedMonitoringProgram("test_data/valid_alarms.json", ["9", "3"])
program.run()
assert program.answers == []
assert program.is_running == False

# val 1 laddar larmen igen från larmfilen
program = ScriptedMonitoringProgram("test_data/finns_inte.json", [])
program.monitor.alarm_file_path = "test_data/valid_alarms.json"
program.handle_choice("1")
assert len(program.monitor.alarms) == 3

# ask_length_type frågar igen tills valet är giltigt
program = ScriptedMonitoringProgram("test_data/valid_alarms.json", ["x", "3", "2"])
assert program.ask_length_type() == SECONDS
assert program.answers == []

# ask_length frågar igen tills längden är giltig
program = ScriptedMonitoringProgram("test_data/valid_alarms.json", ["0", "fem", "4"])
assert program.ask_length(ITERATIONS) == 4
assert program.answers == []

# val 2 startar en monitorsession med den valda längden: 2 varv
program = ScriptedMonitoringProgram("test_data/valid_alarms.json", ["2", "1", "2", "3"])
program.system_usage = FakeSystemUsage()
program.run()
assert program.answers == []
assert program.is_running == False

print("Alla tester för monitoring gick igenom")
