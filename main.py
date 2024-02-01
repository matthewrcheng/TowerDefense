from constants import CELL_SIZE, GRID_HEIGHT, GRID_WIDTH, SIDEBAR_WIDTH
from utils import GameState
from states.menu import menu_screen
from states.selection import selection_screen
from states.game import game_screen
from states.collection import collection_screen
from states.achievements import achievements_screen
import pygame


pygame.init()

WIDTH = GRID_WIDTH*CELL_SIZE + SIDEBAR_WIDTH
HEIGHT = GRID_HEIGHT*CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

running = True
current_state = GameState.MENU
map = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_state == GameState.MENU:
        current_state = menu_screen(screen)
    elif current_state == GameState.SELECTION:
        map = selection_screen(screen)
        if map:
            current_state = GameState.GAME
        else:
            current_state = GameState.MENU
    elif current_state == GameState.GAME:
        current_state,win = game_screen(screen, map, WIDTH, HEIGHT)
        pygame.display.set_caption("Tower Defense")
    elif current_state == GameState.COLLECTION:
        current_state = collection_screen(screen)
    elif current_state == GameState.ACHIEVEMENTS:
        current_state = achievements_screen(screen)

pygame.quit()