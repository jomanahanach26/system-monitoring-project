# System Monitoring Project

## Ansvarsfördelning / Delegation

**Esther:** Ansvarig för **Krav: Loggsystem**. 
  - **Filer:** logger.py och test_logger.py
  - **Klasser:** Logger
  - **Funktioner:** write_log() och format_log_entry()

**Lewis:** Ansvarig för **Krav: Monitoreringssystem**.
  - **Filer:** monitoring.py, monitor.py, session_length.py, system_usage.py, fakes.py,
    test_monitoring.py, test_monitor.py, test_session_length.py, test_system_usage.py och mappen test_data/
  - **Klasser:** MonitoringProgram, Monitor, SessionLength, SystemUsage, FakeLogger och FakeSystemUsage
  - **Funktioner:** format_menu(), format_length_question(), parse_startup_choices(), format_startup_choices(),
    format_for_log(), present(), read_alarm_file(), create_alarms(), format_alarm_list(), is_alarm_triggered(),
    find_triggered_alarms(), format_usage_report(), seconds_since(), parse_length_type(), parse_length()
    och get_root_directory()

## Larmkonfigurationssystem

Den här delen av projektet hanterar konfiguration av larm för CPU-, RAM- och diskanvändning.

## Funktioner

- Lägga till larm.
- Ta bort larm med hjälp av larmets nummer.
- Visa alla konfigurerade larm.
- Sortera larm efter kategori och nivå.
- Spara larm i en JSON-fil.
- Ladda sparade larm när programmet startar.
- Skicka larm till övervakningssystemet genom att välja alternativ 4.
- Hantera felaktig användarinmatning.

## Tillåtna värden

Kategorier:
- `cpu`
- `ram`
- `disk`

Larmnivån måste vara mellan 0 och 100 procent.

## Filer

- `alarm.py` – innehåller klasserna `Alarm` och `AlarmManager`.
- `main.py` – innehåller programmets meny.
- `test_alarm.py` – innehåller automatiska tester.
- `alarms.json` – sparar konfigurerade larm.
- `monitoring_data.json` – innehåller den senast skickade larmlistan.

## Köra programmet

Starta programmet med:

```bash
python main.py
```

## Köra testerna

## Loggsystem
Den här delen av projektet hanterar spårning, formatering och lagring av systemhändelser, användarsessioner och data i unika loggfiler.

### Funktioner
- **Automatisk start:** Skapar en unik loggfil när ett associerat program startar.
- **Loggning av användarval:** Sparar alla val som utförs av användaren.
- **Spårbarhet av information:** Loggar information som presenteras för användarna.
- **Persistent data:** Fångar upp när data laddas in respektive sparas.
- **Systemhändelser:** Loggar aktiverade systemfunktioner.
- **Felhantering:** Registrerar fel och felmeddelanden (möjliggör att en annan användare kan återskapa exakt samma användarsession i efterhand).
- **Tidsstämpling:** Associerar all information i loggfilen med exakt datum och tid med hjälp av `datetime`-modulen.

### Tekniska krav & implementationstekniker
Vid utveckling av loggsystemet används följande tekniker:
- **Klasser:** Objektorienterad struktur (t.ex. klassen `Logger`).
- **Funktioner:** Modulär struktur och uppdelning i funktioner.
- **Variabler:** Lagring av tillstånd och sessionsdata.
- **Funktionellt paradigm:** Användning av koncept som rena funktioner (*pure functions*) för deterministisk formatering.
- **Errorhantering:** Fångar och hanterar I/O-fel och undantag på ett säkert sätt.
- **Git:** Versionshantering under utvecklingsprocessen.


### Filer
- `logger.py` – innehåller loggningslogik, klasser och formateringsfunktioner.
- `test_logger.py` – innehåller automatiska tester för loggsystemet.


### Implementation
Loggsystemet är utformat för att enkelt kunna integreras i andra utvecklares kod i form av funktioner och metoder.

### Köra testerna
Kör de automatiska testerna för loggsystemet med:
```bash
python -m unittest test_logger.py
```
### Samarbete
Loggsystemet utvecklas som en del av ett gemensamt systemövervakningsprojekt och integreras i övriga utvecklares moduler för att säkerställa fullständig spårbarhet.

Kör de automatiska testerna med:

```bash
python -m unittest test_alarm.py
```

## Samarbete

Larmkonfigurationssystemet utvecklas som en del av ett gemensamt systemövervakningsprojekt. Integrationen med övervakningssystemet behöver samordnas med den ansvariga utvecklaren.

