from enum import Enum

class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4

class COLOR:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (128, 0, 0)
    GREEN = (0, 128, 0)
    BLUE = (0, 0, 128)
    PURPLE = (128, 0, 128)
    TEAL = (0, 200, 150)
    GRAY = (128, 128, 128)
    LIGHT = (200, 200, 0)
    FAINT = (220, 220, 220)
    LIGHT_BLUE = (100, 180, 250)
    LIGHT_GREEN = (100, 250, 150)
    GRASS = (130, 225, 100)
    LIGHT_RED = (100, 250, 100)
    ORANGE = (128, 190, 0)
    YELLOW = (128, 128, 0)
    PINK = (250, 180, 250)
    DARK_GREEN = (0, 64, 0)
    DARK_BLUE = (0, 0, 64)
    DARK_RED = (64, 0, 0)

class GameState(Enum):
    MENU = 0
    SELECTION = 1
    GAME = 2
    COLLECTION = 3
    ACHIEVEMENTS = 4

class Map():


    class Field():
        primary = COLOR.GREEN
        secondary = COLOR.LIGHT
        background = COLOR.GRASS
        name = "Field"


    class Beach():
        primary = COLOR.TEAL
        secondary = COLOR.BLUE
        background = COLOR.LIGHT_BLUE
        name = "Beach"


    class Moon():
        primary = COLOR.GRAY
        secondary = COLOR.FAINT
        background = COLOR.FAINT
        name = "Moon"