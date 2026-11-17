"""Basisklasse ``Game`` für einfache pygame-Anwendungen."""

import pygame


class Game:
    """Basisklasse für pygame-Spiele.

    Unterklassen passen das Verhalten durch Überschreiben von
    :meth:`handle_event`, :meth:`update_game` und :meth:`draw_game` an.
    """

    def __init__(
        self,
        title: str,
        fps: int = 60,
        size: tuple[int, int] = (640, 400),
    ) -> None:
        """Legt Fenstertitel, Bildrate und Fenstergröße fest.

        Args:
            title: Titel des Fensters.
            fps: Maximale Bilder pro Sekunde.
            size: Fenstergröße als (Breite, Höhe) in Pixeln.
        """
        self.title: str = title
        self.fps: int = fps
        self.size: tuple[int, int] = size
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.dt: float = 0
        self.screen: pygame.Surface | None = None

    def init_game(self) -> None:
        """Initialisiert pygame und erzeugt das Fenster."""
        pygame.init()
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode(self.size)

    def game_loop(self) -> None:
        """Führt die Hauptschleife aus, bis Events oder Update ``False`` liefern."""
        while True:
            # Berechnung der Zeitdifferenz seit dem letzten Frame
            self.dt = self.clock.tick(self.fps) / 1000
            if self.event_handling() == False:
                break
            if self.update_game() == False:
                break
            self.draw_game()

    def exit_game(self) -> None:
        """Beendet pygame."""
        pygame.quit()

    def event_handling(self) -> bool:
        """Verteilt alle anstehenden Events an :meth:`handle_event`.

        Bleibt in der Unterklasse unverändert.

        Returns:
            ``False``, sobald ein Event das Spiel beenden soll, sonst ``True``.
        """
        for event in pygame.event.get():
            if not self.handle_event(event):
                return False
        return True

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Verarbeitet ein einzelnes Event.

        Wird in der Unterklasse überschrieben.

        Args:
            event: Das zu verarbeitende pygame-Event.

        Returns:
            ``False`` bei ``pygame.QUIT``, sonst ``True``.
        """
        if event.type == pygame.QUIT:
            return False
        return True

    def update_game(self) -> bool:
        """Aktualisiert den Spielzustand um einen Frame.

        Returns:
            ``False``, wenn das Spiel beendet werden soll, sonst ``True``.
        """
        return True

    def draw_game(self) -> None:
        """Zeichnet den aktuellen Frame und bringt ihn zur Anzeige."""
        pygame.display.flip()

    def run(self) -> None:
        """Startet das Spiel: Initialisierung, Hauptschleife, Beenden."""
        self.init_game()
        self.game_loop()
        self.exit_game()