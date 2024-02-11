import pygame
import numpy as np
import random
from constants import GRID_HEIGHT,GRID_WIDTH,CELL_SIZE,SIDEBAR_WIDTH,FPS
from utils import COLOR, GameState, Map, Targeting, Unicode, draw_circle_alpha, draw_polygon_alpha, draw_rect_alpha
from Tower import Tower, Warrior, Archer, Deadeye, Berserker, Assassin, Gunslinger, Dragoon, Farm, Electrocutioner
# from Enemy import Enemy, , Speedy, Slow, Tough
from enemy_seeds.normal import seed

def draw_enemy_bar(screen, enemy, font):
    enemy_name_text = font.render(enemy.name, True, COLOR.WHITE)
    screen.blit(enemy_name_text, (enemy.x * CELL_SIZE, enemy.y * CELL_SIZE - 20))

    # Draw health bar
    health_bar_rect = pygame.Rect(enemy.x * CELL_SIZE, enemy.y * CELL_SIZE - 10,
                                  enemy.width * CELL_SIZE, 5)
    pygame.draw.rect(screen, COLOR.GREEN, health_bar_rect)  # Assuming green for health
    red_width = int((1 - enemy.health / enemy.max_health) * health_bar_rect.width)
    red_part_rect = health_bar_rect.inflate(red_width, 0)
    pygame.draw.rect(screen, COLOR.RED, red_part_rect)

