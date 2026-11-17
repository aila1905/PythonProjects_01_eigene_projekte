# Malprogramm mit Undo

Ein einfaches Malprogramm in Python mit Pygame. Gemalt wird mit der Maus, Striche lassen sich rückgängig machen.

## Besonderheit
Das Programm ist **funktional** aufgebaut: Der Zustand (alle Striche) wird nie verändert, sondern bei jeder Änderung durch eine neue Kopie ersetzt. 
Dadurch ist die Undo-Funktion über eine Historie von bis zu 5 Zuständen einfach umzusetzen.

## Steuerung
| Aktion | Wirkung |
|--------|---------|
| Maustaste gedrückt halten und bewegen | Strich malen |
| Backspace | Letzten Strich rückgängig machen (bis zu 5 Schritte) |

## Starten
```
pip install -r requirements.txt
python [DATEINAME].py
```

## Aufbau
- `[DATEINAME].py`: Die Klasse `DrawingGame` mit Zustand, Ereignisbehandlung und Zeichnen
- `game.py`: Basisklasse `Game` (Fenster und Hauptschleife)