from constants import CELL_SIZE, GRID_HEIGHT, GRID_WIDTH, SIDEBAR_WIDTH
from utils import COLOR
import pygame


pygame.init()

grid = [[0 for w in range(GRID_WIDTH)] for h in GRID_HEIGHT]

screen = pygame.display.set_mode((GRID_WIDTH*CELL_SIZE + SIDEBAR_WIDTH,
                                  GRID_HEIGHT*CELL_SIZE))
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(COLOR.BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()