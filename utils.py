from enum import Enum

class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4

class COLOR:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 128, 0)
    BLUE = (0, 0, 128)
    PURPLE = (128, 0, 128)
    TEAL = (0, 200, 150)
    GRAY = (128, 128, 128)
    LIGHT = (200, 200, 0)
    FAINT = (220, 220, 220)

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
        name = "Field"


    class Beach():
        primary = COLOR.TEAL
        secondary = COLOR.BLUE
        name = "Beach"


    class Moon():
        primary = COLOR.GRAY
        secondary = COLOR.FAINT
        name = "Moon"