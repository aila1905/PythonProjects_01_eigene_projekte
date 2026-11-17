import pygame
from shapes import SHAPES, SHAPE_COLORS
import random

WIDTH = 600
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 255)
GRAY = (180, 180, 180)
LIGHTGRAY = (140, 140, 140)

TEXT_SIZE = 25
TITLE_SIZE = 50
SMALL_SIZE = 20

INSTRUCTIONS_DURATION = 4000
FALL_SPEED = 500
game_state = "splash"
instructions_timer = 0
score = 0
# ========================================
# Speichert die aktuelle Auswahl im Pause-Menü.
# 0 bedeutet "Continue",
# 1 bedeutet "Quit Game".
# ========================================
pause_selection = 0

# =======================================
# Optionen des Pause-Menüs.
# Diese werden später auf dem Bildschirm angezeigt.
# =======================================
pause_options = [
    "Continue",
    "Quit Game"
]


def main():
    screen = init_game()
    game_loop(screen)
    exit_game()

def init_game():
    global clock, my_font, title_font, small_font, grid, current_piece, next_piece, fall_timer
    pygame.init()
    clock = pygame.time.Clock()
    random.seed()
    my_font = pygame.font.SysFont("Arial",TEXT_SIZE)
    title_font = pygame.font.SysFont("Arial",TITLE_SIZE)
    small_font = pygame.font.SysFont("Arial",SMALL_SIZE)

    # Spielfeld erstellen.
    # Jede Zahl 0 bedeutet ein leeres Feld.
    grid = [[0 for _ in range(15)]for _ in range(15)]

    # ========================================
    # Erstellt den ersten aktiven Stein.
    # Dieser Stein erscheint sofort auf dem Spielfeld.
    # ========================================
    current_piece = new_piece()

    # ========================================
    # Erstellt einen Vorschau-Stein.
    # Dieser Stein wird im rechten Bereich
    # als "Next Piece" angezeigt.
    # ========================================
    next_piece = new_piece()
    # Zeitmesser für automatisches Fallen.
    fall_timer = 0
    return pygame.display.set_mode((WIDTH, HEIGHT))


def exit_game():
    pygame.quit()

def game_loop(screen):
    while True:
        dt = clock.tick(FPS)
        if not event_handling():
            return
        if not update_game(dt):
            return
        draw_game(screen)


def event_handling() -> bool:
    global game_state, current_piece, pause_selection

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if game_state == "splash":
                game_state = "instructions" # direkt zur Anleitung
            elif game_state == "instructions":
                game_state = "playing"# beliebige Taste überspringt
            elif game_state == "playing":
                # ========================================
                # Öffnet das Pause-Menü.
                # Die Auswahl wird immer zurückgesetzt,
                # damit "Continue" zuerst ausgewählt ist.
                # ========================================
                if event.key == pygame.K_p:
                    pause_selection = 0
                    game_state = "paused"
                elif event.key == pygame.K_LEFT:
                    current_piece["col"] -= 1
                    if not valid_position(current_piece):
                        current_piece["col"] += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece["col"] += 1
                    if not valid_position(current_piece):
                        current_piece["col"] -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece["row"] += 1
                    if not valid_position(current_piece):
                        current_piece["row"] -= 1
                elif event.key == pygame.K_UP:
                    # Alte Rotation speichern,
                    # falls die neue Rotation ungültig ist.
                    old_rotation = current_piece["rotation"]
                    current_piece["rotation"] += 1
                    current_piece["rotation"] %= len(SHAPES[current_piece["shape"]])
                    if not valid_position(current_piece):
                        current_piece["rotation"] = old_rotation

            # ========================================
            # Steuerung des Pause-Menüs.
            # Pfeiltasten wechseln die Auswahl.
            # ENTER bestätigt die Auswahl.
            # ESC beendet das Spiel.
            # =========================================
            elif game_state == "paused":

                if event.key == pygame.K_UP:
                    pause_selection -= 1

                elif event.key == pygame.K_DOWN:
                    pause_selection += 1

                elif event.key == pygame.K_RETURN:

                    if pause_selection == 0:
                        game_state = "playing"

                    else:
                        return False

            # ========================================
            # Nach dem Game Over kann das Spiel
            # mit ESC beendet werden.
            # ========================================
            elif game_state == "gameover":
                if event.key == pygame.K_ESCAPE:
                    return False
    return True


