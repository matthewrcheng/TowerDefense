import pygame
import numpy as np
from constants import GRID_HEIGHT,GRID_WIDTH,CELL_SIZE,SIDEBAR_WIDTH
from utils import COLOR, GameState, Map
from Tower import Warrior, Archer, Deadeye, Berserker, Assassin
from Enemy import Enemy, Speedy, Tough

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

def find_target(tower, enemies):
    distances = {
        k: np.sqrt(((enemy.x+(enemy.width//2))-tower.x)**2 +
                   ((enemy.y+(enemy.height//2))-tower.x)**2)
        for k, enemy in enemies.items()
    }

    targets_in_range = [k for k, distance in distances.items() if distance <= tower.range]
    if targets_in_range:
        target_key = max(targets_in_range, key=lambda k: enemies[k].x)
        return enemies[target_key]

    return None  # No target found within the tower's range

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

def place_tower(grids, grid, selected_tower, num):
    extrax = selected_tower.width//2
    extray = selected_tower.height//2

    gridx = grids[0]
    gridy = grids[1]

    selected_tower.place(gridx,gridy,num)

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
    warrior_button = pygame.Rect(WIDTH-125, 100, 100, 50)
    archer_button = pygame.Rect(WIDTH-125, 175, 100, 50)
    deadeye_button = pygame.Rect(WIDTH-125, 250, 100, 50)
    berserker_button = pygame.Rect(WIDTH-125, 325, 100, 50)
    assassin_button = pygame.Rect(WIDTH-125, 400, 100, 50)
    warrior = Warrior()
    archer = Archer()
    deadeye = Deadeye()
    berserker = Berserker()
    assassin = Assassin()

    # States
    game_over = False
    won = False
    paused = False
    placing = False
    selected_tower = None
    level = 1
    enemy_timer = 0
    enemy_spawn_time = FPS*5

    # trackers
    tower_num = 0
    enemy_num = 0
    towers = dict()
    enemies = dict()

    # conversion
    tower_color = {0: map.background, 1:COLOR.GREEN, 2:COLOR.RED, 3:COLOR.PURPLE, 4:COLOR.BLUE, 5:COLOR.BLACK,
                   101:COLOR.DARK_GREEN, 102:COLOR.DARK_BLUE, 103:COLOR.DARK_RED}

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
                elif warrior_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = Warrior
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
                elif event.key == pygame.K_1:
                    placing = True
                    selected_tower = Warrior
                elif event.key == pygame.K_2:
                    placing = True
                    selected_tower = Archer
                elif event.key == pygame.K_3:
                    placing = True
                    selected_tower = Deadeye
                elif event.key == pygame.K_4:
                    placing = True
                    selected_tower = Berserker
                elif event.key == pygame.K_5:
                    placing = True
                    selected_tower = Assassin
                
        
        pygame.display.set_caption(f"{map.name}: LEVEL {level}")

        if not paused:
        
            screen.fill(COLOR.WHITE)

            pygame.draw.rect(screen, COLOR.GRAY, pause_button)
            pause_text = fonts.render("Pause", True, COLOR.BLACK)
            screen.blit(pause_text, (pause_button.x+13, pause_button.y+10))
            pygame.draw.rect(screen, COLOR.GREEN, warrior_button)
            warrior_text = fonts.render("Warrior", True, COLOR.WHITE)
            screen.blit(warrior_text, (warrior_button.x+13, warrior_button.y+10))
            pygame.draw.rect(screen, COLOR.RED, archer_button)
            archer_text = fonts.render("Archer", True, COLOR.WHITE)
            screen.blit(archer_text, (archer_button.x+13, archer_button.y+10))
            pygame.draw.rect(screen, COLOR.PURPLE, deadeye_button)
            deadeye_text = fonts.render("Deadeye", True, COLOR.WHITE)
            screen.blit(deadeye_text, (deadeye_button.x+13, deadeye_button.y+10))
            pygame.draw.rect(screen, COLOR.BLUE, berserker_button)
            berserker_text = fonts.render("Berserker", True, COLOR.WHITE)
            screen.blit(berserker_text, (berserker_button.x+13, berserker_button.y+10))
            pygame.draw.rect(screen, COLOR.BLACK, assassin_button)
            assassin_text = fonts.render("Assassin", True, COLOR.WHITE)
            screen.blit(assassin_text, (assassin_button.x+13, assassin_button.y+10))

            if enemy_timer >= enemy_spawn_time:
                new_enemy = Enemy()
                new_enemy.place((0,GRID_HEIGHT//2), grid, enemy_num)
                enemies[enemy_num] = new_enemy
                enemy_num += 1
                enemy_timer = 0
                print(f"Spawned new enemy, enemy count: {len(enemies)}")

            for row in range(GRID_HEIGHT):
                for col in range(GRID_WIDTH):
                    cell_value = grid[row, col]
                    pygame.draw.rect(screen, tower_color[cell_value], (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            for tower in towers.values():
                target = find_target(tower, enemies)
                if target:
                    killed = tower.attack(target)
                    if killed:
                        killed.kill(grid)
                        enemies.pop(killed.num)

            to_remove = []
            for k,enemy in enemies.items():
                success = enemy.walk(grid)
                if not success:
                    enemy.kill(grid)
                    enemies.pop(k)

            enemy_timer+=1

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
            tower = selected_tower()
            

            # Check if the placement is valid (not on the track and no overlap with existing towers)
            # Implement your own validation logic
            valid,grids = validate_tower_placement(mouse_pos, tower, grid, WIDTH, HEIGHT)

            # Draw tower in red if placement is not valid
            if not valid:
                draw_circle_alpha(screen, COLOR.CANT_PLACE, mouse_pos, tower.range*CELL_SIZE)
            else:
                draw_circle_alpha(screen, COLOR.CAN_PLACE, mouse_pos, tower.range*CELL_SIZE)
            draw_rect_alpha(screen, tower.color, placing_tower_rect)

            # Check if the left mouse button is released to place the tower
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if valid:
                    towers[tower_num] = tower
                    place_tower(grids, grid, tower, tower_num)
                    tower_num += 1

                placing = False

        pygame.display.flip()
        clock.tick(FPS)
    
    return GameState.MENU,won