def validate_tower_placement(mouse_pos, selected_tower, grid, WIDTH, HEIGHT):
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

    # Towers
    warrior_button = pygame.Rect(WIDTH-125, 80, 100, 50)
    archer_button = pygame.Rect(WIDTH-125, 135, 100, 50)
    deadeye_button = pygame.Rect(WIDTH-125, 190, 100, 50)
    berserker_button = pygame.Rect(WIDTH-125, 245, 100, 50)
    assassin_button = pygame.Rect(WIDTH-125, 300, 100, 50)
    gunslinger_button = pygame.Rect(WIDTH-125, 355, 100, 50)
    dragoon_button = pygame.Rect(WIDTH-125, 410, 100, 50)
    farm_button = pygame.Rect(WIDTH-125, 465, 100, 50)
    electrocutioner_button = pygame.Rect(WIDTH-125, 520, 100, 50)
    warrior = Warrior()
    archer = Archer()
    deadeye = Deadeye()
    berserker = Berserker()
    assassin = Assassin()
    gunslinger = Gunslinger()
    dragoon = Dragoon()
    farm = Farm()
    electrocutioner = Electrocutioner()

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
    money = 500 # 500

    # trackers
    tower_num = 0
    enemy_num = 0
    towers = dict()
    enemies = dict()
    farms = []

    # conversion
    tower_color = {0: map.background, 1:COLOR.GREEN, 2:COLOR.RED, 3:COLOR.PURPLE, 4:COLOR.BLUE, 5:COLOR.BLACK,
                   101:COLOR.DARK_GREEN, 102:COLOR.DARK_BLUE, 103:COLOR.DARK_RED}

    while not won:
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
                enemy_num = 0
                towers = dict()
                enemies = dict()
                farms = []
                return GameState.MENU,False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
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
                elif gunslinger_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = Gunslinger
                elif dragoon_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = Dragoon
                elif farm_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = Farm
                elif electrocutioner_button.collidepoint(event.pos):
                    placing = True
                    selected_tower = Electrocutioner
                else:
                    if tower_info_menu:
                        if tower_info_exit_button.collidepoint(event.pos):
                            tower_info_menu = False
                            print("Closed info menu")
                        elif tower_info_upgrade_button.collidepoint(event.pos):
                            cost = tower_info_menu.upgrade_next(money)
                            print("Attempted to upgrade")
                            if cost:
                                money -= cost
                                print("Upgraded successfully")
                        elif tower_info_target_button.collidepoint(event.pos):
                            tower_info_menu.targeting = target_cycle.get(tower_info_menu.targeting)
                            print("Changing targeting")
                    elif not placing:
                        for tower in towers.values():
                            if tower.rect.collidepoint(event.pos):
                                tower_info_menu = tower
                                print("Opened info menu")
                                break
                    
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
                elif event.key == pygame.K_6:
                    placing = True
                    selected_tower = Gunslinger
                elif event.key == pygame.K_7:
                    placing = True
                    selected_tower = Dragoon
                elif event.key == pygame.K_8:
                    placing = True
                    selected_tower = Farm
                elif event.key == pygame.K_9:
                    placing = True
                    selected_tower = Electrocutioner
                elif event.key == pygame.K_q:
                    placing = False

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
            money = 5000 # 500

            # trackers
            tower_num = 0
            enemy_num = 0
            towers = dict()
            enemies = dict()
            farms = []
            return GameState.MENU,won    
        
        pygame.display.set_caption(f"{map.name}: LEVEL {level}")
        
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

        # Warrior
        pygame.draw.rect(screen, COLOR.GREEN, warrior_button)
        warrior_text = fonts.render("Warrior", True, COLOR.WHITE)
        screen.blit(warrior_text, (warrior_button.x+13, warrior_button.y+10))
        warrior_cost = fonts.render(f"${warrior.cost}", True, COLOR.WHITE)
        screen.blit(warrior_cost, (warrior_button.x+13, warrior_button.y+30))

        # Archer
        pygame.draw.rect(screen, COLOR.RED, archer_button)
        archer_text = fonts.render("Archer", True, COLOR.WHITE)
        screen.blit(archer_text, (archer_button.x+13, archer_button.y+10))
        archer_cost = fonts.render(f"${archer.cost}", True, COLOR.WHITE) 
        screen.blit(archer_cost, (archer_button.x + 13, archer_button.y + 30))

        # Deadeye
        pygame.draw.rect(screen, COLOR.PURPLE, deadeye_button)
        deadeye_text = fonts.render("Deadeye", True, COLOR.WHITE)
        screen.blit(deadeye_text, (deadeye_button.x+13, deadeye_button.y+10))
        deadeye_cost = fonts.render(f"${deadeye.cost}", True, COLOR.WHITE)
        screen.blit(deadeye_cost, (deadeye_button.x + 13, deadeye_button.y + 30))

        # Berserker
        pygame.draw.rect(screen, COLOR.BLUE, berserker_button)
        berserker_text = fonts.render("Berserker", True, COLOR.WHITE)
        screen.blit(berserker_text, (berserker_button.x+13, berserker_button.y+10))
        berserker_cost = fonts.render(f"${berserker.cost}", True, COLOR.WHITE) 
        screen.blit(berserker_cost, (berserker_button.x + 13, berserker_button.y + 30))

        # Assassin
        pygame.draw.rect(screen, COLOR.BLACK, assassin_button)
        assassin_text = fonts.render("Assassin", True, COLOR.WHITE)
        screen.blit(assassin_text, (assassin_button.x+13, assassin_button.y+10))
        assassin_cost = fonts.render(f"${assassin.cost}", True, COLOR.WHITE) 
        screen.blit(assassin_cost, (assassin_button.x + 13, assassin_button.y + 30))

        # Gunslinger
        pygame.draw.rect(screen, COLOR.ORANGE, gunslinger_button)
        gunslinger_text = fonts.render("Gunslinger", True, COLOR.WHITE)
        screen.blit(gunslinger_text, (gunslinger_button.x + 13, gunslinger_button.y + 10))
        gunslinger_cost = fonts.render(f"${gunslinger.cost}", True, COLOR.WHITE)  
        screen.blit(gunslinger_cost, (gunslinger_button.x + 13, gunslinger_button.y + 30))

        # Dragoon 
        pygame.draw.rect(screen, COLOR.PURPLE, dragoon_button)
        dragoon_text = fonts.render("Dragoon", True, COLOR.WHITE)
        screen.blit(dragoon_text, (dragoon_button.x + 13, dragoon_button.y + 10))
        dragoon_cost = fonts.render(f"${dragoon.cost}", True, COLOR.WHITE) 
        screen.blit(dragoon_cost, (dragoon_button.x + 13, dragoon_button.y + 30))

        # Farm
        pygame.draw.rect(screen, COLOR.FAINT, farm_button)
        farm_text = fonts.render("Farm", True, COLOR.BLACK)
        screen.blit(farm_text, (farm_button.x + 13, farm_button.y + 10))
        farm_cost = fonts.render(f"${farm.cost}", True, COLOR.BLACK) 
        screen.blit(farm_cost, (farm_button.x + 13, farm_button.y + 30))

        # Farm
        pygame.draw.rect(screen, COLOR.DARK_TEAL, electrocutioner_button)
        electrocutioner_text = fonts.render("Electrocutioner", True, COLOR.WHITE)
        screen.blit(electrocutioner_text, (electrocutioner_button.x + 13, electrocutioner_button.y + 10))
        electrocutioner_cost = fonts.render(f"${electrocutioner.cost}", True, COLOR.WHITE) 
        screen.blit(electrocutioner_cost, (electrocutioner_button.x + 13, electrocutioner_button.y + 30))


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
        # for row in range(GRID_HEIGHT):
        #     for col in range(GRID_WIDTH):
        #         cell_value = grid[row, col]
        #         pygame.draw.rect(screen, tower_color[cell_value], (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for tower in towers.values():
            pygame.draw.rect(screen, tower.color, tower.rect)

        for tower in towers.values():
            if tower.current_delay <= 0 and tower.damage:
                target = tower.find_target(screen, enemies)
                if target:
                    if type(target) is list:
                        total_damage = sum(min(tower.damage, t.health) for t in target)                            
                    else:
                        total_damage = min(tower.damage, target.health)
                    money += total_damage
                    if type(tower) == Gunslinger:
                        money += tower.money
                    killed_list = tower.attack(screen, target)
                    tower.total_damage += total_damage
                    if killed_list:
                        for killed in killed_list:
                            killed.kill(grid)
                            enemies.pop(killed.num)
            else:
                tower.current_delay -= 1

        to_remove = []
        for k,enemy in enemies.items():
            success = enemy.walk(grid)
            if not success:
                health -= enemy.health
                enemy.kill(grid)
                to_remove.append(k)
            else:
                pygame.draw.rect(screen, enemy.color, enemy.rect)
            
        if not placing and not tower_info_menu:
            mouse_pos = pygame.mouse.get_pos()
            for tower in towers.values():
                if tower.rect.collidepoint(mouse_pos):
                    draw_circle_alpha(screen, COLOR.CAN_PLACE, (tower.x*CELL_SIZE, tower.y*CELL_SIZE), tower.range*CELL_SIZE)
            for enemy in enemies.values():
                if enemy.rect.collidepoint(mouse_pos):
                    draw_enemy_bar(screen, enemy, fonts)

        
        for k in to_remove:
            enemies.pop(k)

        if tower_info_menu:
            draw_rect_alpha(screen, COLOR.FADE, darken_screen_rect)
            pygame.draw.rect(screen, COLOR.BROWN, menu_rect)
            pygame.draw.rect(screen, tower_info_menu.color, tower_display_rect)
            pygame.draw.rect(screen, COLOR.RED, tower_info_exit_button)
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
            upgrade_text = fonts.render(f"UPGRADE", True, COLOR.BLACK)
            cost_display_text = f"Cost: {tower_info_menu.upgrade_cost}" if tower_info_menu.upgrade_cost else "Max Upgrade"
            cost_text = fonts.render(cost_display_text, True, COLOR.BLACK)
            screen.blit(upgrade_text, (tower_info_upgrade_button.x + 5, tower_info_upgrade_button.y + 5))
            screen.blit(cost_text, (tower_info_upgrade_button.x + 5, tower_info_upgrade_button.y + 17))
            pygame.draw.rect(screen, COLOR.FAINT, tower_info_target_button)
            target_text = fonts.render(f"{tower_info_menu.targeting}", True, COLOR.BLACK)
            screen.blit(target_text, (tower_info_target_button.x + 5, tower_info_target_button.y + 5))
            total_damage_text = fonts.render(f"Total Damage: {tower_info_menu.total_damage}", True, COLOR.BLACK)
            screen.blit(total_damage_text, (tower_display_rect.x, tower_display_rect.y + 100))


        enemy_timer-=1


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
                if valid and tower.cost <= money:
                    money -= tower.cost
                    towers[tower_num] = tower
                    if type(tower) == Farm:
                        farms.append(tower)
                    place_tower(grids, grid, tower, tower_num)
                    tower_num += 1
                    print(f"Placed new tower: {tower.name}, tower count: {len(towers)}")

                placing = False

        if not seed.get(level) and not enemies:
            level += 1
            money += 100 + int(level**1.5) + sum(farm.money for farm in farms)
            enemy_spawn_time = None

        if level == 26:
            won = True

        pygame.display.flip()
        clock.tick(FPS)
    
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
    enemy_num = 0
    towers = dict()
    enemies = dict()
    farms = []
    return GameState.MENU,won