def update_game(dt):
    global game_state, instructions_timer, fall_timer, current_piece, next_piece

    if game_state == "instructions":
        instructions_timer += dt
        if instructions_timer >= INSTRUCTIONS_DURATION:
            game_state = "playing"
    if game_state != "playing":
        return True
    fall_timer += dt
    if fall_timer >= FALL_SPEED:
        fall_timer = 0
        current_piece["row"] += 1

        # ========================================
        # Prüft, ob der Stein nicht mehr fallen kann.
        # Wenn eine Kollision entsteht,
        # wird der Stein im Spielfeld gespeichert.
        # ========================================
        if not valid_position(current_piece):
            current_piece["row"] -= 1
            lock_piece(current_piece)
            clear_lines()
            # ========================================
            # Der Vorschau-Stein wird jetzt zum aktiven Stein.
            # Danach wird ein neuer Vorschau-Stein erstellt.
            # ========================================
            current_piece = next_piece
            next_piece = new_piece()
            # ========================================
            # Wenn der neue Stein nicht platziert werden kann,
            # ist das Spielfeld voll.
            # Das Spiel endet.
            # ========================================
            if not valid_position(current_piece):
                game_state = "gameover"
    return True


# Erstellt einen neuen zufälligen Tetris-Stein.
# Jeder Stein startet oben in der Mitte.
def new_piece():
    current_piece = {
        "shape": random.choice(list(SHAPES.keys())),  # welche Form
        "rotation": 0,  # welche Rotation
        "row": 0,  # Position im Grid
        "col": 7  # startet in der Mitte
    }
    return current_piece



# ========================================
# Überprüft, ob der aktuelle Stein an einer gültigen
# Position liegt.
# Geprüft werden:
# - Spielfeldgrenzen
# - Kollision mit bereits gesetzten Steinen
# =========================================

def valid_position(piece):
    shape_matrix = SHAPES[piece["shape"]][piece["rotation"]]
    for r, row in enumerate(shape_matrix):
        for c, cell in enumerate(row):
            if cell == 0:
                continue

            new_row= piece["row"] + r
            new_col= piece["col"] + c

            if new_col < 0 or new_col >=15:
                return False

            if new_row >=15:
                return False

            if new_row >= 0 and grid[new_row][new_col] != 0:
                return False

    return True

# ========================================
# Speichert einen gefallenen Stein dauerhaft im Grid.
# Die einzelnen Blöcke werden mit dem Namen der Form
# gespeichert, damit später die richtige Farbe angezeigt wird.
# ========================================
def lock_piece(piece):
    shape_matrix = SHAPES[piece["shape"]][piece["rotation"]]
    for r, row in enumerate(shape_matrix):
        for c, cell in enumerate(row):
            if cell == 1:
                grid_row = piece["row"] + r
                grid_col = piece["col"] + c

                if 0<=grid_row<15:
                    grid[grid_row][grid_col] = piece["shape"]



# ========================================
# Entfernt alle vollständig gefüllten Reihen.
# Für jede entfernte Reihe bekommt der Spieler Punkte.
# ========================================
def clear_lines():
    global score
    new_grid = []
    removed_lines = 0
    for row in grid:
        if all(cell != 0 for cell in row):
            removed_lines += 1
        else:
            new_grid.append(row)
    while len(new_grid) < 15:
        new_grid.insert(0,[0 for _ in range(15)])

    grid[:] = new_grid
    score += removed_lines * 100

