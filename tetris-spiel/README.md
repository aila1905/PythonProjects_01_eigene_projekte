# Tetris in Python

Ein Tetris-Klon, geschrieben in Python mit Pygame. Das Projekt ist bei mir im Rahmen von [Ausbildung/Studium/Kurs, z. B. "meiner Ausbildung zum ..."] entstanden.

## Funktionen
- Spielfeld mit 15x15 Feldern
- Zufällige Steine mit Rotation und Kollisionserkennung
- Vorschau des nächsten Steins
- Reihen werden gelöscht, dafür gibt es Punkte (100 pro Reihe)
- Startbildschirm, Anleitung und Pause-Menü
- Game-Over-Erkennung

## Steuerung
| Taste | Aktion |
|-------|--------|
| ← → | Stein nach links/rechts bewegen |
| ↓ | Stein schneller fallen lassen |
| ↑ | Stein drehen |
| P | Pause-Menü öffnen |
| Enter | Auswahl im Pause-Menü bestätigen |
| Esc | Spiel nach Game Over beenden |

## Starten
1. Python 3 installieren
2. Pygame installieren:
   ```
   pip install -r requirements.txt
   ```
3. Spiel starten:
   ```
   python [DATEINAME].py
   ```

## Aufbau
- `[DATEINAME].py`: Spiellogik, Zeichnen und Eingabeverarbeitung
- `shapes.py`: Formen und Farben der Steine

## Mögliche Erweiterungen
- Weitere Rotationen für die J- und L-Steine
- Steigende Geschwindigkeit mit höherem Level
- Highscore speichern

## Was ich dabei gelernt habe
[Zwei bis drei Sätze, z. B.: Umgang mit Pygame, Zustandsverwaltung des Spiels (Splash, Anleitung, Spiel, Pause, Game Over), Arbeit mit 2D-Listen.]