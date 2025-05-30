import pygame
import numpy as np
import random
from constants import GRID_HEIGHT,GRID_WIDTH,CELL_SIZE,SIDEBAR_WIDTH,FPS
from utils import COLOR, GameState, Map, Targeting, Unicode, draw_circle_alpha, draw_polygon_alpha, draw_rect_alpha
from Tower import Artisan, Bard, Tower, Gunslinger, Farm, General, Infantry, ArmoredInfantry, Artillery, CombatAviation
from Enemy import TrojanHorse, Infiltrator
from Status import *
# from Enemy import Enemy, , Speedy, Slow, Tough

# region Helper Functions
def draw_enemy_bar(screen, enemy, font):
    enemy_name_text = font.render(enemy.name, True, COLOR.WHITE)
    screen.blit(enemy_name_text, (enemy.x * CELL_SIZE, enemy.y * CELL_SIZE - 20))

    # Draw health bar
    health_bar_rect = pygame.Rect(enemy.x * CELL_SIZE, enemy.y * CELL_SIZE - 10,
                                  enemy.width * CELL_SIZE, 5)
    pygame.draw.rect(screen, COLOR.RED, health_bar_rect)  # Assuming green for health
    green_width = int((enemy.health / enemy.max_health) * health_bar_rect.width)
    green_part_rect = pygame.Rect(health_bar_rect.left, health_bar_rect.top, green_width, health_bar_rect.height)
    pygame.draw.rect(screen, COLOR.GREEN, green_part_rect)