# ========================================
# Zeigt das Pause-Menü mit zwei Optionen.
# Der Spieler kann auswählen:
# Continue oder Quit Game.
# ============================================
def draw_pause_menu(screen):
    panel = pygame.Surface((300,200))
    panel.set_alpha(220)
    panel.fill((20,20,20))
    screen.blit(panel,(150,200))
    title = title_font.render("PAUSE",True,RED)
    screen.blit(title,title.get_rect(center=(WIDTH//2,230)))

    for i, option in enumerate(pause_options):
        color = WHITE
        if i == pause_selection:
            color = PINK
        text = small_font.render(option,True,color)
        screen.blit(text,(230,300+i*40))

# ========================================
# Zeigt den nächsten Stein im unteren Fenster.
# Das rechte Fenster bleibt nur für den Score.
# ========================================
def draw_next_piece(screen, piece):
    shape_matrix = SHAPES[piece["shape"]][piece["rotation"]]
    text = small_font.render("Next",True,WHITE)
    screen.blit(text,(200,475))
    for r, row in enumerate(shape_matrix):
        for c, cell in enumerate(row):
            if cell == 1:
                x = 190 + c * 30
                y = 500 + r * 30
                pygame.draw.rect(screen,SHAPE_COLORS[piece["shape"]],(x,y,30,30))
                pygame.draw.rect(screen,LIGHTGRAY,(x,y,30,30),1)


def draw_game(screen):
    screen.fill(BLACK)

    if game_state == "splash":
        write_caption(screen)

    elif game_state == "instructions":
        draw_window(screen)         # Spielfeld im Hintergrund
        write_titles(screen)
        draw_grid(screen, grid)
        draw_instructions(screen)   # Anleitung als Overlay

    elif game_state in ("playing", "paused","gameover"):
        draw_window(screen)
        write_titles(screen)
        draw_grid(screen, grid)


        if game_state != "gameover":
            draw_piece(screen, current_piece)
        if game_state =="gameover":
            text = title_font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

        if game_state == "paused":
            draw_pause_menu(screen)

    pygame.display.flip()


def write_caption(screen):
    text = my_font.render("Press any key to start game", True, PINK)
    text_rect = text.get_rect()
    text_rect.center = screen.get_rect().center
    screen.blit(text, text_rect)

    title = title_font.render("TETRIS", True, BLUE)
    title_rect = title.get_rect()
    title_rect.midtop = (WIDTH // 2, 20)
    screen.blit(title, title_rect)


def draw_instructions(screen):
    # Halbtransparentes dunkles Panel
    panel = pygame.Surface((520, 400))
    panel.set_alpha(210)
    panel.fill((20, 20, 20))
    screen.blit(panel, (40, 80))

    title = my_font.render("Instructions", True, PINK)
    screen.blit(title, title.get_rect(midtop=(WIDTH // 2, 95)))

    lines = [
        "← →   Move block left/right",
        "↓      Let block fall faster",
        "↑      Turn block",
        "P      Pause/Unpause",
        "",
    ]

    for i, line in enumerate(lines):
        surf = small_font.render(line, True, WHITE)
        screen.blit(surf, surf.get_rect(midleft=(60, 140 + i * 35)))

    hint = small_font.render("Press any Key to start imeadiatly", True, GRAY)
    screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, 465)))


def draw_window(screen):
    global score_window

    pygame.draw.rect(screen, WHITE, (10, 10, 450, 450), 3)
    score_window = pygame.draw.rect(screen, WHITE, (470, 10, 120, 450), 3)
    pygame.draw.rect(screen, WHITE, (10, 470, 450, 120), 3)

def write_titles(screen):
    score_txt = small_font.render("Score", False, WHITE)
    score_txt_rect = score_txt.get_rect()
    score_txt_rect.topleft = (score_window.centerx - 10, score_window.top + 10)
    screen.blit(score_txt, score_txt_rect.topleft)


    value = small_font.render(str(score), True, WHITE)
    screen.blit(value, (score_window.left +35, score_window.top + 40))
    draw_next_piece(screen,next_piece)

def draw_grid(screen, grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            x = 10 + j * 30
            y = 10 + i * 30
            if cell != 0:
                pygame.draw.rect(screen, SHAPE_COLORS[cell], (x, y, 30, 30))
            pygame.draw.rect(screen, LIGHTGRAY, (x, y, 30, 30), 1)

def draw_piece(screen, piece):
    shape_matrix = SHAPES[piece["shape"]][piece["rotation"]]
    for r, row in enumerate(shape_matrix):
        for c, cell in enumerate(row):
            if cell == 1:
                x = 10 + (piece["col"] + c) * 30
                y = 10 + (piece["row"] + r) * 30
                pygame.draw.rect(screen, SHAPE_COLORS[piece["shape"]], (x, y, 30, 30))

if __name__ == "__main__":
    main()