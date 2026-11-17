# Jede Form ist eine Liste von Rotationen
# 1 = Block, 0 = leer

SHAPES = {

    # I-Form
    "I": [
        [[1, 1, 1, 1]],          # horizontal
        [[1], [1], [1], [1]]     # vertikal
    ],

    # J-Form
    "J": [
        [[1, 0],
         [1, 1],
         [0, 1]],
        # ... weitere Rotationen später
    ],

    # L-Form
    "L": [
        [[0, 1],
         [1, 1],
         [1, 0]],
    ],

    # O-Form
    "O": [
        [[1, 1],
         [1, 1]]     # Quadrat rotiert sich nicht
    ],

    # S-Form
    "S": [
        [[0, 1, 1],
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],

    # T-Form
    "T": [
        [[0, 1, 0],
         [1, 1, 1]],
        [[1, 0],
         [1, 1],
         [1, 0]],
        [[1, 1, 1],
         [0, 1, 0]],
        [[0, 1],
         [1, 1],
         [0, 1]]
    ],

    # Z-Form
    "Z": [
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]]
    ],
}


SHAPE_COLORS = {
    "I": (144, 238, 144),   # hellgrün
    "J": (100, 149, 237),   # blau
    "L": (255, 182, 193),   # pink
    "O": (144, 238, 144),   # grün
    "S": (255, 160, 122),   # lachs
    "T": (100, 149, 237),   # blau
    "Z": (255, 105, 180),   # pink/rot
}
