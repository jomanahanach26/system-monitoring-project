
"""Program för att hantera larmkonfiguration."""

import sys

from alarm import AlarmManager, Alarm
from logger import Logger


# Hämta förinställda val från kommandoraden
arguments = sys.argv[1:]
automatic_mode = len(arguments) > 0


def get_user_input(prompt):
    """Hämtar inmatning från användaren eller kommandoraden."""
    if automatic_mode:
        if arguments:
            answer = arguments.pop(0)
            print(f"{prompt}{answer}")
            return answer

        return None

    return input(prompt)


# Skapa loggsystemet
logger = Logger("Larmkonfiguration")

# Skapa larmhanteraren
manager = AlarmManager()

# Ladda sparade larm
logger.write_log("DATA_LOAD", "Försöker ladda sparade larm.")

if manager.load_alarms():
    logger.write_log("DATA_LOAD", "Sparade larm har laddats.")
else:
    logger.write_log("ERROR", "Kunde inte ladda sparade larm.")

logger.write_log("INFO", "Programmet är redo att användas.")


while True:
    print("\n--- Larmkonfiguration ---")
    print("1. Lägg till larm")
    print("2. Ta bort larm")
    print("3. Visa alla larm")
    print("4. Skicka larm till övervakningssystemet")
    print("5. Avsluta")

    choice = get_user_input("Välj ett alternativ: ")

    # Avsluta automatiskt när alla förinställda val har utförts
    if choice is None:
        print("Alla förinställda val har utförts.")
        break

    # Logga användarens val
    logger.write_log(
        "USER_CHOICE",
        f"Användaren valde alternativ {choice}."
    )

    if choice == "1":
        try:
            category = get_user_input(
                "Ange kategori (cpu, ram, disk): "
            )

            if category is None:
                print("Kategorin saknas.")
                break

            level_input = get_user_input(
                "Ange larmnivå (0-100): "
            )

            if level_input is None:
                print("Larmnivån saknas.")
                break

            level = float(level_input)

            alarm = Alarm(category, level)
            manager.add_alarm(alarm)

            print("Larmet har lagts till.")
            logger.write_log(
                "INFO",
                f"Larm har lagts till: {alarm}."
            )

        except (ValueError, TypeError, AttributeError) as error:
            print(f"Felaktig inmatning: {error}")
            logger.write_log(
                "ERROR",
                f"Fel vid tillägg av larm: {error}"
            )

    elif choice == "2":
        manager.show_alarms()

        try:
            index_input = get_user_input(
                "Ange numret på larmet du vill ta bort: "
            )

            if index_input is None:
                print("Larmnumret saknas.")
                break

            index = int(index_input)

            logger.write_log(
                "USER_CHOICE",
                f"Användaren valde larm nummer {index} för borttagning."
            )

            if manager.remove_alarm(index):
                logger.write_log(
                    "INFO",
                    f"Larm nummer {index} har tagits bort."
                )
            else:
                logger.write_log(
                    "ERROR",
                    f"Kunde inte ta bort larm nummer {index}."
                )

        except (ValueError, TypeError) as error:
            print("Felaktig inmatning. Ange ett giltigt larmnummer.")
            logger.write_log(
                "ERROR",
                f"Felaktigt larmnummer: {error}"
            )

    elif choice == "3":
        logger.write_log(
            "SYSTEM_FUNCTION",
            "Funktionen för att visa larm aktiverades."
        )

        manager.sort_alarms()
        manager.show_alarms()

        if manager.alarms:
            for index, alarm in enumerate(manager.alarms, start=1):
                logger.write_log(
                    "INFO",
                    f"Visat larm {index}: {alarm}."
                )
        else:
            logger.write_log(
                "INFO",
                "Det finns inga konfigurerade larm."
            )

    elif choice == "4":
        logger.write_log(
            "SYSTEM_FUNCTION",
            "Funktionen för att skicka larm aktiverades."
        )

        if manager.send_alarms_to_monitoring():
            logger.write_log(
                "DATA_SAVE",
                "Larmen har skickats till övervakningssystemets datafil."
            )
        else:
            logger.write_log(
                "ERROR",
                "Larmen kunde inte skickas till övervakningssystemet."
            )

    elif choice == "5":
        logger.write_log(
            "SYSTEM_FUNCTION",
            "Programmet sparar larm innan avslut."
        )

        if manager.save_alarms():
            logger.write_log(
                "DATA_SAVE",
                "Larmen har sparats i alarms.json."
            )
        else:
            logger.write_log(
                "ERROR",
                "Larmen kunde inte sparas i alarms.json."
            )

        logger.write_log(
            "SYSTEM_END",
            "Larmkonfigurationen avslutas."
        )

        print("Programmet avslutas.")
        break

    else:
        print("Ogiltigt val. Försök igen.")

        logger.write_log(
            "ERROR",
            f"Ogiltigt menyval: {choice}."
        )
