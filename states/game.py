import pygame
import numpy as np
from constants import GRID_HEIGHT,GRID_WIDTH,CELL_SIZE,SIDEBAR_WIDTH
from utils import COLOR, GameState, Map
from Tower import Soldier, Archer, Deadeye, Berserker, Assassin

def validate_tower_placement(mouse_pos, selected_tower, grid, WIDTH, HEIGHT):
    extrax = selected_tower.width//2
    extray = selected_tower.height//2

    gridx = mouse_pos[0]//CELL_SIZE
    gridy = mouse_pos[1]//CELL_SIZE

    # Check if the tower is within the grid boundaries
    if not (extrax <= gridx < WIDTH-extrax and extray <= gridy < HEIGHT-extray):
        return False,None

    # Check if the tower overlaps with existing towers
    tower_cells = grid[gridy-extray:gridy+extray+1, gridx-extrax:gridx+extrax+1]
    if np.any(tower_cells != 0):
        return False,(gridx,gridy)

    # Add more specific validation checks based on your game rules
    # For example, check if the tower is not on the track or other restricted areas

    return True,(gridx,gridy)

def place_tower(grids, grid, selected_tower):
    extrax = selected_tower.width//2
    extray = selected_tower.height//2

    gridx = grids[0]
    gridy = grids[1]

    grid[gridy-extray:gridy+extray+1, gridx-extrax:gridx+extrax+1] = selected_tower.id

def game_screen(screen, map, WIDTH, HEIGHT):

    # placements
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)

    # clock
    clock = pygame.time.Clock()
    FPS = 30

    # Constants for screen dimensions and fonts
    fonts = pygame.font.Font(None, 36)
    fontl = pygame.font.Font(None, 72)

    # Button
    resume_button = pygame.Rect((WIDTH//2)-100, (HEIGHT//2)-75, 200, 50)
    quit_button = pygame.Rect((WIDTH//2)-100, (HEIGHT//2)+25, 200, 50)
    pause_button = pygame.Rect(WIDTH-125, 25, 100, 50)

    placing_tower_rect = pygame.Rect(0,0,3*CELL_SIZE,3*CELL_SIZE)

    # Towers
    soldier_button = pygame.Rect(WIDTH-125, 100, 100, 50)
    archer_button = pygame.Rect(WIDTH-125, 175, 100, 50)
    deadeye_button = pygame.Rect(WIDTH-125, 250, 100, 50)
    berserker_button = pygame.Rect(WIDTH-125, 325, 100, 50)
    assassin_button = pygame.Rect(WIDTH-125, 400, 100, 50)

    # States
    game_over = False
    won = False
    paused = False
    placing = False
    selected_tower = None
    level = 1

    # conversion
    tower_color = {0: map.background, 1:COLOR.GREEN, 2:COLOR.RED, 3:COLOR.PURPLE, 4:COLOR.BLUE, 5:COLOR.BLACK}

    while not game_over and not won:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.MENU
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    paused = False
                elif pause_button.collidepoint(event.pos):
                    paused = True
                elif quit_button.collidepoint(event.pos):  # Handle the "Quit" button
                    return GameState.MENU,False
                elif soldier_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = Soldier
                elif archer_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = Archer
                elif deadeye_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = Deadeye
                elif berserker_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = Berserker
                elif assassin_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = Assassin
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
        
        pygame.display.set_caption(f"{map.name}: LEVEL {level}")

        if not paused:
        
            screen.fill(COLOR.WHITE)

            pygame.draw.rect(screen, COLOR.GRAY, pause_button)
            pause_text = fonts.render("Pause", True, COLOR.BLACK)
            screen.blit(pause_text, (pause_button.x+13, pause_button.y+10))
            pygame.draw.rect(screen, Soldier.color, soldier_button)
            soldier_text = fonts.render(Soldier.name, True, COLOR.WHITE)
            screen.blit(soldier_text, (soldier_button.x+13, soldier_button.y+10))
            pygame.draw.rect(screen, Archer.color, archer_button)
            archer_text = fonts.render(Archer.name, True, COLOR.WHITE)
            screen.blit(archer_text, (archer_button.x+13, archer_button.y+10))
            pygame.draw.rect(screen, Deadeye.color, deadeye_button)
            deadeye_text = fonts.render(Deadeye.name, True, COLOR.WHITE)
            screen.blit(deadeye_text, (deadeye_button.x+13, deadeye_button.y+10))
            pygame.draw.rect(screen, Berserker.color, berserker_button)
            berserker_text = fonts.render(Berserker.name, True, COLOR.WHITE)
            screen.blit(berserker_text, (berserker_button.x+13, berserker_button.y+10))
            pygame.draw.rect(screen, Assassin.color, assassin_button)
            assassin_text = fonts.render(Assassin.name, True, COLOR.WHITE)
            screen.blit(assassin_text, (assassin_button.x+13, assassin_button.y+10))

            for row in range(GRID_HEIGHT):
                for col in range(GRID_WIDTH):
                    cell_value = grid[row, col]
                    pygame.draw.rect(screen, tower_color[cell_value], (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            if placing:
                pygame.draw.rect(screen, selected_tower.color, placing_tower_rect)

        else:
            screen.fill(COLOR.BLACK)

            pygame.draw.rect(screen, COLOR.WHITE, resume_button)
            resume_text = fontl.render("Resume", True, COLOR.BLACK)
            screen.blit(resume_text, (resume_button.x+2, resume_button.y+1))
            pygame.draw.rect(screen, COLOR.WHITE, quit_button)
            quit_text = fontl.render("Quit", True, COLOR.BLACK)
            screen.blit(quit_text, (quit_button.x+35, quit_button.y+1))


        if placing:
            mouse_pos = pygame.mouse.get_pos()
            placing_tower_rect.topleft = (mouse_pos[0] - placing_tower_rect.width // 2,
                                          mouse_pos[1] - placing_tower_rect.height // 2)

            # Check if the placement is valid (not on the track and no overlap with existing towers)
            # Implement your own validation logic
            valid,grids = validate_tower_placement(mouse_pos, selected_tower, grid, WIDTH, HEIGHT)

            # Draw tower in red if placement is not valid
            if not valid:
                pygame.draw.rect(screen, COLOR.RED, placing_tower_rect)

            # Check if the left mouse button is released to place the tower
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if valid:
                    print("Placement cells:", grids)
                    place_tower(grids, grid, selected_tower)
                    print("All cells:", grid)

                placing = False

        pygame.display.flip()
        clock.tick(FPS)
    
    return GameState.MENU,won