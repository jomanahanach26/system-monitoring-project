from alarm import AlarmManager, Alarm

manager = AlarmManager()
manager.load_alarms()


while True:
    print("\n--- Larmkonfiguration ---")
    print("1. Lägg till larm")
    print("2. Ta bort larm")
    print("3. Visa alla larm")
    print("4. Skicka larm till övervakningssystemet")
    print("5. Avsluta")

    choice = input("Välj ett alternativ: ")

    if choice == "1":
        try:
            category = input("Ange kategori (cpu, ram, disk): ")
            level = float(input("Ange larmnivå (0-100): "))

            alarm = Alarm(category, level)
            manager.add_alarm(alarm)
            print("Larmet har lagts till.")

        except (ValueError, TypeError) as error:
            print(f"Felaktig inmatning: {error}")

    elif choice == "2":
        manager.show_alarms()

        try:
            index = int(input("Ange numret på larmet du vill ta bort: "))
            manager.remove_alarm(index)

        except ValueError:
            print("Felaktig inmatning. Ange ett giltigt larmnummer.")

    elif choice == "3":
        manager.sort_alarms()
        manager.show_alarms()

    elif choice == "4":
        manager.send_alarms_to_monitoring()

    elif choice == "5":
        manager.save_alarms()
        print("Programmet avslutas.")
        break

    else:
        print("Ogiltigt val. Försök igen.")