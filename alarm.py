import json


class Alarm:
    """Representerar ett larm för CPU-, RAM- eller diskanvändning."""

    VALID_CATEGORIES = ("cpu", "ram", "disk")

    def __init__(self, category: str, level: float):
        """Skapar ett larm och kontrollerar att värdena är giltiga."""
        category = category.strip().lower()

        if category not in self.VALID_CATEGORIES:
            raise ValueError("Kategorin måste vara cpu, ram eller disk.")

        if isinstance(level, bool) or not isinstance(level, (int, float)):
            raise TypeError("Larmnivån måste vara ett tal.")

        if not 0 <= level <= 100:
            raise ValueError("Larmnivån måste vara mellan 0 och 100.")

        self.category = category
        self.level = float(level)

    def __str__(self):
        """Returnerar en läsbar beskrivning av larmet."""
        return f"{self.category.upper()}-larm: {self.level:.1f}%"


class AlarmManager:
    """Hanterar alla konfigurerade larm."""

    def __init__(self):
        self.alarms = []

    def add_alarm(self, alarm):
        """Lägger till ett nytt larm."""
        self.alarms.append(alarm)

    def show_alarms(self):
        """Visar alla larm."""
        if not self.alarms:
            print("Det finns inga konfigurerade larm.")
            return

        for index, alarm in enumerate(self.alarms, start=1):
            print(f"{index}. {alarm}")

    def remove_alarm(self, index):
        """Tar bort ett larm med hjälp av dess nummer."""
        if index < 1 or index > len(self.alarms):
            print("Ogiltigt larmnummer.")
            return

        removed_alarm = self.alarms.pop(index - 1)
        print(f"Larmet {removed_alarm} har tagits bort.")

    def sort_alarms(self):
        """Sorterar larmen efter kategori och nivå."""
        self.alarms.sort(key=lambda alarm: (alarm.category, alarm.level))

    def save_alarms(self):
        """Sparar alla larm i en JSON-fil."""
        alarm_list = []

        for alarm in self.alarms:
            alarm_data = {
                "category": alarm.category,
                "level": alarm.level
            }
            alarm_list.append(alarm_data)

        try:
            with open("alarms.json", "w", encoding="utf-8") as file:
                json.dump(alarm_list, file, indent=4)

            print("Larmen har sparats.")

        except OSError:
            print("Fel: Larmen kunde inte sparas.")

    def load_alarms(self):
        """Laddar sparade larm från en JSON-fil."""
        try:
            with open("alarms.json", "r", encoding="utf-8") as file:
                alarm_list = json.load(file)

            loaded_alarms = []

            for alarm_data in alarm_list:
                alarm = Alarm(
                    alarm_data["category"],
                    alarm_data["level"]
                )
                loaded_alarms.append(alarm)

            self.alarms = loaded_alarms
            print("Larmen har laddats.")

        except FileNotFoundError:
            print("Ingen sparad larmlista hittades.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("Fel: Den sparade larmlistan kunde inte läsas.")

    def send_alarms_to_monitoring(self):
        """Skickar konfigurerade larm till övervakningssystemet."""
        alarm_list = []

        for alarm in self.alarms:
            alarm_data = {
                "category": alarm.category,
                "level": alarm.level
            }
            alarm_list.append(alarm_data)

        try:
            with open(
                "monitoring_data.json", "w", encoding="utf-8"
            ) as file:
                json.dump(alarm_list, file, indent=4)

            print("Larmen har skickats till övervakningssystemet.")

        except OSError:
            print("Fel: Larmen kunde inte skickas.")