## Monitoreringssystem
Den här delen av projektet hanterar övervakning av CPU-, RAM- och diskanvändning och visar vilka larm som slår till.

### Funktioner
- **Ladda alarm:** Läser larmen som larmkonfigurationssystemet har skickat till `monitoring_data.json`. Larmen laddas också automatiskt när programmet startar.
- **Starta monitorsession:** Visar CPU-, RAM- och diskanvändning (root directory) en gång per sekund och alla larm vars nivå överskrids.
- **Sessionens längd:** Väljs i antal varv eller antal sekunder, från 1 till oändligt (skriv `oändligt`).
- **Avbryta sessionen:** Ctrl+C avbryter monitorsessionen utan att programmet avslutas.
- **Användarval vid start:** Menyval kan skrivas efter filnamnet och körs automatiskt när programmet startar.
- **Loggning:** Allt som händer loggas med loggsystemets `Logger` i en ny loggfil i mappen `logs/`.
- **Felhantering:** Hanterar larmfil som saknas, trasig larmfil och felaktig användarinmatning.

### Användarval vid start
Skriv valen efter filnamnet, så körs de i tur och ordning när programmet startar:
```bash
python monitoring.py 2 1 5 3
```
- `2` – starta monitorsession
- `1` – mät längden i varv (`2` = sekunder)
- `5` – fem varv
- `3` – avsluta

När valen är slut fortsätter programmet som vanligt och frågar användaren.

### Loggning
Varje logginlägg har en kategori:
- `ANVÄNDARVAL` – varje fråga och svar, om valet kom från start, och Ctrl+C.
- `INFORMATION` – allt som visas för användaren, även varje varv i monitorsessionen.
- `LADDAD DATA` – vilken larmfil som laddades och vilka larm den innehöll.
- `FUNKTION` – laddning av larm, start av monitorsession och avslut.
- `FEL` – larmfil som saknas, trasig larmfil, ogiltiga val och ogiltiga längder.

### Tekniska krav & implementationstekniker
Vid utveckling av monitoreringssystemet används följande tekniker:
- **Klasser:** `MonitoringProgram` (menyn), `Monitor` (larm och monitorsessioner), `SessionLength` (sessionens längd) och `SystemUsage` (avläsning med `psutil`).
- **Funktioner:** Varje uppgift har en egen funktion eller metod, till exempel `find_triggered_alarms()` och `format_usage_report()`.
- **Variabler:** Självdokumenterande namn, till exempel `triggered_alarms` och `iterations_done`.
- **Funktionellt paradigm:** Pure functions som `find_triggered_alarms()` och `create_alarms()`, och first-class functions där menyvalen är kopplade till metoder i en dict (`menu_actions`).
- **Errorhantering:** `try`/`except` för larmfil som saknas eller är trasig, och för Ctrl+C (`KeyboardInterrupt`).
- **Unit-tester:** Tester med `assert` för alla funktioner och klasser. Låtsasklasserna i `fakes.py` gör att testerna inte skapar loggfiler.
- **Git:** Utvecklat i branchen `lewis-utveckling` med en commit per steg.

### Filer
- `monitoring.py` – innehåller programmets meny, användarval vid start och loggning.
- `monitor.py` – innehåller laddning av larm, kontroll av larm och monitorsessionen.
- `session_length.py` – innehåller tolkning av sessionens längd i varv eller sekunder.
- `system_usage.py` – innehåller avläsning av CPU, RAM och disk med `psutil`.
- `fakes.py` – innehåller låtsasklasser som testerna använder.
- `test_monitoring.py`, `test_monitor.py`, `test_session_length.py` och `test_system_usage.py` – innehåller automatiska tester.
- `test_data/` – innehåller larmfiler som används i testerna.

### Köra programmet
Installera `psutil` i en virtual environment första gången:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Starta programmet med:
```bash
python monitoring.py
```

### Köra testerna
Kör de automatiska testerna för monitoreringssystemet med:
```bash
python test_monitoring.py
python test_monitor.py
python test_session_length.py
python test_system_usage.py
```

### Samarbete
Monitoreringssystemet utvecklas som en del av ett gemensamt systemövervakningsprojekt. Det läser larmen som larmkonfigurationssystemet skickar till `monitoring_data.json`, använder klassen `Alarm` från `alarm.py` och loggar med klassen `Logger` från `logger.py`. Båda programmen måste köras från projektmappen för att hitta den delade larmfilen.
