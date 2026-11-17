import pygame
from game import Game

WHITE = (255, 255, 255)


class DrawingGame(Game):
    def __init__(self) -> None:
        super().__init__(title="Funktionales Malprogramm", size=(800, 600))

        #Spielzustand, Eine Liste von Strichen jeder Strich ist eine Liste von (x, y)-Tupeln
        self.state: list[list[tuple[int, int]]] = []

        #Speichert bis zu 5 vorherige Zustände für das Undo (Backspace)
        self.history: list[list[list[tuple[int, int]]]] = []

        #Temporärer Speicher für den Strich, der gerade gemalt wird
        self.current_stroke: list[tuple[int, int]] = []
        self.is_drawing: bool = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_drawing = True
            self.current_stroke = [event.pos]

        #Maus wird bewegt: Punkte sammeln, solange die Taste gedrückt ist
        elif event.type == pygame.MOUSEMOTION:
            if self.is_drawing:
                self.current_stroke.append(event.pos)

        #Maustaste loslassen: Strich beenden und Zustand aktualisieren
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_drawing:
                self.is_drawing = False

                #Nur speichern, wenn der Strich mehr als einen Punkt hat
                if len(self.current_stroke) > 1:
                    #Alten Zustand kopieren und in die Historie
                    previous_state = [list(stroke) for stroke in self.state]

                    new_history = list(self.history)
                    new_history.append(previous_state)
                    if len(new_history) > 5:
                        new_history.pop(0)  #Ältesten Eintrag entfernen
                    self.history = new_history

                    #Neuen Zustand erzeugen (alten Zustand + neuen Strich)
                    new_state = [list(stroke) for stroke in self.state]
                    new_state.append(list(self.current_stroke))
                    self.state = new_state

                self.current_stroke = []

        #Backspace-Taste: Letzten Strich rückgängig machen (Undo über Historie)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.history:
                    self.state = self.history[-1]  # Letzten Zustand wiederherstellen
                    self.history = self.history[:-1]  # Aus Historie entfernen

        return True

    def draw_game(self) -> None:
        self.screen.fill(WHITE)

        for stroke in self.state:
            if len(stroke) > 1:
                pygame.draw.lines(self.screen, (0, 0, 0), False, stroke, 3)

        if len(self.current_stroke) > 1:
            pygame.draw.lines(self.screen, (0, 0, 0), False, self.current_stroke, 3)
        pygame.display.flip()


if __name__ == "__main__":
    app = DrawingGame()
    app.run()