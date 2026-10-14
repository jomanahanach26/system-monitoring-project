# System Monitoring Project

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

Kör de automatiska testerna med:

```bash
python -m unittest test_alarm.py
```

## Samarbete

Larmkonfigurationssystemet utvecklas som en del av ett gemensamt systemövervakningsprojekt. Integrationen med övervakningssystemet behöver samordnas med den ansvariga utvecklaren.