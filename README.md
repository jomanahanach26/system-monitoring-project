# System Monitoring Project

## Ansvarsfördelning / Delegation

**Esther:** Ansvarig för **Krav: Loggsystem**. 
  - **Filer:** logger.py och test_logger.py
  - **Klasser:** Logger
  - **Funktioner:** write_log() och format_log_entry()

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