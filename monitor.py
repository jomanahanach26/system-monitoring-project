"""Monitoreringssystemets logik: laddar larmen, kontrollerar vilka larm som slår till och kör monitorsessioner."""

import json
from datetime import datetime

from alarm import Alarm

# filen som larm-konfigurationssystemet skapar när användaren väljer "Skicka larm"
SHARED_ALARM_FILE = "monitoring_data.json"

# kategorierna som används i loggfilen, så att det syns vad varje rad handlar om
LOG_USER_CHOICE = "ANVÄNDARVAL"
LOG_INFORMATION = "INFORMATION"
LOG_LOADED_DATA = "LADDAD DATA"
LOG_FUNCTION = "FUNKTION"
LOG_ERROR = "FEL"


def format_for_log(text: str):
    """Returnerar texten på en enda rad, så att varje logginlägg blir en rad i loggfilen. (Pure function)"""
    return text.replace("\n", " | ").strip(" |")


def present(message: str, logger):
    """Visar ett meddelande för användaren och loggar samma meddelande som information."""
    print(message)
    logger.write_log(LOG_INFORMATION, format_for_log(message))


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


def format_alarm_list(alarms: list):
    """Returnerar alla larm som en text, till exempel "CPU-larm: 80.0%, RAM-larm: 70.5%". (Pure function)"""
    if len(alarms) == 0:
        return "inga larm"
    text = ""
    for alarm in alarms:
        text += f"{alarm}, "
    # tar bort det sista kommatecknet och mellanslaget
    return text[:-2]


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


def format_usage_report(iteration: int, usage: dict, triggered_alarms: list):
    """Returnerar texten som visas för användaren under ett varv i monitorsessionen. (Pure function)"""
    report = f"Varv {iteration}: CPU {usage['cpu']}% | RAM {usage['ram']}% | Disk {usage['disk']}%"
    if len(triggered_alarms) == 0:
        return report + "\n  Inga larm har slagit till."
    for alarm in triggered_alarms:
        report += f"\n  LARM! {alarm} överskrids (nu {usage[alarm.category]}%)"
    return report


def seconds_since(start_time: datetime):
    """Returnerar hur många sekunder som har gått sedan start_time."""
    return (datetime.now() - start_time).total_seconds()


class Monitor:
    """Håller reda på monitoreringssystemets larm och kör monitorsessioner."""

    def __init__(self, alarm_file_path: str, logger):
        """Sparar vilken larmfil larmen ska laddas från och vilken logger som ska användas.

        logger är ett Logger-objekt från loggsystemet. Inga larm är laddade från början.
        """
        self.alarm_file_path = alarm_file_path
        self.logger = logger
        self.alarms = []

    def load_alarms(self):
        """Laddar larmen från larmfilen, loggar vad som laddades och returnerar ett meddelande om hur det gick."""
        self.logger.write_log(LOG_FUNCTION, f"Laddar larm från {self.alarm_file_path}.")
        try:
            alarm_data_list = read_alarm_file(self.alarm_file_path)
            self.alarms = create_alarms(alarm_data_list)
            self.logger.write_log(LOG_LOADED_DATA, f"{self.alarm_file_path}: {format_alarm_list(self.alarms)}")
            return f"{len(self.alarms)} larm har laddats från {self.alarm_file_path}."

        except FileNotFoundError:
            self.alarms = []
            self.logger.write_log(LOG_ERROR, f"Larmfilen {self.alarm_file_path} finns inte.")
            return (f"Hittade ingen larmfil ({self.alarm_file_path}). "
                    "Skicka larm från larm-konfigurationssystemet först.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            # larmen som redan var laddade behålls när filen inte går att läsa
            self.logger.write_log(LOG_ERROR, f"Larmfilen {self.alarm_file_path} kunde inte läsas: {error}")
            return f"Fel: Larmfilen {self.alarm_file_path} kunde inte läsas, larmen laddades inte."

    def run_session(self, session_length, system_usage):
        """Kör en monitorsession tills den valda längden är nådd eller användaren trycker Ctrl+C.

        session_length är ett SessionLength-objekt och system_usage ett SystemUsage-objekt.
        Returnerar hur många varv sessionen hann köra.
        """
        self.logger.write_log(LOG_FUNCTION, f"Startar monitorsession som pågår i {session_length}.")
        present(f"Monitorsessionen startar och pågår i {session_length}. Tryck Ctrl+C för att avbryta.",
                self.logger)
        start_time = datetime.now()
        iterations_done = 0
        try:
            while not session_length.is_finished(iterations_done, seconds_since(start_time)):
                usage = system_usage.get_all_usage()
                iterations_done += 1
                triggered_alarms = find_triggered_alarms(self.alarms, usage)
                present(format_usage_report(iterations_done, usage, triggered_alarms), self.logger)
            present(f"Monitorsessionen är klar efter {iterations_done} varv.", self.logger)
        except KeyboardInterrupt:
            # Ctrl+C avbryter bara sessionen, inte hela programmet
            self.logger.write_log(LOG_USER_CHOICE, "Användaren tryckte Ctrl+C under monitorsessionen.")
            present(f"\nMonitorsessionen avbröts efter {iterations_done} varv.", self.logger)
        return iterations_done
