import pygame
import copy
from numpy import sqrt
from random import choice
from Enemy import Enemy
from utils import COLOR,Targeting,draw_circle_alpha,Unicode
from constants import CELL_SIZE,FPS

class Tower:
    """Base Tower Class
    """

    def __init__(self) -> None:
        self.name = 'Warrior'
        self.cost = 250
        self.total_cost = self.cost

        # flags
        self.invisible_flag = False
        self.metal_flag = False
        self.air_flag = False
        self.boss_multiplier = 0

        # stats
        self.damage = 1                 # health ticks
        self.attack_delay = 20          # frames between attacks
        self.range = 20                 # grid squares
        
        # display
        self.color = COLOR.GREEN        # look
        self.text_color = COLOR.WHITE   # text display color
        self.width = 3                  # number of cells wide
        self.height = 3                 # number of cells tall

        # tracking
        self.id = 1                     # ID number for grid
        self.rect = pygame.Rect(0, 0, self.width * CELL_SIZE, self.height * CELL_SIZE)
        self.total_damage = 0

        # configuration
        self.targeting = Targeting.FIRST   
        self.upgrade_level = 0
        self.upgrade_cost = 0

        # attack
        self.current_delay = self.attack_delay # attack delay counter
        self.attack_color = COLOR.BLACK
        self.attack_type = 0
        self.attack_size = 2
        self.attack_sound = pygame.mixer.Sound('sounds/throw.ogg')

        # secondary attacks
        self.secondary_damages = []
        self.secondary_attack_delays = []
        self.current_secondary_delays = self.secondary_attack_delays
        self.secondary_attack_sounds = []
        self.secondary_attack_colors = []
        self.secondary_attack_sizes = []
        self.secondary_attack_radii = []

    @property
    def info(self):
        first_line = ""
        if self.invisible_flag:
            first_line += Unicode.invisible_detection  
        if self.metal_flag:
            first_line += Unicode.metal
        if self.air_flag:
            first_line += Unicode.air 
        if self.boss_multiplier:
            first_line += Unicode.boss
        if first_line:
            first_line += "\n"
        return f"{first_line}{Unicode.damage} {self.damage}\n{Unicode.delay} {round(self.attack_delay/FPS, 2)}\n{Unicode.range} {self.range}"

    def place(self, x, y, num) -> None:
        self.x = x
        self.y = y
        self.num = num

        self.rect.center = (self.x * CELL_SIZE, self.y * CELL_SIZE)

    def attack(self, screen, enemy: Enemy) -> None:
        start_pos = ((self.x+0.5)*CELL_SIZE, self.y*CELL_SIZE)
        end_pos = ((enemy.x + 0.5 + enemy.width // 2)*CELL_SIZE, (enemy.y + enemy.height // 2)*CELL_SIZE)
        self.attack_sound.play()
        pygame.draw.line(screen, self.attack_color, start_pos, end_pos, self.attack_size)
        self.current_delay = self.attack_delay
        damage = self.damage
        if enemy.boss_flag:
            damage *= self.boss_multiplier
        killed = enemy.damage(damage)
        if killed:
            return [killed]
        return None
    
    def secondary_attack(self, idx, screen, enemy: Enemy) -> None:
        start_pos = ((self.x+0.5)*CELL_SIZE, self.y*CELL_SIZE)
        end_pos = ((enemy.x + 0.5 + enemy.width // 2)*CELL_SIZE, (enemy.y + enemy.height // 2)*CELL_SIZE)
        self.secondary_attack_sounds[idx].play()
        pygame.draw.line(screen, self.secondary_attack_colors[idx], start_pos, end_pos, self.secondary_attack_sizes[idx])
        self.current_secondary_delays[idx] = self.secondary_attack_delays[idx]
        damage = self.secondary_damages[idx]
        if enemy.boss_flag:
            damage *= self.boss_multiplier
        killed = enemy.damage(damage)
        if killed:
            return [killed]
        return None

    def can_attack(self, enemy: Enemy):
        if enemy.invisible_flag and not self.invisible_flag:
            return False
        if enemy.air_flag and not self.air_flag:
            return False
        if enemy.metal_flag and not self.metal_flag:
            return False
        return True

    def find_target(self, screen, enemies):
        distances = {
            k: sqrt(((max(enemy.x, min(self.x, enemy.x + enemy.width))) - self.x) ** 2 +
                    ((max(enemy.y, min(self.y, enemy.y + enemy.height))) - self.y) ** 2)
            for k, enemy in enemies.items()
        }

        targets_in_range = [k for k, distance in distances.items() if distance <= self.range and self.can_attack(enemies[k])]
        if targets_in_range:
            if self.targeting == Targeting.FIRST:
                target_key = max(targets_in_range, key=lambda k: enemies[k].x)
            elif self.targeting == Targeting.STRONG:
                target_key = max(targets_in_range, key=lambda k: enemies[k].health)
            elif self.targeting == Targeting.LAST:
                target_key = min(targets_in_range, key=lambda k: enemies[k].x)
            elif self.targeting == Targeting.WEAK:
                target_key = min(targets_in_range, key=lambda k: enemies[k].health)
            else:
                target_key = choice(targets_in_range)
            return enemies[target_key]

        return None  # No target found within the tower's range
        
    def set_targeting(self, targeting: Targeting):
        self.targeting = targeting

    def upgrade_next(self, money):
        if self.upgrade_level == 0 and 0 < self.upgrade_cost <= money:
            cost = self.upgrade_cost
            self.upgrade1()
            return cost
        elif self.upgrade_level == 1 and 0 < self.upgrade_cost <= money:
            cost = self.upgrade_cost
            self.upgrade2()
            return cost
        elif self.upgrade_level == 2 and 0 < self.upgrade_cost <= money:
            cost = self.upgrade_cost
            self.upgrade3()
            return cost
        elif self.upgrade_level == 3 and 0 < self.upgrade_cost <= money:
            cost = self.upgrade_cost
            self.upgrade4()
            return cost
        elif self.upgrade_level == 4 and 0 < self.upgrade_cost <= money:
            cost = self.upgrade_cost
            self.upgrade5()
            return cost
        else:
            return 0

    def upgrade1(self):
        self.total_cost += self.upgrade_cost
        self.upgrade_level = 1

    def upgrade2(self):
        self.total_cost += self.upgrade_cost
        self.upgrade_level = 2

    def upgrade3(self):
        self.total_cost += self.upgrade_cost
        self.upgrade_level = 3

    def upgrade4(self):
        self.total_cost += self.upgrade_cost
        self.upgrade_level = 4

    def upgrade5(self):
        self.total_cost += self.upgrade_cost
        self.upgrade_level = 5

    def __str__(self):
        return self.name
        

class Warrior(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.upgrade_cost = 50

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 200
        self.range = 23
        self.attack_delay = 16

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 500
        self.damage = 2
        self.range = 25
        self.attack_sound = pygame.mixer.Sound('sounds/metalimpact3.ogg')

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 0
        self.damage = 4
        self.attack_delay = 10
        self.range = 27
        self.invisible_flag = True
        self.attack_sound = pygame.mixer.Sound('sounds/metalimpact1.ogg')


class Archer(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Archer'
        self.cost = 350
        self.total_cost = self.cost
        self.damage = 2
        self.attack_delay = 45
        self.range = 25
        self.air_flag = True
        self.color = COLOR.RED
        self.id = 2
        self.upgrade_cost = 150
        self.attack_sound = pygame.mixer.Sound('sounds/hit1.ogg')

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 350
        self.damage = 3
        self.attack_delay = 35
        self.range = 30

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 1000
        self.damage = 7

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 0
        self.damage = 25
        self.attack_delay = 45
        self.range = 35
        self.attack_sound = pygame.mixer.Sound('sounds/auto.ogg')
    

class Deadeye(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Deadeye'
        self.cost = 600
        self.total_cost = self.cost
        self.damage = 5
        self.attack_delay = 120
        self.range = 45
        self.invisible_flag = True
        self.air_flag = True
        self.color = COLOR.GRAY
        self.id = 3
        self.upgrade_cost = 400
        self.attack_sound = pygame.mixer.Sound('sounds/hit3.ogg')

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 1000
        self.damage = 15
        self.attack_delay = 110

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 2000
        self.damage = 35
        self.attack_delay = 95
        self.attack_size = 3

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 4000
        self.damage = 50
        self.attack_delay = 65

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 0
        self.damage = 250
        self.attack_delay = 90
        self.attack_size = 4
        self.metal_flag = True

class Berserker(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Berserker'
        self.cost = 800
        self.total_cost = self.cost
        self.damage = 1
        self.base_delay = 45
        self.delay_changes = {6: self.base_delay, 7: 0, 8: 0, 9: 0, 10: 0} # {6: 30, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        self.range_changes = {10: 6, 6: 7, 7: 8, 8: 9, 9: 10} # {30: 3, 3: 6, 6: 9, 9: 12, 12: 15, 15: 18, 18: 21, 21: 24, 24: 27, 27: 30}
        self.attack_delay = 45
        self.range = 10
        self.temp_range = 6
        self.color = COLOR.BLUE
        self.id = 4
        self.upgrade_cost = 200
        self.attack_color = COLOR.FAINT_BLUE
        self.attack_sound = pygame.mixer.Sound('sounds/electric_zap.ogg')

    @property
    def info(self):
        first_line = ""
        if self.invisible_flag:
            first_line += Unicode.invisible_detection  
        if self.metal_flag:
            first_line += Unicode.metal
        if self.air_flag:
            first_line += Unicode.air 
        if self.boss_multiplier:
            first_line += Unicode.boss
        if first_line:
            first_line += "\n"
        return f"{first_line}{Unicode.damage} {self.damage}\n{Unicode.delay} {round(self.base_delay/FPS, 2)}\n{Unicode.range} {self.range}\n{Unicode.pulse_range} {len(self.delay_changes)}"

    def attack_round(self, screen):
        self.attack_sound.play()
        draw_circle_alpha(screen, self.attack_color, (self.x*CELL_SIZE, self.y*CELL_SIZE), self.temp_range*CELL_SIZE)
        self.temp_range = self.range_changes.get(self.temp_range)
        self.attack_delay = self.delay_changes.get(self.temp_range)
        self.current_delay = self.attack_delay

    def attack(self, screen, enemies: list) -> list:
        self.attack_round(screen)

        killed_list = []
        for enemy in enemies:
            killed = enemy.damage(self.damage)
            if killed:
                killed_list.append(killed)
        return killed_list
    
    def find_target(self, screen, enemies):
        # distances = {
        #     k: sqrt(((max(enemy.x, min(self.x, enemy.x + enemy.width))) - self.x) ** 2 +
        #             ((max(enemy.y, min(self.y, enemy.y + enemy.height))) - self.y) ** 2)
        #     for k, enemy in enemies.items()
        # }
        targets_in_range = [enemy for k, enemy in enemies.items() if self.can_attack(enemy) and sqrt(((max(enemy.x, min(self.x, enemy.x + enemy.width))) - self.x) ** 2 +
                    ((max(enemy.y, min(self.y, enemy.y + enemy.height))) - self.y) ** 2) <= self.range]

        # targets_in_range = [k for k, distance in distances.items() if distance <= self.range]

        if targets_in_range:
            return targets_in_range

        if self.temp_range != 6:
            self.attack_round(screen)

        return None  # No target found within the tower's range

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 500
        self.delay_changes = {6: self.base_delay, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0} # {6: 30, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        self.range_changes = {12: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12} # {30: 3, 3: 6, 6: 9, 9: 12, 12: 15, 15: 18, 18: 21, 21: 24, 24: 27, 27: 30}

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 3500
        self.base_delay = 40
        self.range = 12
        self.air_flag = True

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 7000
        self.damage = 2
        self.delay_changes = {6: self.base_delay, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0} # {6: 30, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        self.range_changes = {15: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15} # {30: 3, 3: 6, 6: 9, 9: 12, 12: 15, 15: 18, 18: 21, 21: 24, 24: 27, 27: 30}
        self.metal_flag = True
        self.attack_sound = pygame.mixer.Sound('sounds/missile-blast.ogg')

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 0
        self.damage = 5
        self.delay_changes = {6: self.base_delay, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0} # {6: 30, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        self.range_changes = {20: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15, 15: 16, 16: 17, 17: 18, 18: 19, 19: 20} # {30: 3, 3: 6, 6: 9, 9: 12, 12: 15, 15: 18, 18: 21, 21: 24, 24: 27, 27: 30}
        self.boss_multiplier = 2

class Assassin(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Assassin'
        self.cost = 400
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 10
        self.invisible_flag = True
        self.range = 15
        self.color = COLOR.BLACK
        self.id = 5
        self.upgrade_cost = 100
        self.attack_sound = pygame.mixer.Sound('sounds/hit4.ogg')

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 500
        self.range = 17
        self.attack_delay = 9
        self.air_flag = True

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 2000
        self.damage = 2
        self.attack_delay = 8

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 4000
        self.damage = 4
        self.range = 20
        self.attack_delay = 7
        self.attack_sound = pygame.mixer.Sound('sounds/hit6.ogg')

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 0
        self.damage = 8
        self.attack_delay = 3

class Gunslinger(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Gunslinger'
        self.cost = 600
        self.total_cost = self.cost
        self.damage = 5
        self.attack_delay = 50
        self.range = 20
        self.money = 3
        self.boss_multiplier = 2
        self.color = COLOR.ORANGE
        self.id = 6
        self.upgrade_cost = 100
        self.attack_sound = pygame.mixer.Sound('sounds/pistol1.ogg')

    @property
    def info(self):
        first_line = ""
        if self.invisible_flag:
            first_line += Unicode.invisible_detection  
        if self.metal_flag:
            first_line += Unicode.metal
        if self.air_flag:
            first_line += Unicode.air 
        if self.boss_multiplier:
            first_line += Unicode.boss
        if first_line:
            first_line += "\n"
        return f"{first_line}{Unicode.damage} {self.damage}\n{Unicode.delay} {round(self.attack_delay/FPS, 2)}\n{Unicode.range} {self.range}\n{Unicode.dollar} {self.money}"

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 250
        self.money = 5
        self.attack_sound = pygame.mixer.Sound('sounds/shotgun1.ogg')

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 2000
        self.air_flag = True
        self.damage = 7
        self.boss_multiplier = 3
        self.attack_sound = pygame.mixer.Sound('sounds/pistol2.ogg')

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 5000
        self.damage = 15
        self.attack_delay = 40
        self.range = 23
        self.boss_multiplier = 5
        self.attack_sound = pygame.mixer.Sound('sounds/shotgunreload1.ogg')

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 7500
        self.range = 25
        self.money = 15
        self.attack_sound = pygame.mixer.Sound('sounds/shotgunreload2.ogg')

    def upgrade5(self):
        super().upgrade4()
        self.upgrade_cost = 0
        self.damage = 30
        self.attack_delay = 30
        self.range = 30
        self.money = 30
        self.boss_multiplier = 10
        self.attack_sound = pygame.mixer.Sound('sounds/shotgunreload3.ogg')

class Dragoon(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Dragoon'
        self.cost = 1500
        self.total_cost = self.cost
        self.damage = 10
        self.attack_delay = 60
        self.attack_radius = 5
        self.range = 32
        self.metal_flag = True
        self.color = COLOR.PURPLE
        self.attack_color = COLOR.DARK_PURPLE
        self.id = 7
        self.upgrade_cost = 750
        self.attack_sound = pygame.mixer.Sound('sounds/firework.ogg')

    @property
    def info(self):
        first_line = ""
        if self.invisible_flag:
            first_line += Unicode.invisible_detection  
        if self.metal_flag:
            first_line += Unicode.metal
        if self.air_flag:
            first_line += Unicode.air 
        if self.boss_multiplier:
            first_line += Unicode.boss
        if first_line:
            first_line += "\n"
        return f"{first_line}{Unicode.damage} {self.damage}\n{Unicode.delay} {round(self.attack_delay/FPS, 2)}\n{Unicode.range} {self.range}\n{Unicode.explosion} {self.attack_radius}"

    def attack(self, screen, enemies: list) -> None:
        enemy = enemies[0]
        start_pos = ((self.x+0.5)*CELL_SIZE, self.y*CELL_SIZE)
        end_pos = ((enemy.x + 0.5 + enemy.width // 2)*CELL_SIZE, (enemy.y + enemy.height // 2)*CELL_SIZE)
        pygame.draw.line(screen, self.attack_color, start_pos, end_pos, 2)
        self.attack_sound.play()
        draw_circle_alpha(screen, self.attack_color, end_pos, self.attack_radius*CELL_SIZE)
        self.current_delay = self.attack_delay
        killed_list = []
        for enemy in enemies:
            killed = enemy.damage(self.damage)
            if killed:
                killed_list.append(killed)
        return killed_list

    def find_target(self, screen, enemies):
        distances = {
            k: sqrt(((max(enemy.x, min(self.x, enemy.x + enemy.width))) - self.x) ** 2 +
                    ((max(enemy.y, min(self.y, enemy.y + enemy.height))) - self.y) ** 2)
            for k, enemy in enemies.items()
        }
        target = None

        targets_in_range = [k for k, distance in distances.items() if distance <= self.range and self.can_attack(enemies[k])]
        if targets_in_range:
            if self.targeting == Targeting.FIRST:
                target_key = max(targets_in_range, key=lambda k: enemies[k].x)
            elif self.targeting == Targeting.STRONG:
                target_key = max(targets_in_range, key=lambda k: enemies[k].health)
            elif self.targeting == Targeting.LAST:
                target_key = min(targets_in_range, key=lambda k: enemies[k].x)
            elif self.targeting == Targeting.WEAK:
                target_key = min(targets_in_range, key=lambda k: enemies[k].health)
            else:
                target_key = choice(targets_in_range)
            target = enemies[target_key]
        if target:
            targets = [target]
            targetx = target.x + target.width // 2
            targety = target.y + target.height // 2
            new_distances = {
                k: sqrt(((max(enemy.x, min(targetx, enemy.x + enemy.width))) - targetx) ** 2 +
                        ((max(enemy.y, min(targety, enemy.y + enemy.height))) - targety) ** 2)
                for k, enemy in enemies.items()
            }
            new_targets_in_range = [k for k, distance in new_distances.items() if distance <= self.attack_radius and k != target.num]
            return targets + [enemies[k] for k in new_targets_in_range]

        return None  # No target found within the tower's range

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 1500
        self.attack_delay = 50
        self.range = 35

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 4000
        self.damage = 20
        self.attack_radius = 8

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 10000
        self.damage = 45
        self.range = 38
        self.attack_sound = pygame.mixer.Sound('sounds/proton.ogg')

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 25000
        self.air_flag = True
        self.damage = 90
        self.attack_delay = 90
        self.attack_radius = 13

    def upgrade5(self):
        super().upgrade4()
        self.upgrade_cost = 0
        self.damage = 200
        self.attack_radius = 15
        self.range = 40

class Farm(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Farm'
        self.cost = 200
        self.total_cost = self.cost
        self.damage = 0
        self.attack_delay = -1
        self.range = 3
        self.color = COLOR.LIGHT
        self.text_color = COLOR.BLACK
        self.id = 8
        self.upgrade_cost = 150
        self.money = 50

    @property
    def info(self):
        return f"{Unicode.money} {self.money}"

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 200
        self.money = 100

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 750
        self.money = 200

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 2500
        self.money = 500

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 7500
        self.money = 1000

    def upgrade5(self):
        super().upgrade5()
        self.upgrade_cost = 0
        self.money = 2500

class Electrocutioner(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Electrocutioner"
        self.cost = 750
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_TEAL
        self.attack_color = COLOR.TEAL
        self.id = 9
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

    @property
    def info(self):
        first_line = ""
        if self.invisible_flag:
            first_line += Unicode.invisible_detection  
        if self.metal_flag:
            first_line += Unicode.metal
        if self.air_flag:
            first_line += Unicode.air 
        if self.boss_multiplier:
            first_line += Unicode.boss
        if first_line:
            first_line += "\n"
        return f"{first_line}{Unicode.damage} {self.damage}\n{Unicode.delay} {round(self.attack_delay/FPS, 2)}\n{Unicode.range} {self.range}\n{Unicode.link} {self.max_targets}\n{Unicode.targets} {self.attack_radius}\n{Unicode.stun} {round(self.stun_delay/FPS, 2)}s"

    def attack(self, screen, enemies: list) -> None:
        enemy = enemies[0]
        start_pos = ((self.x+0.5)*CELL_SIZE, self.y*CELL_SIZE)
        killed_list = []
        for enemy in enemies:
            enemy.current_delay += self.stun_delay
            end_pos = ((enemy.x + 0.5 + enemy.width // 2)*CELL_SIZE, (enemy.y + enemy.height // 2)*CELL_SIZE)
            pygame.draw.line(screen, self.attack_color, start_pos, end_pos, 2)
            self.attack_sound.play()
            killed = enemy.damage(self.damage)
            if killed:
                killed_list.append(killed)
            start_pos = end_pos
        self.current_delay = self.attack_delay
        return killed_list

    def find_target(self, screen, enemies):
        temp_enemies = copy.deepcopy(enemies)
        distances = {
            k: sqrt(((max(enemy.x, min(self.x, enemy.x + enemy.width))) - self.x) ** 2 +
                    ((max(enemy.y, min(self.y, enemy.y + enemy.height))) - self.y) ** 2)
            for k, enemy in temp_enemies.items()
        }
        target = None

        targets_in_range = [k for k, distance in distances.items() if distance <= self.range and self.can_attack(enemies[k])]
        if targets_in_range:
            if self.targeting == Targeting.FIRST:
                target_key = max(targets_in_range, key=lambda k: enemies[k].x)
            elif self.targeting == Targeting.STRONG:
                target_key = max(targets_in_range, key=lambda k: enemies[k].health)
            elif self.targeting == Targeting.LAST:
                target_key = min(targets_in_range, key=lambda k: enemies[k].x)
            elif self.targeting == Targeting.WEAK:
                target_key = min(targets_in_range, key=lambda k: enemies[k].health)
            else:
                target_key = choice(targets_in_range)
            target = enemies[target_key]
            temp_enemies.pop(target_key)
        if target:
            targets = [target]
            done = False
            while not done and len(temp_enemies) and len(targets) < self.max_targets:
                targetx = target.x + target.width // 2
                targety = target.y + target.height // 2
                new_distances = {
                    k: sqrt(((max(enemy.x, min(targetx, enemy.x + enemy.width))) - targetx) ** 2 +
                            ((max(enemy.y, min(targety, enemy.y + enemy.height))) - targety) ** 2)
                    for k, enemy in temp_enemies.items() if k != target.num
                }
                if new_distances:
                    closest = min(new_distances, key=new_distances.get)
                    if new_distances[closest] <= self.attack_radius:
                        target = enemies[closest]
                        targets.append(target)
                        temp_enemies.pop(target.num)
                    else:
                        done = True
                else:
                    done = True
            return targets

        return None  # No target found within the tower's range


    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 750
        self.attack_delay = 55
        self.attack_radius = 5
        self.range = 17

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 3000
        self.damage = 2
        self.air_flag = True
        self.max_targets = 5

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 7500
        self.damage = 8
        self.attack_radius = 7
        self.stun_delay = 15
        self.range = 20
        self.attack_sound = pygame.mixer.Sound('sounds/laser.ogg')

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 20000
        self.damage = 12
        self.max_targets = 10

    def upgrade5(self):
        super().upgrade4()
        self.upgrade_cost = 0
        self.damage = 20
        self.attack_radius = 10
        self.max_targets = 10000
        self.stun_delay = 20
        self.range = 22
        self.attack_sound = pygame.mixer.Sound('sounds/strong_laser.ogg')

class Bard(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Bard"
        self.cost = 1500
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_TEAL
        self.attack_color = COLOR.TEAL
        self.id = 10
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

class Mage(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Mage"
        self.cost = 600
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_TEAL
        self.attack_color = COLOR.TEAL
        self.id = 11
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

class Artisan(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Artisan"
        self.cost = 900
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_TEAL
        self.attack_color = COLOR.TEAL
        self.id = 12
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

    

class General(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "General"
        self.cost = 2 # 2000
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_TEAL
        self.attack_color = COLOR.DARK_GRAY
        self.id = 13
        self.upgrade_cost = 1 # 1000
        self.attack_sound = pygame.mixer.Sound('sounds/pistol1.ogg')
        # Infantry
        self.total_infantry_spawn_delay = 450
        self.current_infantry_spawn_delay = self.total_infantry_spawn_delay
        self.spawn_infantry = True
        self.infantry_level = 1
        # Armored Infantry
        self.total_armored_infantry_spawn_delay = 600
        self.current_armored_infantry_spawn_delay = self.total_armored_infantry_spawn_delay
        self.spawn_armored_infantry = False
        self.armored_infantry_level = 1
        # Artillery
        self.total_artillery_spawn_delay = 900
        self.current_artillery_spawn_delay = self.total_artillery_spawn_delay
        self.spawn_artillery = False
        self.artillery_level = 1
        # Combat Aviation
        self.total_combat_aviation_spawn_delay = 1200
        self.current_combat_aviation_spawn_delay = self.total_combat_aviation_spawn_delay
        self.spawn_combat_aviation = False
        self.combat_aviation_level = 1

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 1 # 2000
        self.attack_delay = 50
        self.spawn_armored_infantry = True
        self.total_infantry_spawn_delay = 300
        self.infantry_level = 2

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 1 # 5000
        self.attack_delay = 40
        self.damage = 2
        self.spawn_artillery = True

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 1 # 10000
        self.attack_delay = 30
        self.spawn_combat_aviation = True
        self.total_infantry_spawn_delay = 200
        self.total_armored_infantry_spawn_delay = 400
        self.infantry_level = 3
        self.armored_infantry_level = 2

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 0
        self.attack_delay = 20
        self.damage = 5
        self.total_infantry_spawn_delay = 150
        self.total_armored_infantry_spawn_delay = 300
        self.total_artillery_spawn_delay = 600
        self.total_combat_aviation_spawn_delay = 800
        self.infantry_level = 4
        self.armored_infantry_level = 3
        self.artillery_level = 2
        self.combat_aviation_level = 2

class Troop(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Troop"
        self.total_walk_delay = 5
        self.current_walk_delay = self.total_walk_delay
        self.max_health = 10
        self.health = self.max_health
        self.damage = 1
        self.attack_delay = 30
        self.current_delay = self.attack_delay
        self.range = 10
        self.invisible_flag = True
        self.color = COLOR.DARK_TEAL
        self.attack_color = COLOR.DARK_GRAY
        self.id = 14
        self.attack_sound = pygame.mixer.Sound('sounds/pistol1.ogg')

    def set_progress(self, path) -> None:
        self.path_progress = len(path) - 1

    def walk(self, grid, selected_map) -> bool:
        if self.current_walk_delay <= 0:
            if self.x == selected_map.start[0] and self.y == selected_map.start[1] or self.path_progress == -1:
                print("Troop has reached the end of the path")
                return False
            grid[self.y:self.y+self.height+1, self.x:self.x+self.width+1] = 0
            self.x -= selected_map.path[self.path_progress][0]
            self.y -= selected_map.path[self.path_progress][1]
            grid[self.y:self.y+self.height+1, self.x:self.x+self.width+1] = self.id
            self.current_walk_delay = self.total_walk_delay
            self.path_progress -= 1
            return True
        self.current_walk_delay -= 1
        self.rect.topleft = (self.x * CELL_SIZE, self.y * CELL_SIZE)
        return True
    
    def kill(self, grid):
        grid[self.y:self.y+self.height+1, self.x:self.x+self.width+1] = 0

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return self
        else:
            return None

class Infantry(Troop):
    def __init__(self, level) -> None:
        super().__init__()
        self.name = "Infantry"
        self.max_health = 10+10*(level - 1)
        self.health = self.max_health
        self.damage = 1*level
        self.attack_delay = 30-3*(level - 1)
        self.current_delay = self.attack_delay
        self.range = 10+2*(level - 1)
        self.color = COLOR.LIGHT

class ArmoredInfantry(Troop):
    def __init__(self, level) -> None:
        super().__init__()
        self.name = "Armored Infantry"
        self.max_health = 35+35*(level - 1)
        self.health = self.max_health
        self.damage = 2*level
        self.total_walk_delay = 8
        self.current_walk_delay = self.total_walk_delay
        self.attack_delay = 30-3*(level - 1)
        self.current_delay = self.attack_delay
        self.range = 10+2*(level - 1)
        self.color = COLOR.DARK_GRAY

class Artillery(Troop):
    def __init__(self, level) -> None:
        super().__init__()
        self.name = "Artillery"
        self.damage = 50+25*(level - 1)
        self.attack_delay = 100-10*(level - 1)
        self.current_delay = self.attack_delay
        self.max_health = 100+60*(level - 1)
        self.total_walk_delay = 12
        self.range = 30
        self.current_walk_delay = self.total_walk_delay
        self.health = self.max_health
        self.metal_flag = True
        self.air_flag = True
        self.color = COLOR.DARK_GREEN

class CombatAviation(Troop):
    def __init__(self, level) -> None:
        super().__init__()
        self.name = "Combat Aviation"
        self.damage = 25+15*(level - 1)
        self.attack_delay = 10-1*(level - 1)
        self.current_delay = self.attack_delay
        self.range = 25
        self.total_walk_delay = 3
        self.current_walk_delay = self.total_walk_delay
        self.metal_flag = True
        self.air_flag = True
        self.color = COLOR.GRAY

        self.secondary_damages = [200+100*(level - 1)]
        self.secondary_attack_delays = [50-3*(level - 1)]
        self.current_secondary_delays = self.secondary_attack_delays
        self.secondary_attack_sounds = [pygame.mixer.Sound('sounds/firework.ogg')]
        self.secondary_attack_colors = [COLOR.RED]
        self.secondary_attack_sizes = [4]
        self.secondary_attack_radii = [5]

    def secondary_attack(self, idx, screen, enemies: list) -> None:
        enemy = enemies[0]
        start_pos = ((self.x+0.5)*CELL_SIZE, self.y*CELL_SIZE)
        end_pos = ((enemy.x + 0.5 + enemy.width // 2)*CELL_SIZE, (enemy.y + enemy.height // 2)*CELL_SIZE)
        pygame.draw.line(screen, self.secondary_attack_colors[idx], start_pos, end_pos, 2)
        self.secondary_attack_sounds[idx].play()
        draw_circle_alpha(screen, self.secondary_attack_colors[idx], end_pos, self.secondary_attack_radii[idx]*CELL_SIZE)
        self.current_secondary_delays[idx] = self.secondary_attack_delays[idx]
        killed_list = []
        for enemy in enemies:
            killed = enemy.damage(self.secondary_damages[idx])
            if killed:
                killed_list.append(killed)
        return killed_list
    
    def secondary_find_target(self, idx, screen, enemies):
        distances = {
            k: sqrt(((max(enemy.x, min(self.x, enemy.x + enemy.width))) - self.x) ** 2 +
                    ((max(enemy.y, min(self.y, enemy.y + enemy.height))) - self.y) ** 2)
            for k, enemy in enemies.items()
        }
        target = None

        targets_in_range = [k for k, distance in distances.items() if distance <= self.range and self.can_attack(enemies[k])]
        if targets_in_range:
            if self.targeting == Targeting.FIRST:
                target_key = max(targets_in_range, key=lambda k: enemies[k].x)
            elif self.targeting == Targeting.STRONG:
                target_key = max(targets_in_range, key=lambda k: enemies[k].health)
            elif self.targeting == Targeting.LAST:
                target_key = min(targets_in_range, key=lambda k: enemies[k].x)
            elif self.targeting == Targeting.WEAK:
                target_key = min(targets_in_range, key=lambda k: enemies[k].health)
            else:
                target_key = choice(targets_in_range)
            target = enemies[target_key]
        if target:
            targets = [target]
            targetx = target.x + target.width // 2
            targety = target.y + target.height // 2
            new_distances = {
                k: sqrt(((max(enemy.x, min(targetx, enemy.x + enemy.width))) - targetx) ** 2 +
                        ((max(enemy.y, min(targety, enemy.y + enemy.height))) - targety) ** 2)
                for k, enemy in enemies.items()
            }
            new_targets_in_range = [k for k, distance in new_distances.items() if distance <= self.secondary_attack_radii[idx] and k != target.num]
            return targets + [enemies[k] for k in new_targets_in_range]

        return None  # No target found within the tower's range

class Alchemist(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Alchemist"
        self.cost = 1100
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_PURPLE
        self.attack_color = COLOR.PURPLE
        self.id = 15
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

class PlagueDoctor(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Plague Doctor"
        self.cost = 1300
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_PURPLE
        self.attack_color = COLOR.PURPLE
        self.id = 14
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

class Toxicologist(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Toxicologist"
        self.cost = 1500
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_PURPLE
        self.attack_color = COLOR.PURPLE
        self.id = 15
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

class Pyromancer(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Pyromancer"
        self.cost = 1200
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.ORANGE
        self.attack_color = COLOR.LIGHT_ORANGE
        self.id = 16
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

class Hypnotist(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Hypnotist"
        self.cost = 700
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.PINK
        self.attack_color = COLOR.LIGHT_PURPLE
        self.id = 15
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

class Butcher(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Butcher"
        self.cost = 900
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_RED
        self.attack_color = COLOR.RED
        self.id = 17
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

class Blacksmith(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Blacksmith"
        self.cost = 1100
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_RED
        self.attack_color = COLOR.RED
        self.id = 18
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

class Miner(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Miner"
        self.cost = 450
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.BROWN
        self.attack_color = COLOR.DARK_ORANGE
        self.id = 16
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

class Detonator(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Detonator"
        self.cost = 800
        self.total_cost = self.cost
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 3
        self.max_targets = 3
        self.stun_delay = 10
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_ORANGE
        self.attack_color = COLOR.ORANGE
        self.id = 17
        self.upgrade_cost = 250
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

if __name__ == "__main__":
    # print(Warrior().color)
    print(Tower(), Warrior())