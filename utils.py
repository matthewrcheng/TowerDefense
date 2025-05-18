import pygame
from pygame.surface import Surface
from enum import Enum

def draw_rect_alpha(surface: Surface, color: tuple[int], rect: tuple[int, int, int, int], alpha: int=255):
    shape_surf = Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw_circle_alpha(surface: Surface, color: tuple[int], center: tuple[int, int], radius: int):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def draw_polygon_alpha(surface: Surface, color: tuple[int], points: list[tuple[int, int]]):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)

class Direction:
    up = (0,-1)
    down = (0,1)
    left = (-1,0)
    right = (1,0)

class Targeting:
    FIRST = "First"
    STRONG = "Strong"
    LAST = "Last"
    WEAK = "Weak"
    RANDOM = "Random"

class Attacking:
    MELEE = "Melee"
    RANGED = "Ranged"
    PULSE = "Pulse"
    AOE = "AOE"
    CHAIN = "Chain"

class Unicode:
    damage = "\U0001F5E1"
    delay = "\U0000231B"
    range = "\U0001F3F9"
    targets = "\U0001F3AF"
    pulse_range = "\U0001F310"
    heart = "\U00002764"
    heart_suit = "\U00002665"
    air = "\U0001FABD"
    metal = "\U0001F6E1"
    invisible_detection = "\U0001F441"
    invisible = "\U0001F47B"
    boss = "\U0001F451"
    stun = "\U0001F4AB"
    explosion = "\U0001F4A5"
    poison = "\U00002622"
    biohazard = "\U00002623"
    skull = "\U00002620"
    freeze = "\U00002744"
    fire = "\U0001F525"
    money = "\U0001F4B0"
    dollar = "\U0001F4B5"
    dollar_sign = "\U0001F4B2"
    medical = "\U00002695"
    link = "\U0001F517"

class COLOR:
    # Main colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (128, 0, 0)
    GREEN = (0, 128, 0)
    BLUE = (0, 0, 128)
    PURPLE = (128, 0, 128)
    TEAL = (0, 200, 150)
    GRAY = (128, 128, 128)
    ORANGE = (255, 170, 0)
    YELLOW = (230, 230, 0)
    PINK = (250, 180, 250)
    GOLD = (128,107,0)
    BROWN = (145, 110, 50)
    MAROON = (128, 0, 0)
    MAGENTA = (128, 0, 128)
    BLUE_PURPLE = (104, 0, 208)

    # Light colors
    LIGHT = (200, 200, 0)
    LIGHT_BLUE = (100, 180, 250)
    LIGHT_GREEN = (100, 250, 150)
    LIGHT_RED = (100, 250, 100)
    LIGHT_PURPLE = (192, 0, 192)
    LIGHT_GRAY = (192, 192, 192)
    LIGHT_ORANGE = (255, 210, 0)
    LIGHT_YELLOW = (255, 255, 0)
    LIGHT_BROWN = (186, 128, 60)
    
    # Dark colors
    DARK_GREEN = (0, 64, 0)
    DARK_BLUE = (0, 0, 64)
    DARK_RED = (64, 0, 0)
    DARK_PURPLE = (64, 0, 64)
    DARK_TEAL = (0, 100, 75)
    DARK_GRAY = (64, 64, 64)
    DARK_ORANGE = (235, 100, 0)
    DARK_YELLOW = (200, 150, 0)
    DARK_PINK = (125, 90, 125)
    DARK_BROWN = (120, 85, 40)
    DARK_BLUE_PURPLE = (52, 0, 104)

    # Alt colors
    FAINT_BLUE = (0, 0, 128, 80)
    FAINT_DARK_PURPLE = (64, 0, 64, 80)
    FADE = (0, 0, 0, 80)
    FAINT = (220, 220, 220)

    # Util colors
    CAN_PLACE = (255,255,255,80)
    CANT_PLACE = (128,0,0,80)

    # Terrain colors
    GRASS = (130, 225, 100)
    DARK_ROCK = (128, 128, 128)
    LIGHT_ROCK = (192, 192, 192)
    WET_SAND = (240, 225, 0)
    DRY_SAND = (255, 240, 160)
    WATER = (0, 0, 255)
    SNOW = (252, 252, 252)
    ICE = (160, 255, 255)
    FIRE = (255, 0, 0)
    LAVA = (255, 128, 0)


class GameState(Enum):
    MENU = 0
    MAP_SELECTION = 1
    TOWER_SELECTION = 2
    DIFFICULTY_SELECTION = 3
    GAME = 4
    COLLECTION = 5
    ACHIEVEMENTS = 6
    RESULTS = 7
    QUIT = 8

class Map():


    class Field():
        primary = COLOR.GREEN
        secondary = COLOR.LIGHT
        background = COLOR.GRASS
        path_color = COLOR.LIGHT_BROWN
        name = "Field"
        start = (0, 30)
        end = (79, 16)
        path = [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), \
                (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), \
                (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), \
                (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), \
                (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), \
                (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), \
                (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), \
                (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), (0, -1), \
                (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), \
                (1, 0), (1, 0)]


    class Beach():
        primary = COLOR.TEAL
        secondary = COLOR.WET_SAND
        background = COLOR.WET_SAND
        name = "Beach"


    class Moon():
        primary = COLOR.DARK_ROCK
        secondary = COLOR.LIGHT_ROCK
        background = COLOR.LIGHT_ROCK
        name = "Moon"

    class Desert():
        primary = COLOR.DARK_GREEN
        secondary = COLOR.DRY_SAND
        background = COLOR.DRY_SAND
        name = "Desert"

    class Arctic():
        primary = COLOR.SNOW
        secondary = COLOR.ICE
        background = COLOR.ICE
        name = "Arctic"

    class Jungle():
        primary = COLOR.DARK_BROWN
        secondary = COLOR.DARK_GREEN
        background = COLOR.GREEN
        name = "Jungle"

    class Volcano():
        primary = COLOR.DARK_RED
        secondary = COLOR.DARK_ORANGE
        background = COLOR.DARK_ORANGE
        name = "Volcano"
if __name__ == "__main__":
    field_map = Map.Field()
    cur = field_map.start
    for i in range(len(field_map.path)):
        print(cur)
        cur = cur[0] + field_map.path[i][0], cur[1] + field_map.path[i][1]
    print(cur)
