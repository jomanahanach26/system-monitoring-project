"""Monitoreringssystemet: programmet som användaren startar för att övervaka cpu, ram och disk.

Starta med: python monitoring.py

Användarval kan beskrivas innan programmet startar genom att skriva dem efter filnamnet.
De körs i tur och ordning när programmet startar, sedan fortsätter programmet som vanligt.
Exempel: python monitoring.py 2 1 5 3
  2 = Starta monitorsession, 1 = mät i varv, 5 = fem varv, 3 = Avsluta
"""

import sys

from monitor import SHARED_ALARM_FILE, Monitor
from session_length import ITERATIONS, SessionLength, parse_length, parse_length_type
from system_usage import SystemUsage

# menyvalen i monitoreringssystemet
LOAD_ALARMS = "1"
START_SESSION = "2"
EXIT_PROGRAM = "3"


def format_menu(alarm_count: int):
    """Returnerar huvudmenyn med antalet laddade larm. (Pure function)"""
    return ("\n--- Monitoreringssystem ---\n"
            f"Laddade larm: {alarm_count}\n"
            f"{LOAD_ALARMS}. Ladda alarm\n"
            f"{START_SESSION}. Starta monitorsession\n"
            f"{EXIT_PROGRAM}. Avsluta")


def format_length_question(length_type: str):
    """Returnerar frågan om sessionens längd för den valda typen av längd. (Pure function)"""
    if length_type == ITERATIONS:
        unit = "varv"
    else:
        unit = "sekunder"
    return f"Ange antal {unit} (ett heltal från 1, eller 'oändligt'): "


def parse_startup_choices(arguments: list):
    """Returnerar användarvalen som skrevs efter filnamnet när programmet startades. (Pure function)

    arguments är sys.argv, där första värdet är filnamnet och resten är användarvalen.
    """
    return arguments[1:]


def format_startup_choices(startup_choices: list):
    """Returnerar användarvalen från start som en text, till exempel "2 1 5 3". (Pure function)"""
    text = ""
    for choice in startup_choices:
        text += choice + " "
    return text.strip()


class MonitoringProgram:
    """Monitoreringssystemets meny som låter användaren ladda larm och starta monitorsessioner."""

    def __init__(self, alarm_file_path: str, startup_choices: list):
        """Skapar monitorn och avläsningen av datorn. Programmet körs tills användaren väljer Avsluta.

        startup_choices är användarvalen som ska köras automatiskt när programmet startar.
        """
        self.monitor = Monitor(alarm_file_path)
        self.startup_choices = startup_choices
        self.system_usage = SystemUsage()
        self.is_running = True
        # first-class functions: varje menyval är kopplat till metoden som ska köras
        self.menu_actions = {
            LOAD_ALARMS: self.load_alarms,
            START_SESSION: self.start_session,
            EXIT_PROGRAM: self.exit_program,
        }

    def get_user_input(self, prompt: str):
        """Returnerar nästa användarval från start, eller frågar användaren när de är slut.

        Svaret returneras utan mellanslag i början och slutet.
        """
        if len(self.startup_choices) > 0:
            choice = self.startup_choices.pop(0).strip()
            # visar valet som om användaren hade skrivit det, så att det syns vad som händer
            print(f"{prompt}{choice}   (valt vid start)")
            return choice
        return input(prompt).strip()

    def load_alarms(self):
        """Laddar larmen från den delade larmfilen och visar hur det gick."""
        print(self.monitor.load_alarms())

    def ask_length_type(self):
        """Frågar om sessionens längd ska mätas i varv eller sekunder, tills svaret är giltigt."""
        while True:
            choice = self.get_user_input("Hur ska längden mätas?\n1. Antal varv\n2. Antal sekunder\nVälj: ")
            length_type = parse_length_type(choice)
            if length_type is not None:
                return length_type
            print("Ogiltigt val, välj 1 eller 2.")

    def ask_length(self, length_type: str):
        """Frågar efter sessionens längd tills svaret är ett heltal från 1 eller 'oändligt'."""
        while True:
            length = parse_length(self.get_user_input(format_length_question(length_type)))
            if length is not None:
                return length
            print("Ogiltig längd, ange ett heltal från 1 eller 'oändligt'.")

    def start_session(self):
        """Frågar efter sessionens längd och kör sedan monitorsessionen."""
        length_type = self.ask_length_type()
        session_length = SessionLength(length_type, self.ask_length(length_type))
        self.monitor.run_session(session_length, self.system_usage)

    def exit_program(self):
        """Avslutar programmet efter nuvarande menyval."""
        print("Monitoreringssystemet avslutas.")
        self.is_running = False

    def handle_choice(self, choice: str):
        """Kör metoden som hör till menyvalet, eller visar ett felmeddelande om valet är ogiltigt."""
        if choice in self.menu_actions:
            self.menu_actions[choice]()
        else:
            print(f"Ogiltigt val, välj {LOAD_ALARMS}, {START_SESSION} eller {EXIT_PROGRAM}.")

    def run(self):
        """Laddar larmen automatiskt och visar sedan menyn tills användaren avslutar."""
        if len(self.startup_choices) > 0:
            print(f"Användarval från start som körs automatiskt: {format_startup_choices(self.startup_choices)}")
        self.load_alarms()
        try:
            while self.is_running:
                print(format_menu(len(self.monitor.alarms)))
                self.handle_choice(self.get_user_input("Välj ett alternativ: "))
        except KeyboardInterrupt:
            # Ctrl+C i menyn avslutar programmet utan felmeddelande från Python
            print("\nMonitoreringssystemet avslutas.")


if __name__ == "__main__":
    MonitoringProgram(SHARED_ALARM_FILE, parse_startup_choices(sys.argv)).run()