def draw_path(screen, selected_map):
    cur = selected_map.start
    color = selected_map.path_color
    left = False
    top = False
    right = False
    bottom = False
    for i in range(len(selected_map.path) - 1): 
        # color each cell with the path color (each cell is 1 grid square or 10x10 pixels)
        pygame.draw.rect(screen, color, (cur[0] * CELL_SIZE, cur[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # color each surrounding cell with the path color as well
        # check if cell is on the left edge
        if cur[0] != 0:
            left = True
        # check if cell is on the top edge
        if cur[1] != 0:
            top = True
        # check if cell is on the right edge
        if cur[0] != GRID_WIDTH - 1:
            right = True
        # check if cell is on the bottom edge
        if cur[1] != GRID_HEIGHT - 1:
            bottom = True
        if left:
            pygame.draw.rect(screen, color, ((cur[0] - 1) * CELL_SIZE, cur[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if top:
            pygame.draw.rect(screen, color, (cur[0] * CELL_SIZE, (cur[1] - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if right:
            pygame.draw.rect(screen, color, ((cur[0] + 1) * CELL_SIZE, cur[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if bottom:
            pygame.draw.rect(screen, color, (cur[0] * CELL_SIZE, (cur[1] + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if left and top:
            pygame.draw.rect(screen, color, ((cur[0] - 1) * CELL_SIZE, (cur[1] - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if right and top:
            pygame.draw.rect(screen, color, ((cur[0] + 1) * CELL_SIZE, (cur[1] - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if left and bottom:
            pygame.draw.rect(screen, color, ((cur[0] - 1) * CELL_SIZE, (cur[1] + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if right and bottom:
            pygame.draw.rect(screen, color, ((cur[0] + 1) * CELL_SIZE, (cur[1] + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        cur = (cur[0] + selected_map.path[i][0], cur[1] + selected_map.path[i][1])
        left = False
        top = False
        right = False
        bottom = False

def validate_tower_placement(mouse_pos, selected_tower, grid, path_coords):
    extrax = selected_tower.width//2
    extray = selected_tower.height//2

    gridx = mouse_pos[0]//CELL_SIZE
    gridy = mouse_pos[1]//CELL_SIZE

    # Check if the tower is within the grid boundaries
    if not (extrax <= gridx < GRID_WIDTH-extrax and extray <= gridy < GRID_HEIGHT-extray):
        return False,None

    # Check if the tower overlaps with existing towers
    tower_cells = grid[gridy-extray:gridy+extray+1, gridx-extrax:gridx+extrax+1]
    if np.any(tower_cells != 0):
        return False,(gridx,gridy)

    # Check if the tower overlaps with the path
    if (gridx,gridy) in path_coords:
        return False,(gridx,gridy)
    # Check if the tower extra overlaps with the path
    if (gridx-extrax,gridy-extray) in path_coords:
        return False,(gridx,gridy)
    if (gridx+extrax,gridy-extray) in path_coords:
        return False,(gridx,gridy)
    if (gridx-extrax,gridy+extray) in path_coords:
        return False,(gridx,gridy)
    if (gridx+extrax,gridy+extray) in path_coords:
        return False,(gridx,gridy)

    return True,(gridx,gridy)

def place_tower(grids, grid, selected_tower, num):
    extrax = selected_tower.width//2
    extray = selected_tower.height//2

    gridx = grids[0]
    gridy = grids[1]

    selected_tower.place(gridx,gridy,num)

    grid[gridy-extray:gridy+extray+1, gridx-extrax:gridx+extrax+1] = selected_tower.id
# endregion

def game_screen(screen: pygame.Surface, selected_map, selected_towers: list[Tower], seed: dict, WIDTH: int, HEIGHT: int):

    # region Setup
    cur = selected_map.start
    path_coords = {cur}
    for i in range(0, len(selected_map.path)): 
        cur = (cur[0] + selected_map.path[i][0], cur[1] + selected_map.path[i][1])
        path_coords.add((cur[0] + selected_map.path[i][0], cur[1] + selected_map.path[i][1]))
        # add 8 surrounding cells to path_coords
        if selected_map.path[i][0] != 0:
            path_coords.add((cur[0] - 1, cur[1] + selected_map.path[i][1]))
        if selected_map.path[i][0] != GRID_WIDTH - 1:
            path_coords.add((cur[0] + 1, cur[1] + selected_map.path[i][1]))
        if selected_map.path[i][1] != 0:
            path_coords.add((cur[0] + selected_map.path[i][0], cur[1] - 1))
        if selected_map.path[i][1] != GRID_HEIGHT - 1:
            path_coords.add((cur[0] + selected_map.path[i][0], cur[1] + 1))
        if selected_map.path[i][0] != 0 and selected_map.path[i][1] != 0:
            path_coords.add((cur[0] - 1, cur[1] - 1))
        if selected_map.path[i][0] != 0 and selected_map.path[i][1] != GRID_HEIGHT - 1:
            path_coords.add((cur[0] - 1, cur[1] + 1))
        if selected_map.path[i][0] != GRID_WIDTH - 1 and selected_map.path[i][1] != 0:
            path_coords.add((cur[0] + 1, cur[1] - 1))
        if selected_map.path[i][0] != GRID_WIDTH - 1 and selected_map.path[i][1] != GRID_HEIGHT - 1:
            path_coords.add((cur[0] + 1, cur[1] + 1))
    # placements
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)

    # clock
    clock = pygame.time.Clock()

    # Constants for screen dimensions and fonts
    fonts = pygame.font.Font(None, 18)
    fontm = pygame.font.Font(None, 36)
    fontl = pygame.font.Font(None, 72)
    djvss = pygame.font.Font('DejaVuSans.ttf', 18)
    djvsm = pygame.font.Font('DejaVuSans.ttf', 36)
    djvsl = pygame.font.Font('DejaVuSans.ttf', 72)
    emojis = pygame.font.Font('emoji.ttf', 18)
    emojim = pygame.font.Font('emoji.ttf', 36)
    emojil = pygame.font.Font('emoji.ttf', 72)

    # Buttons, text, and icons
    exit_button = pygame.Rect(WIDTH-55, 25, 30, 30)
    
    target_cycle = {Targeting.FIRST: Targeting.STRONG, Targeting.STRONG: Targeting.LAST, Targeting.LAST: Targeting.WEAK, Targeting.WEAK: Targeting.RANDOM, Targeting.RANDOM: Targeting.FIRST}
    money_icon = emojis.render(Unicode.money, True, COLOR.YELLOW)
    heart_icon = emojis.render(Unicode.heart, True, COLOR.RED) # U00002764
    money_pos = (WIDTH-130, 25)
    heart_pos = (WIDTH-130, 55)

    placing_tower_rect = pygame.Rect(0,0,3*CELL_SIZE,3*CELL_SIZE)
    darken_screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
    menu_rect = pygame.Rect(150, 150, 300, 300)
    tower_display_rect = pygame.Rect(menu_rect.centerx - 50, menu_rect.centery - 50, 100, 100)
    tower_info_exit_button = pygame.Rect(menu_rect.right - 20, menu_rect.top, 20, 20)
    tower_info_upgrade_button = pygame.Rect(menu_rect.left + 20, menu_rect.bottom - 40, 100, 30)
    tower_info_target_button = pygame.Rect(menu_rect.left + 150, menu_rect.bottom - 40, 100, 30)
    tower_info_sell_button = pygame.Rect(menu_rect.right - 100, menu_rect.top + 60, 80, 20)

    # Towers
    tower1_button = pygame.Rect(WIDTH-125, 80, 100, 50)
    tower2_button = pygame.Rect(WIDTH-125, 135, 100, 50)
    tower3_button = pygame.Rect(WIDTH-125, 190, 100, 50)
    tower4_button = pygame.Rect(WIDTH-125, 245, 100, 50)
    tower5_button = pygame.Rect(WIDTH-125, 300, 100, 50)
    tower6_button = pygame.Rect(WIDTH-125, 355, 100, 50)
    tower7_button = pygame.Rect(WIDTH-125, 410, 100, 50)
    tower8_button = pygame.Rect(WIDTH-125, 465, 100, 50)
    # last_button = pygame.Rect(WIDTH-125, 520, 100, 50)
    tower1 = selected_towers["Tower1"]()
    tower2 = selected_towers["Tower2"]()
    tower3 = selected_towers["Tower3"]()
    tower4 = selected_towers["Tower4"]()
    tower5 = selected_towers["Tower5"]()
    tower6 = selected_towers["Tower6"]()
    tower7 = selected_towers["Tower7"]()
    tower8 = selected_towers["Tower8"]()

    # States
    game_over = False
    won = False
    paused = False
    placing = False
    tower_info_menu = None
    selected_tower = None
    level = 1
    enemy_timer = 0
    enemy_spawn_time = None
    autorun = False
    health = 100
    money = 5000 # 500
    time = 0

    # trackers
    tower_num = 0
    troop_num = 0
    enemy_num = 0
    towers = dict()
    troops = dict()
    enemies = dict()
    farms = []

    # conversion
    tower_color = {0: selected_map.background, 1:COLOR.GREEN, 2:COLOR.RED, 3:COLOR.PURPLE, 4:COLOR.BLUE, 5:COLOR.BLACK,
                   101:COLOR.DARK_GREEN, 102:COLOR.DARK_BLUE, 103:COLOR.DARK_RED}
    # endregion

    while not won:
        # region Handle Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # States
                game_over = False
                won = False
                paused = False
                placing = False
                tower_info_menu = None
                selected_tower = None
                level = 1
                enemy_timer = 0
                enemy_spawn_time = None
                autorun = False
                health = 100
                money = 500

                # trackers
                tower_num = 0
                troop_num = 0
                enemy_num = 0
                towers = dict()
                troops = dict()
                enemies = dict()
                farms = []
                return GameState.MENU,False,0,0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    return GameState.MENU,False,0,0
                elif tower1_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = selected_towers["Tower1"]
                elif tower2_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = selected_towers["Tower2"]
                elif tower3_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = selected_towers["Tower3"]
                elif tower4_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = selected_towers["Tower4"]
                elif tower5_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = selected_towers["Tower5"]
                elif tower6_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = selected_towers["Tower6"]
                elif tower7_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = selected_towers["Tower7"]
                elif tower8_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = selected_towers["Tower8"]
                else:
                    if tower_info_menu:
                        if tower_info_exit_button.collidepoint(event.pos):
                            tower_info_menu = False
                        elif tower_info_upgrade_button.collidepoint(event.pos):
                            cost = tower_info_menu.upgrade_next(money)
                            if cost:
                                money = int(money - cost)
                                print("Upgraded successfully")
                                if type(tower_info_menu) == Artisan or type(tower_info_menu) == Bard:
                                    print("Initializing effects")
                                    tower_info_menu.init_effects(towers)
                        elif tower_info_target_button.collidepoint(event.pos):
                            tower_info_menu.targeting = target_cycle.get(tower_info_menu.targeting)
                            print("Changing targeting")
                        elif tower_info_sell_button.collidepoint(event.pos):
                            towers.pop(tower_info_menu.num)
                            money += tower_info_menu.total_cost//2
                            tower_info_menu = False
                            tower_info_menu.remove_effects(towers)
                            print("Sold tower")
                    elif not placing:
                        for tower in towers.values():
                            if tower.rect.collidepoint(event.pos):
                                tower_info_menu = tower
                                break
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                elif event.key == pygame.K_1:
                    placing = True
                    selected_tower = selected_towers["Tower1"]
                elif event.key == pygame.K_2:
                    placing = True
                    selected_tower = selected_towers["Tower2"]
                elif event.key == pygame.K_3:
                    placing = True  
                    selected_tower = selected_towers["Tower3"]
                elif event.key == pygame.K_4:
                    placing = True
                    selected_tower = selected_towers["Tower4"]
                elif event.key == pygame.K_5:
                    placing = True
                    selected_tower = selected_towers["Tower5"]
                elif event.key == pygame.K_6:
                    placing = True
                    selected_tower = selected_towers["Tower6"]
                elif event.key == pygame.K_7:
                    placing = True
                    selected_tower = selected_towers["Tower7"]
                elif event.key == pygame.K_8:
                    placing = True
                    selected_tower = selected_towers["Tower8"]
        # endregion
        
        # region Game Logic
        if health <= 0:
            # States
            game_over = False
            won = False
            paused = False
            placing = False
            tower_info_menu = None
            selected_tower = None
            level = 1
            enemy_timer = 0
            enemy_spawn_time = None
            autorun = False
            health = 100
            money = 500

            # trackers
            tower_num = 0
            troop_num = 0
            enemy_num = 0
            towers = dict()
            troops = dict()
            enemies = dict()
            farms = []
            return GameState.RESULTS,won,level,time   
        
        pygame.display.set_caption(f"{selected_map.name}: LEVEL {level}")
        
        screen.fill(COLOR.WHITE)

        money_text = fontm.render(str(money), True, COLOR.YELLOW)
        heart_text = fontm.render(str(health), True, COLOR.RED)

        screen.blit(money_icon, money_pos)
        screen.blit(money_text, (money_pos[0] + 20, money_pos[1]))

        screen.blit(heart_icon, heart_pos)
        screen.blit(heart_text, (heart_pos[0] + 20, heart_pos[1]))


        pygame.draw.rect(screen, COLOR.GRAY, exit_button)

        # Draw two horizontal lines to represent pause
        line1_start = (exit_button.x + 10, exit_button.y + 8)
        line1_end = (exit_button.x + 10, exit_button.y + 22)

        line2_start = (exit_button.x + 20, exit_button.y + 8)
        line2_end = (exit_button.x + 20, exit_button.y + 22)

        pygame.draw.line(screen, COLOR.BLACK, line1_start, line2_end, 2)
        pygame.draw.line(screen, COLOR.BLACK, line2_start, line1_end, 2)

        # Tower 1
        pygame.draw.rect(screen, tower1.color, tower1_button)
        tower1_text = fonts.render(tower1.name, True, tower1.text_color)
        screen.blit(tower1_text, (tower1_button.x+13, tower1_button.y+10))
        tower1_cost = fonts.render(f"${tower1.cost}", True, tower1.text_color)
        screen.blit(tower1_cost, (tower1_button.x+13, tower1_button.y+30))

        # Tower 2
        pygame.draw.rect(screen, tower2.color, tower2_button)
        tower2_text = fonts.render(tower2.name, True, tower2.text_color)
        screen.blit(tower2_text, (tower2_button.x+13, tower2_button.y+10))
        tower2_cost = fonts.render(f"${tower2.cost}", True, tower2.text_color)
        screen.blit(tower2_cost, (tower2_button.x+13, tower2_button.y+30))

        # Tower 3
        pygame.draw.rect(screen, tower3.color, tower3_button)
        tower3_text = fonts.render(tower3.name, True, tower3.text_color)
        screen.blit(tower3_text, (tower3_button.x+13, tower3_button.y+10))
        tower3_cost = fonts.render(f"${tower3.cost}", True, tower3.text_color)
        screen.blit(tower3_cost, (tower3_button.x+13, tower3_button.y+30))

        # Tower 4
        pygame.draw.rect(screen, tower4.color, tower4_button)
        tower4_text = fonts.render(tower4.name, True, tower4.text_color)
        screen.blit(tower4_text, (tower4_button.x+13, tower4_button.y+10))
        tower4_cost = fonts.render(f"${tower4.cost}", True, tower4.text_color)
        screen.blit(tower4_cost, (tower4_button.x+13, tower4_button.y+30))

        # Tower 5
        pygame.draw.rect(screen, tower5.color, tower5_button)
        tower5_text = fonts.render(tower5.name, True, tower5.text_color)
        screen.blit(tower5_text, (tower5_button.x+13, tower5_button.y+10))
        tower5_cost = fonts.render(f"${tower5.cost}", True, tower5.text_color)
        screen.blit(tower5_cost, (tower5_button.x+13, tower5_button.y+30))

        # Tower 6
        pygame.draw.rect(screen, tower6.color, tower6_button)
        tower6_text = fonts.render(tower6.name, True, tower6.text_color)
        screen.blit(tower6_text, (tower6_button.x+13, tower6_button.y+10))
        tower6_cost = fonts.render(f"${tower6.cost}", True, tower6.text_color)
        screen.blit(tower6_cost, (tower6_button.x+13, tower6_button.y+30))

        # Tower 7
        pygame.draw.rect(screen, tower7.color, tower7_button)
        tower7_text = fonts.render(tower7.name, True, tower7.text_color)
        screen.blit(tower7_text, (tower7_button.x+13, tower7_button.y+10))
        tower7_cost = fonts.render(f"${tower7.cost}", True, tower7.text_color)
        screen.blit(tower7_cost, (tower7_button.x+13, tower7_button.y+30))

        # Tower 8
        pygame.draw.rect(screen, tower8.color, tower8_button)
        tower8_text = fonts.render(tower8.name, True, tower8.text_color)
        screen.blit(tower8_text, (tower8_button.x+13, tower8_button.y+10))
        tower8_cost = fonts.render(f"${tower8.cost}", True, tower8.text_color)
        screen.blit(tower8_cost, (tower8_button.x+13, tower8_button.y+30))

        if seed.get(level) and enemy_timer <= 0:
            if enemy_spawn_time:
                new_enemy = seed.get(level)[0][0]()
                new_enemy.place((0,GRID_HEIGHT//2), grid, enemy_num)
                enemies[enemy_num] = new_enemy
                enemy_num += 1
                enemy_timer = seed.get(level)[0][1]
                seed.get(level).pop(0)
            else:
                print(f"Starting level {level}")
                enemy_spawn_time = seed.get(level)[0][1]
                enemy_timer = enemy_spawn_time

        pygame.draw.rect(screen, tower_color[0], (0, 0, WIDTH-SIDEBAR_WIDTH, HEIGHT))
        draw_path(screen, selected_map)

        for tower in towers.values():
            pygame.draw.rect(screen, tower.color, tower.rect)

        # region Tower Logic
        for tower in towers.values():
            for i in range(len(tower.attack_names)):
                if tower.current_delays[i] <= 0 and tower.damages[i]:
                    target = tower.find_target(i, enemies, screen)
                    if target:
                        if type(target) is list:
                            total_damage = sum(min(tower.damages[i], t.health) for t in target)                            
                        else:
                            total_damage = min(tower.damages[i], target.health)
                        money += (total_damage * tower.money_multiplier)
                        if type(tower) == Gunslinger or (type(tower) == Artisan and tower.attack_names[i] == "Coin Toss"):
                            money += tower.money
                        killed_list = tower.attack(i, screen, target)
                        tower.total_damage += total_damage
                        if killed_list:
                            for killed in killed_list:
                                killed.kill(grid)
                                # special case for TrojanHorse
                                if type(killed) == TrojanHorse:
                                    for i in range(3):
                                        new_enemy = Infiltrator()
                                        new_enemy.place((killed.x-i+1,GRID_HEIGHT//2), grid, enemy_num)
                                        enemies[enemy_num] = new_enemy
                                        enemy_num += 1
                                enemies.pop(killed.num)
                else:
                    tower.current_delays[i] -= (1 * tower.attack_speed_multiplier)
            if type(tower) == General:
                if tower.current_infantry_spawn_delay <= 0 and tower.spawn_infantry:
                    infantry = Infantry(tower.infantry_level)
                    troops[troop_num] = infantry
                    place_tower(selected_map.end, grid, infantry, troop_num)
                    troop_num += 1
                    infantry.set_progress(selected_map.path)
                    print(f"{infantry.name} spawned at {infantry.x},{infantry.y}")
                    tower.current_infantry_spawn_delay = tower.total_infantry_spawn_delay
                else:
                    tower.current_infantry_spawn_delay -= 1
                if tower.current_armored_infantry_spawn_delay <= 0 and tower.spawn_armored_infantry:
                    armored_infantry = ArmoredInfantry(tower.armored_infantry_level)
                    troops[troop_num] = armored_infantry
                    place_tower(selected_map.end, grid, armored_infantry, troop_num)
                    troop_num += 1
                    armored_infantry.set_progress(selected_map.path)
                    print(f"{armored_infantry.name} spawned at {armored_infantry.x},{armored_infantry.y}")
                    tower.current_armored_infantry_spawn_delay = tower.total_armored_infantry_spawn_delay
                else:
                    tower.current_armored_infantry_spawn_delay -= 1
                if tower.current_artillery_spawn_delay <= 0 and tower.spawn_artillery:
                    artillery = Artillery(tower.artillery_level)
                    troops[troop_num] = artillery
                    place_tower(selected_map.end, grid, artillery, troop_num)
                    troop_num += 1
                    artillery.set_progress(selected_map.path)
                    print(f"{artillery.name} spawned at {artillery.x},{artillery.y}")
                    tower.current_artillery_spawn_delay = tower.total_artillery_spawn_delay
                else:
                    tower.current_artillery_spawn_delay -= 1
                if tower.current_combat_aviation_spawn_delay <= 0 and tower.spawn_combat_aviation:
                    combat_aviation = CombatAviation(tower.combat_aviation_level)
                    troops[troop_num] = combat_aviation
                    place_tower(selected_map.end, grid, combat_aviation, troop_num)
                    troop_num += 1
                    combat_aviation.set_progress(selected_map.path)
                    print(f"{combat_aviation.name} spawned at {combat_aviation.x},{combat_aviation.y}")
                    tower.current_combat_aviation_spawn_delay = tower.total_combat_aviation_spawn_delay
                else:
                    tower.current_combat_aviation_spawn_delay -= 1    
        # endregion

        # region Troop Logic
        to_remove = []
        for k,troop in troops.items():
            for i in range(len(troop.attack_names)):
                target = troop.find_target(screen, enemies)
                if troop.current_delays[i] <= 0 and troop.damages[i]:
                    if target:
                        if type(target) is list:
                            total_damage = sum(min(troop.damages[i], t.health) for t in target)                            
                        else:
                            total_damage = min(troop.damages[i], target.health)
                        money += total_damage
                        killed_list = troop.attack(i, screen, target)
                        troop.total_damage += total_damage
                        if killed_list:
                            for killed in killed_list:
                                killed.kill(grid)
                                # special case for TrojanHorse
                                if type(killed) == TrojanHorse:
                                    for i in range(3):
                                        new_enemy = Infiltrator()
                                        new_enemy.place((killed.x-i+1,GRID_HEIGHT//2), grid, enemy_num)
                                        enemies[enemy_num] = new_enemy
                                        enemy_num += 1
                                enemies.pop(killed.num)
                else:
                    troop.current_delays[i] -= 1
                if not target:
                    success = troop.walk(grid, selected_map)
                    if not success:
                        print(f"{troop.name} died")
                        to_remove.append(k)
                        troop.kill(grid)
                    else:
                        # if a troop runs into an enemy
                        for enemy in enemies.values():
                            if troop.rect.colliderect(enemy.rect) and (type(troop) != CombatAviation or (type(troop) == CombatAviation and not enemy.air_flag)):
                                print(f"{troop.name} runs into {enemy.name}")
                                damage = min(troop.health, enemy.health)
                                killed_troop = troop.take_damage(damage)
                                killed_enemy = enemy.damage(damage)
                                if killed_troop:
                                    to_remove.append(k)
                                    killed_troop.kill(grid)
                                if killed_enemy:
                                    killed_enemy.kill(grid)
                                    enemies.pop(killed_enemy.num)
                        pygame.draw.rect(screen, troop.color, troop.rect)

        for k in to_remove:
            troops.pop(k)
        # endregion

        # region Enemy Logic
        to_remove = []
        for k,enemy in enemies.items():
            success = enemy.walk(grid, selected_map)
            if not success:
                health -= enemy.health
                enemy.kill(grid)
                to_remove.append(k)
            else:
                # if an enemy runs into a troop
                for troop in troops.values():
                    if troop.rect.colliderect(enemy.rect) and (type(troop) != CombatAviation or (type(troop) == CombatAviation and not enemy.air_flag)):
                        damage = min(troop.health, enemy.health)
                        killed_troop = troop.take_damage(damage)
                        killed_enemy = enemy.damage(damage)
                        if killed_troop:
                            killed_troop.kill(grid)
                            troops.pop(killed_troop.num)
                        if killed_enemy:
                            health -= enemy.health
                            enemy.kill(grid)
                            to_remove.append(k)
                pygame.draw.rect(screen, enemy.color, enemy.rect)
        for k in to_remove:
            enemies.pop(k)
        
        to_remove_enemy = []
        for k,enemy in enemies.items():
            to_remove_status = []
            for status in enemy.status_effects:
                killed = status.game_tick(screen, enemy)
                if killed:
                    to_remove_enemy.append(k)
                elif status.duration <= 0:
                    to_remove_status.append(status)
            for status in to_remove_status:
                enemy.status_effects.remove(status)
        for k in to_remove_enemy:
            enemies.pop(k)

        enemy_timer-=1
        # endregion
            
        # region Hover Logic
        if not placing and not tower_info_menu:
            mouse_pos = pygame.mouse.get_pos()
            for tower in towers.values():
                if tower.rect.collidepoint(mouse_pos):
                    draw_circle_alpha(screen, COLOR.CAN_PLACE, (tower.x*CELL_SIZE, tower.y*CELL_SIZE), tower.ranges[0]*CELL_SIZE)
            for enemy in enemies.values():
                if enemy.rect.collidepoint(mouse_pos):
                    draw_enemy_bar(screen, enemy, fonts)
            for troop in troops.values():
                if troop.rect.collidepoint(mouse_pos):
                    draw_enemy_bar(screen, troop, fonts)
                    draw_circle_alpha(screen, COLOR.CAN_PLACE, (troop.x*CELL_SIZE, troop.y*CELL_SIZE), troop.ranges[0]*CELL_SIZE)
        # endregion

        # region Tower Info
        if tower_info_menu:
            draw_rect_alpha(screen, COLOR.FADE, darken_screen_rect)
            pygame.draw.rect(screen, COLOR.BROWN, menu_rect)
            pygame.draw.rect(screen, tower_info_menu.color, tower_display_rect)
            pygame.draw.rect(screen, COLOR.RED, tower_info_exit_button)
            pygame.draw.rect(screen, COLOR.RED, tower_info_sell_button)
            pygame.draw.line(screen, (0, 0, 0),
                        (tower_info_exit_button.left + 5, tower_info_exit_button.top + 5),
                        (tower_info_exit_button.right - 5, tower_info_exit_button.bottom - 5), 3)
            pygame.draw.line(screen, (0, 0, 0),
                        (tower_info_exit_button.left + 5, tower_info_exit_button.bottom - 5),
                        (tower_info_exit_button.right - 5, tower_info_exit_button.top + 5), 3)
            pygame.draw.rect(screen, COLOR.FAINT, tower_info_upgrade_button)
            info_lines = tower_info_menu.info.split('\n')
            for i, line in enumerate(info_lines):
                attribute_text = emojis.render(line, True, COLOR.WHITE)
                screen.blit(attribute_text, (menu_rect.x + 10, menu_rect.y + 35 + i*20))
            tower_text = fontm.render(f"{tower_info_menu.name} Level {tower_info_menu.upgrade_level}", True, COLOR.WHITE)
            screen.blit(tower_text, (menu_rect.x + 10, menu_rect.y + 10))
            upgrade_text = fonts.render(tower_info_menu.upgrade_name, True, COLOR.BLACK)
            cost_display_text = f"Cost: {int(tower_info_menu.upgrade_cost*tower_info_menu.discount_multiplier)}" if tower_info_menu.upgrade_cost else "Max Upgrade"
            cost_text = fonts.render(cost_display_text, True, COLOR.BLACK)
            screen.blit(upgrade_text, (tower_info_upgrade_button.x + 5, tower_info_upgrade_button.y + 5))
            screen.blit(cost_text, (tower_info_upgrade_button.x + 5, tower_info_upgrade_button.y + 17))
            pygame.draw.rect(screen, COLOR.FAINT, tower_info_target_button)
            target_text = fonts.render(f"{tower_info_menu.targeting}", True, COLOR.BLACK)
            screen.blit(target_text, (tower_info_target_button.x + 5, tower_info_target_button.y + 5))
            total_damage_text = fonts.render(f"Total Damage: {tower_info_menu.total_damage}", True, COLOR.BLACK)
            screen.blit(total_damage_text, (tower_display_rect.x, tower_display_rect.y + 100))
            sell_text = fonts.render(f"Sell ${tower_info_menu.total_cost//2}", True, COLOR.BLACK)
            screen.blit(sell_text, (tower_info_sell_button.x + 5, tower_info_sell_button.y + 5))
        # endregion

        # region Tower Placement
        if placing:
            mouse_pos = pygame.mouse.get_pos()
            placing_tower_rect.topleft = (mouse_pos[0] - placing_tower_rect.width // 2,
                                          mouse_pos[1] - placing_tower_rect.height // 2)
            tower = selected_tower()
            

            # Check if the placement is valid (not on the track and no overlap with existing towers)
            # Implement your own validation logic
            valid,grids = validate_tower_placement(mouse_pos, tower, grid, path_coords)

            # Draw tower in red if placement is not valid
            if not valid:
                draw_circle_alpha(screen, COLOR.CANT_PLACE, mouse_pos, tower.ranges[0]*CELL_SIZE)
            else:
                draw_circle_alpha(screen, COLOR.CAN_PLACE, mouse_pos, tower.ranges[0]*CELL_SIZE)
            draw_rect_alpha(screen, tower.color, placing_tower_rect)

            # Check if the left mouse button is released to place the tower
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if valid and tower.cost <= money:
                    money -= tower.cost
                    towers[tower_num] = tower
                    place_tower(grids, grid, tower, tower_num)
                    tower_num += 1
                    if type(tower) == Farm:
                        farms.append(tower)
                    for other_tower in towers.values():
                        if type(other_tower) == Artisan or type(other_tower) == Bard:
                            other_tower.init_effects(towers)
                    print(f"Placed new tower: {tower.name}, tower count: {len(towers)}")

                placing = False
        # endregion
        # region Level Logic
        if not seed.get(level) and not enemies:
            level += 1
            money += 100 + int(level**1.5) + sum(farm.money for farm in farms)
            enemy_spawn_time = None

        if level == seed.get("final_level")+1:
            won = True
        # endregion

        pygame.display.flip()
        clock.tick(FPS)
    
    # States
    # game_over = False
    # won = False
    # paused = False
    # placing = False
    # tower_info_menu = None
    # selected_tower = None
    # level = 1
    # enemy_timer = 0
    # enemy_spawn_time = None
    # autorun = False
    # health = 100
    # money = 500

    # trackers
    tower_num = 0
    troop_num = 0
    enemy_num = 0
    towers = dict()
    enemies = dict()
    farms = []
    return GameState.RESULTS,won,level,time