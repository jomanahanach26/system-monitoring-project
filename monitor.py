"""Monitoreringssystemets logik: laddar larmen och kontrollerar vilka larm som slår till."""

import json

from alarm import Alarm

# filen som larm-konfigurationssystemet skapar när användaren väljer "Skicka larm"
SHARED_ALARM_FILE = "monitoring_data.json"


def read_alarm_file(file_path: str):
    """Läser en larmfil och returnerar innehållet som en lista med larmdata."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def create_alarms(alarm_data_list: list):
    """Gör om larmdata från larmfilen till Alarm-objekt. (Pure function)

    Varje larmdata är en dict med nycklarna "category" och "level".
    Listan som skickas in ändras inte, i stället returneras en ny lista.
    """
    return [Alarm(alarm_data["category"], alarm_data["level"]) for alarm_data in alarm_data_list]


def is_alarm_triggered(alarm: Alarm, usage: dict):
    """Returnerar True om användningen i larmets kategori överskrider larmets nivå. (Pure function)

    usage är användningen i procent per kategori, till exempel {"cpu": 63.0, "ram": 44.7, "disk": 2.4}.
    """
    return usage[alarm.category] > alarm.level


def find_triggered_alarms(alarms: list, usage: dict):
    """Returnerar en ny lista med alla larm vars nivå överskrids av nuvarande användning. (Pure function)"""
    triggered_alarms = []
    for alarm in alarms:
        if is_alarm_triggered(alarm, usage):
            triggered_alarms.append(alarm)
    return triggered_alarms


class Monitor:
    """Håller reda på monitoreringssystemets larm."""

    def __init__(self, alarm_file_path: str):
        """Sparar vilken larmfil larmen ska laddas från. Inga larm är laddade från början."""
        self.alarm_file_path = alarm_file_path
        self.alarms = []

    def load_alarms(self):
        """Laddar larmen från larmfilen och returnerar ett meddelande om hur det gick."""
        try:
            alarm_data_list = read_alarm_file(self.alarm_file_path)
            self.alarms = create_alarms(alarm_data_list)
            return f"{len(self.alarms)} larm har laddats från {self.alarm_file_path}."

        except FileNotFoundError:
            self.alarms = []
            return (f"Hittade ingen larmfil ({self.alarm_file_path}). "
                    "Skicka larm från larm-konfigurationssystemet först.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            # larmen som redan var laddade behålls när filen inte går att läsa
            return f"Fel: Larmfilen {self.alarm_file_path} kunde inte läsas, larmen laddades inte."
