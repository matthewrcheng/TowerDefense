import pygame
from enum import Enum

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def draw_polygon_alpha(surface, color, points):
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
    DARK_PURPLE = (64, 0, 64)
    DARK_TEAL = (0, 100, 75)
    DARK_GRAY = (64, 64, 64)
    DARK_ORANGE = (64, 95, 0)
    DARK_YELLOW = (64, 64, 0)
    DARK_PINK = (125, 90, 125)
    LIGHT_PURPLE = (192, 0, 192)
    LIGHT_GRAY = (192, 192, 192)
    LIGHT_ORANGE = (192, 255, 0)
    LIGHT_YELLOW = (190, 190, 0)
    BROWN = (165, 42, 42)
    CAN_PLACE = (255,255,255,80)
    CANT_PLACE = (128,0,0,80)
    FADE = (0, 0, 0, 80)
    FAINT_BLUE = (0, 0, 128, 80)
    FAINT_DARK_PURPLE = (64, 0, 64, 80)

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