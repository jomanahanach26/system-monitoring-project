"""Modul för hantering av loggning i systemet."""

import os
from datetime import datetime

# Funktionellt paradigm: Pure function (ren funktion).
# Den returnerar alltid exakt samma utdata om den får samma indata.
def format_log_entry(timestamp: str, category: str, message: str) -> str:
    """Formaterar loggtexten tydligt för filen. (Pure function)"""
    return f"[{timestamp}] [{category.upper()}] - {message}\n"

class Logger:
    """Logger class for handling logs."""
    def __init__(self, system_name: str):
        """Hanterar skapande och skrivning till unika loggfiler."""
        self.system_name = system_name
        if not os.path.exists("logs"):
            os.makedirs("logs")
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filepath = f"logs/log_{self.system_name}_{current_time}.txt"
        self.write_log("SYSTEM_START", f"{self.system_name} programmet startade.")

    def write_log(self, category: str, message: str):
        """Skriver ett meddelande till den unika loggfilen. 
        Dina gruppmedlemmar anropar denna funktion i sin kod."""
        # Hämta exakt tid för logginlägget (Krav för datum-tid på varje logg)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Använd vår 'pure function' för att formatera strängen
        log_text = format_log_entry(timestamp, category, message)
        # Errorhantering: Försök skriva till filen, hantera fel om det misslyckas
        try:
            # "a" står för append (lägger till text i slutet av filen utan att radera det gamla)
            with open(self.filepath, "a", encoding="utf-8") as file:
                file.write(log_text)
        except IOError as error:
            print(f"Loggsystem Error: Kunde inte spara till loggfilen. Detaljer: {error}")