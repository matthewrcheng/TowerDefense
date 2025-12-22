import pygame
import copy
from numpy import sqrt
from random import choice
from Enemy import Enemy
from Status import *
from utils import COLOR,Targeting,draw_circle_alpha,Unicode,Attacking
from constants import CELL_SIZE,FPS

pygame.mixer.init(44100, -16,2,2048)

# region Base Tower
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
        self.upgrade_name = "Placeholder"

        # attack
        self.attack_names = ['Normal']
        self.attack_types = [Attacking.MELEE]
        self.attack_functions = [self.normal_attack]
        self.attack_statuses = [None]
        self.targeting_functions = [self.find_single_target]
        self.damages = [1]                 # health ticks
        self.attack_delays = [20]          # frames between attacks
        self.ranges = [20]                 # grid squares
        self.current_delays = [0]
        self.attack_colors = [COLOR.BLACK]
        self.attack_sizes = [2]
        self.attack_sounds = [pygame.mixer.Sound('sounds/throw.ogg')]
        self.attack_radii = [0]
        self.delay_changes = {}
        self.range_changes = {}
        self.max_targets = -1
        self.stun_delay = 0

        # misc
        self.needs_screen = False

        # modifiers
        self.attack_speed_multiplier = 1.05
        self.attack_range_multiplier = 1.0
        self.attack_damage_boost_addend = 0
        self.attack_damage_boost_multiplier = 1.0
        self.money_multiplier = 1.0
        self.discount_multiplier = 1

    def set_name(self, name: str):
        self.name = name

    def set_cost(self, cost: int):
        self.cost = cost

    def set_total_cost(self, cost: int):
        self.total_cost = cost

    def set_color(self, color: tuple):
        self.color = color

    def set_text_color(self, color: tuple):
        self.text_color = color

    def set_id(self, id: int):
        self.id = id

    def set_upgrade_cost(self, cost: int):
        self.upgrade_cost = cost

    def set_upgrade_name(self, name: str):
        self.upgrade_name = name

    def set_invisible_flag(self, flag: bool):
        self.invisible_flag = flag

    def set_metal_flag(self, flag: bool):
        self.metal_flag = flag

    def set_air_flag(self, flag: bool):
        self.air_flag = flag

    def set_boss_multiplier(self, multiplier: int):
        self.boss_multiplier = multiplier

    def set_attack_name(self, name: str, idx: int=0):
        self.attack_names[idx] = name

    def set_attack_type(self, type: str, idx: int=0):
        self.attack_types[idx] = type

    def set_attack_function(self, attack: callable, idx: int=0):
        self.attack_functions[idx] = attack

    def set_targeting_function(self, targeting: callable, idx: int=0):
        self.targeting_functions[idx] = targeting

    def set_damage(self, damage: int, idx: int=0):
        self.damages[idx] = damage

    def set_attack_delay(self, delay: int, idx: int=0):
        self.attack_delays[idx] = delay

    def set_range(self, new_range: int, idx: int=0):
        self.ranges[idx] = new_range

    def set_ranges(self, new_range: int):
        for i in range(len(self.ranges)):
            self.ranges[i] = new_range

    def set_attack_color(self, color: tuple, idx: int=0):
        self.attack_colors[idx] = color

    def set_attack_size(self, size: int, idx: int=0):
        self.attack_sizes[idx] = size

    def set_attack_sound(self, sound: pygame.mixer.Sound, idx: int=0):
        self.attack_sounds[idx] = sound

    def set_attack_radius(self, radius: int, idx: int=0):
        self.attack_radii[idx] = radius

    def set_attack_status(self, status: Status, idx: int=0):
        self.attack_statuses[idx] = status

    def add_attack(self, attack: callable, targeting: callable, name: str='Normal', type: str=Attacking.MELEE, damage: int=1, delay: int=20, attack_range: int=10,
                   color: tuple=COLOR.BLACK, size: int=1, sound: pygame.mixer.Sound=pygame.mixer.Sound('sounds/boop.ogg'), radius: int=0, status=None):
        self.attack_names.append(name)
        self.attack_types.append(type)
        self.attack_functions.append(attack)
        self.targeting_functions.append(targeting)    
        self.damages.append(damage)
        self.attack_delays.append(delay)
        self.current_delays.append(0)
        self.ranges.append(attack_range)
        self.attack_colors.append(color)
        self.attack_sizes.append(size)
        self.attack_sounds.append(sound)
        self.attack_radii.append(radius)
        self.attack_statuses.append(status)

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
        return f"{first_line}{Unicode.damage} {round((self.damages[0]*self.attack_damage_boost_multiplier)+self.attack_damage_boost_addend)}\n{Unicode.delay} {round((self.attack_delays[0]/self.attack_speed_multiplier)/FPS, 2)}\n{Unicode.range} {(round(self.ranges[0]*self.attack_range_multiplier, 2))}"

    def place(self, x: int, y: int, num: int) -> None:
        self.x = x
        self.y = y
        self.num = num

        self.rect.center = (self.x * CELL_SIZE, self.y * CELL_SIZE)

    def attack(self, idx: int, screen: pygame.Surface, enemy: Enemy) -> None:
        return self.attack_functions[idx](idx, screen, enemy)

    def normal_attack(self, idx: int, screen: pygame.Surface, enemy: Enemy):
        start_pos = ((self.x+0.5)*CELL_SIZE, self.y*CELL_SIZE)
        end_pos = ((enemy.x + 0.5 + enemy.width // 2)*CELL_SIZE, (enemy.y + enemy.height // 2)*CELL_SIZE)
        self.attack_sounds[idx].play()
        pygame.draw.line(screen, self.attack_colors[idx], start_pos, end_pos, self.attack_sizes[idx])
        self.current_delays[idx] = self.attack_delays[idx]
        damage = self.damages[idx]
        if enemy.boss_flag:
            damage *= self.boss_multiplier
        damage *= self.attack_damage_boost_multiplier
        damage += self.attack_damage_boost_addend
        killed = enemy.damage(damage)
        if killed:
            return [killed]
        elif self.attack_statuses[idx]:
            # loop through enemy's statuses and determine if it already has this status
            has_status = False
            for status in enemy.status_effects:
                if status.name == self.attack_statuses[idx].name:
                    has_status = True
                    break
            if not has_status:
                enemy.status_effects.append(copy.deepcopy(self.attack_statuses[idx]))
        return None
    
    def multi_attack(self, idx: int, screen: pygame.Surface, enemies: list[Enemy]):
        enemy: Enemy = enemies[0]
        start_pos = ((self.x+0.5)*CELL_SIZE, self.y*CELL_SIZE)
        end_pos = ((enemy.x + 0.5 + enemy.width // 2)*CELL_SIZE, (enemy.y + enemy.height // 2)*CELL_SIZE)
        pygame.draw.line(screen, self.attack_colors[idx], start_pos, end_pos, 2)
        self.attack_sounds[idx].play()
        draw_circle_alpha(screen, self.attack_colors[idx], end_pos, self.attack_radii[idx]*CELL_SIZE)
        self.current_delays[idx] = self.attack_delays[idx]
        killed_list = []
        for enemy in enemies:
            damage = self.damages[idx]
            if enemy.boss_flag:
                damage *= self.boss_multiplier
            damage *= self.attack_damage_boost_multiplier
            damage += self.attack_damage_boost_addend
            killed = enemy.damage(damage)
            if killed:
                killed_list.append(killed)
            elif self.attack_statuses[idx]:
                # loop through enemy's statuses and determine if it already has this status
                has_status = False
                for status in enemy.status_effects:
                    if status.name == self.attack_statuses[idx].name:
                        has_status = True
                        break
                if not has_status:
                    enemy.status_effects.append(self.attack_statuses[idx])
        return killed_list
    
    def chain_attack(self, idx: int, screen: pygame.Surface, enemies: list[Enemy]):
        enemy = enemies[0]
        start_pos = ((self.x+0.5)*CELL_SIZE, self.y*CELL_SIZE)
        killed_list = []
        for enemy in enemies:
            enemy.current_delay += self.stun_delay
            end_pos = ((enemy.x + 0.5 + enemy.width // 2)*CELL_SIZE, (enemy.y + enemy.height // 2)*CELL_SIZE)
            pygame.draw.line(screen, self.attack_colors[idx], start_pos, end_pos, 2)
            self.attack_sounds[idx].play()
            damage = self.damages[idx]
            if enemy.boss_flag:
                damage *= self.boss_multiplier
            damage *= self.attack_damage_boost_multiplier
            damage += self.attack_damage_boost_addend
            killed = enemy.damage(damage)
            if killed:
                killed_list.append(killed)
            elif self.attack_statuses[idx]:
                # loop through enemy's statuses and determine if it already has this status
                has_status = False
                for status in enemy.status_effects:
                    if status.name == self.attack_statuses[idx].name:
                        has_status = True
                        break
                if not has_status:
                    enemy.status_effects.append(self.attack_statuses[idx])
            start_pos = end_pos
        self.current_delays[idx] = self.attack_delays[idx]
        return killed_list
    
    def berserker_attack_round(self, idx: int, screen: pygame.Surface):
        self.attack_sounds[idx].play()
        draw_circle_alpha(screen, self.attack_colors[idx], (self.x*CELL_SIZE, self.y*CELL_SIZE), self.temp_range*CELL_SIZE)
        self.temp_range = self.range_changes.get(self.temp_range)
        self.attack_delays[idx] = self.delay_changes.get(self.temp_range)
        self.current_delays[idx] = self.attack_delays[idx]

    def berserker_attack(self, idx: int, screen, enemies: list[Enemy]) -> list:
        self.berserker_attack_round(idx, screen)

        killed_list = []
        for enemy in enemies:
            killed = enemy.damage((self.damages[idx]*self.attack_damage_boost_multiplier) + self.attack_damage_boost_addend)
            if killed:
                killed_list.append(killed)
            elif self.attack_statuses[idx]:
                # loop through enemy's statuses and determine if it already has this status
                has_status = False
                for status in enemy.status_effects:
                    if status.name == self.attack_statuses[idx].name:
                        has_status = True
                        break
                if not has_status:
                    enemy.status_effects.append(self.attack_statuses[idx])
        return killed_list

    def can_attack(self, enemy: Enemy):
        if enemy.invisible_flag and not self.invisible_flag:
            return False
        if enemy.air_flag and not self.air_flag:
            return False
        if enemy.metal_flag and not self.metal_flag:
            return False
        return True
    
    def find_target(self, idx: int, enemies: dict[int, Enemy], screen: pygame.Surface = None):
        if self.needs_screen:
            return self.targeting_functions[idx](idx, screen, enemies)    
        return self.targeting_functions[idx](idx, enemies)

    def find_single_target(self, idx: int, enemies: dict[int, Enemy]):
        distances = {
            k: sqrt(((max(enemy.x, min(self.x, enemy.x + enemy.width))) - self.x) ** 2 +
                    ((max(enemy.y, min(self.y, enemy.y + enemy.height))) - self.y) ** 2)
            for k, enemy in enemies.items()
        }

        targets_in_range = [k for k, distance in distances.items() if distance <= (self.ranges[idx]*self.attack_range_multiplier) and self.can_attack(enemies[k])]
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
    
    def find_multi_target(self, idx: int, enemies: dict[int, Enemy]):
        distances = {
            k: sqrt(((max(enemy.x, min(self.x, enemy.x + enemy.width))) - self.x) ** 2 +
                    ((max(enemy.y, min(self.y, enemy.y + enemy.height))) - self.y) ** 2)
            for k, enemy in enemies.items()
        }
        target = None

        targets_in_range = [k for k, distance in distances.items() if distance <= (self.ranges[idx]*self.attack_range_multiplier) and self.can_attack(enemies[k])]
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
            new_targets_in_range = [k for k, distance in new_distances.items() if distance <= self.attack_radii[idx] and k != target.num]
            return targets + [enemies[k] for k in new_targets_in_range]

        return None  # No target found within the tower's range
    
    def find_chain_target(self, idx: int, enemies: dict[int, Enemy]):
        temp_enemies = copy.deepcopy(enemies)
        distances = {
            k: sqrt(((max(enemy.x, min(self.x, enemy.x + enemy.width))) - self.x) ** 2 +
                    ((max(enemy.y, min(self.y, enemy.y + enemy.height))) - self.y) ** 2)
            for k, enemy in temp_enemies.items()
        }
        target = None

        targets_in_range = [k for k, distance in distances.items() if distance <= (self.ranges[idx]*self.attack_range_multiplier) and self.can_attack(enemies[k])]
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
                    if new_distances[closest] <= self.attack_radii[idx]:
                        target = enemies[closest]
                        targets.append(target)
                        temp_enemies.pop(target.num)
                    else:
                        done = True
                else:
                    done = True
            return targets

        return None  # No target found within the tower's range
    
    def berserker_find_target(self, idx: int, screen: pygame.Surface, enemies: dict[int, Enemy]):
        targets_in_range = [enemy for k, enemy in enemies.items() if self.can_attack(enemy) and sqrt(((max(enemy.x, min(self.x, enemy.x + enemy.width))) - self.x) ** 2 +
                    ((max(enemy.y, min(self.y, enemy.y + enemy.height))) - self.y) ** 2) <= (self.ranges[idx]*self.attack_range_multiplier)]

        if targets_in_range:
            return targets_in_range

        if self.temp_range != 6:
            self.berserker_attack_round(idx, screen)

        return None  # No target found within the tower's range
        
    def set_targeting(self, targeting: Targeting):
        self.targeting = targeting

    def upgrade_next(self, money: int):
        upgrade_cost = int(self.upgrade_cost*self.discount_multiplier)
        if self.upgrade_level == 0 and 0 < upgrade_cost <= money:
            cost = upgrade_cost
            self.upgrade1()
            return cost
        elif self.upgrade_level == 1 and 0 < upgrade_cost <= money:
            cost = upgrade_cost
            self.upgrade2()
            return cost
        elif self.upgrade_level == 2 and 0 < upgrade_cost <= money:
            cost = upgrade_cost
            self.upgrade3()
            return cost
        elif self.upgrade_level == 3 and 0 < upgrade_cost <= money:
            cost = upgrade_cost
            self.upgrade4()
            return cost
        elif self.upgrade_level == 4 and 0 < upgrade_cost <= money:
            cost = upgrade_cost
            self.upgrade5()
            return cost
        else:
            return 0

    def upgrade1(self):
        upgrade_cost = int(self.upgrade_cost*self.discount_multiplier)
        self.total_cost += upgrade_cost
        self.upgrade_level = 1

    def upgrade2(self):
        upgrade_cost = int(self.upgrade_cost*self.discount_multiplier)
        self.total_cost += upgrade_cost
        self.upgrade_level = 2

    def upgrade3(self):
        upgrade_cost = int(self.upgrade_cost*self.discount_multiplier)
        self.total_cost += upgrade_cost
        self.upgrade_level = 3

    def upgrade4(self):
        upgrade_cost = int(self.upgrade_cost*self.discount_multiplier)
        self.total_cost += upgrade_cost
        self.upgrade_level = 4

    def upgrade5(self):
        upgrade_cost = int(self.upgrade_cost*self.discount_multiplier)
        self.total_cost += upgrade_cost
        self.upgrade_level = 5

    def __str__(self):
        return self.name
    
    def remove_effects(self, towers):
        pass

# endregion    
# region Warrior
class Warrior(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.set_upgrade_cost(50)
        self.set_upgrade_name("Sharpened Focus")

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(200)
        self.set_upgrade_name("Battle Hardened")
        self.set_range(23)
        self.set_attack_delay(16)

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(500)
        self.set_upgrade_name("Elite Warrior")
        self.set_damage(2)
        self.set_range(25)
        self.set_attack_sound(pygame.mixer.Sound('sounds/metalimpact3.ogg'))

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(0)
        self.set_damage(4)
        self.set_attack_delay(10)
        self.set_range(27)
        self.set_invisible_flag(True)
        self.set_attack_sound(pygame.mixer.Sound('sounds/metalimpact1.ogg'))
# endregion
# region Archer
class Archer(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.set_name('Archer')
        self.set_cost(350)
        self.set_total_cost(self.cost)
        self.set_damage(2)
        self.set_attack_delay(45)
        self.set_range(25)
        self.set_air_flag(True)
        self.set_color(COLOR.RED)
        self.set_id(2)
        self.set_upgrade_cost(150)
        self.set_upgrade_name("Steady Aim")
        self.set_attack_sound(pygame.mixer.Sound('sounds/hit1.ogg'))

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(350)
        self.set_upgrade_name("Piercing Shot")
        self.set_damage(3)
        self.set_attack_delay(35)
        self.set_range(30)

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(1000)
        self.set_upgrade_name("Deadly Marksman")
        self.set_damage(7)

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(0)
        self.set_damage(25)
        self.set_attack_delay(45)
        self.set_range(35)
        self.set_attack_sound(pygame.mixer.Sound('sounds/auto.ogg'))
# endregion
# region Deadeye
class Deadeye(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.set_name('Deadeye')
        self.set_cost(600)
        self.set_total_cost(self.cost)
        self.set_damage(5)
        self.set_attack_delay(120)
        self.set_range(45)
        self.set_invisible_flag(True)
        self.set_air_flag(True)
        self.set_color(COLOR.GRAY)
        self.set_id(3)
        self.set_upgrade_cost(400)
        self.set_upgrade_name("Precision Rounds")
        self.set_attack_sound(pygame.mixer.Sound('sounds/hit3.ogg'))

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(1000)
        self.set_upgrade_name("Ballistic Shot")
        self.set_damage(15)
        self.set_attack_delay(110)

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(2000)
        self.set_upgrade_name("Deadzone")
        self.set_damage(35)
        self.set_attack_delay(95)
        self.set_attack_size(3)

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(4000)
        self.set_upgrade_name("Final Judgement")
        self.set_damage(50)
        self.set_attack_delay(65)

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_cost(0)
        self.set_damage(250)
        self.set_attack_delay(90)
        self.set_attack_size(4)
        self.set_metal_flag(True)
# endregion

# region Berserker
class Berserker(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.set_name('Berserker')
        self.set_cost(800)
        self.set_total_cost(self.cost)
        self.set_damage(1)
        self.base_delay = 45
        self.delay_changes = {6: self.base_delay, 7: 0, 8: 0, 9: 0, 10: 0}
        self.range_changes = {10: 6, 6: 7, 7: 8, 8: 9, 9: 10}
        self.set_attack_delay(45)
        self.set_range(10)
        self.temp_range = 6
        self.set_color(COLOR.BLUE)
        self.set_id(4)
        self.set_upgrade_cost(200)
        self.set_upgrade_name("Shock Wave")
        self.set_attack_color(COLOR.FAINT_BLUE)
        self.set_attack_sound(pygame.mixer.Sound('sounds/electric_zap.ogg'))
        self.attack_functions = [self.berserker_attack]
        self.targeting_functions = [self.berserker_find_target]
        self.needs_screen = True

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
        return f"{first_line}{Unicode.damage} {round((self.damages[0]*self.attack_damage_boost_multiplier)+self.attack_damage_boost_addend)}\n{Unicode.delay} {round((self.base_delay/self.attack_speed_multiplier)/FPS, 2)}\n{Unicode.range} {round(self.ranges[0]*self.attack_range_multiplier, 2)}\n{Unicode.pulse_range} {len(self.delay_changes)}"

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(500)
        self.set_upgrade_name("Sonic Frenzy")
        self.delay_changes = {6: self.base_delay, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
        self.range_changes = {12: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12}

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(3500)
        self.set_upgrade_name("Shockstorm")
        self.base_delay = 40
        self.set_range(12)
        self.set_air_flag(True)

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(7000)
        self.set_upgrade_name("Catacalysmic Pulse")
        self.set_damage(2)
        self.delay_changes = {6: self.base_delay, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0} # {6: 30, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        self.range_changes = {15: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15} # {30: 3, 3: 6, 6: 9, 9: 12, 12: 15, 15: 18, 18: 21, 21: 24, 24: 27, 27: 30}
        self.set_metal_flag(True)
        self.set_attack_sound(pygame.mixer.Sound('sounds/missile-blast.ogg'))

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_cost(0)
        self.set_damage(5)
        self.delay_changes = {6: self.base_delay, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0} # {6: 30, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        self.range_changes = {20: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15, 15: 16, 16: 17, 17: 18, 18: 19, 19: 20} # {30: 3, 3: 6, 6: 9, 9: 12, 12: 15, 15: 18, 18: 21, 21: 24, 24: 27, 27: 30}
        self.set_boss_multiplier(2)
# endregion

# region Assassin
class Assassin(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.set_name('Assassin')
        self.set_cost(400)
        self.set_total_cost(self.cost)
        self.set_damage(1)
        self.set_attack_delay(10)
        self.set_invisible_flag(True)
        self.set_range(15)
        self.set_color(COLOR.BLACK)
        self.set_id(5)
        self.set_upgrade_cost(100)
        self.set_upgrade_name("Aerial Support")
        self.set_attack_sound(pygame.mixer.Sound('sounds/hit4.ogg'))

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(500)
        self.set_upgrade_name("Sharpened Silence")
        self.set_range(17)
        self.set_attack_delay(9)
        self.set_air_flag(True)

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(2000)
        self.set_upgrade_name("Night Reaper")
        self.set_damage(2)
        self.set_attack_delay(8)

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(4000)
        self.set_upgrade_name("Apex Killer")
        self.set_damage(4)
        self.set_range(20)
        self.set_attack_delay(7)
        self.set_attack_sound(pygame.mixer.Sound('sounds/hit6.ogg'))

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_cost(0)
        self.set_damage(8)
        self.set_attack_delay(3)
# endregion

# region Bounty Hunter
class BountyHunter(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Bounty Hunter'
        self.cost = 600
        self.total_cost = self.cost
        self.set_damage(5)
        self.set_attack_delay(50)
        self.set_range(20)
        self.money = 3  # Specific to this class
        self.boss_multiplier = 2
        self.set_color(COLOR.ORANGE)
        self.set_id(6)
        self.set_upgrade_cost(100)
        self.set_upgrade_name("Payback")
        self.set_attack_sound(pygame.mixer.Sound('sounds/pistol1.ogg'))

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
        return f"{first_line}{Unicode.damage} {round((self.damages[0]*self.attack_damage_boost_multiplier)+self.attack_damage_boost_addend)}\n{Unicode.delay} {round((self.attack_delays[0]/self.attack_speed_multiplier)/FPS, 2)}\n{Unicode.range} {(round(self.ranges[0]*self.attack_range_multiplier, 2))}\n{Unicode.dollar} {self.money}"

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(250)
        self.set_upgrade_name("Triggerhawk")
        self.money = 5  # Specific to this class
        self.set_attack_sound(pygame.mixer.Sound('sounds/shotgun1.ogg'))

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(2000)
        self.set_upgrade_name("Elite Outlaw")
        self.set_air_flag(True)
        self.set_damage(7)
        self.set_boss_multiplier(3)
        self.set_attack_sound(pygame.mixer.Sound('sounds/pistol2.ogg'))

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(5000)
        self.set_upgrade_name("The Collector")
        self.set_damage(15)
        self.set_attack_delay(40)
        self.set_range(23)
        self.set_boss_multiplier(5)
        self.set_attack_sound(pygame.mixer.Sound('sounds/shotgunreload1.ogg'))

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_cost(7500)
        self.set_upgrade_name("Wanted Dead or Alive")
        self.set_range(25)
        self.money = 15  # Specific to this class
        self.set_attack_sound(pygame.mixer.Sound('sounds/shotgunreload2.ogg'))

    def upgrade5(self):
        super().upgrade5()
        self.set_upgrade_cost(0)
        self.set_damage(30)
        self.set_attack_delay(30)
        self.set_range(30)
        self.money = 30  # Specific to this class
        self.set_boss_multiplier(10)
        self.set_attack_sound(pygame.mixer.Sound('sounds/shotgunreload3.ogg'))
# endregion

# region Dragoon
class Dragoon(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Dragoon'
        self.cost = 1500
        self.total_cost = self.cost
        self.set_damage(10)
        self.set_attack_delay(60)
        self.set_attack_radius(5)
        self.set_range(32)
        self.metal_flag = True
        self.set_color(COLOR.PURPLE)
        self.set_attack_color(COLOR.DARK_PURPLE)
        self.set_id(7)
        self.set_upgrade_cost(750)
        self.set_upgrade_name("Shockpoint")
        self.set_attack_sound(pygame.mixer.Sound('sounds/firework.ogg'))
        self.set_attack_function(self.multi_attack)  # Custom attack
        self.set_targeting_function(self.find_multi_target)  # Custom targeting

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
        return f"{first_line}{Unicode.damage} {round((self.damages[0]*self.attack_damage_boost_multiplier)+self.attack_damage_boost_addend)}\n{Unicode.delay} {round((self.attack_delays[0]/self.attack_speed_multiplier)/FPS, 2)}\n{Unicode.range} {(round(self.ranges[0]*self.attack_range_multiplier, 2))}\n{Unicode.explosion} {self.attack_radii[0]}"

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(1500)
        self.set_upgrade_name("Blastframe")
        self.set_attack_delay(50)
        self.set_range(35)

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(4000)
        self.set_upgrade_name("Ion Cannon")
        self.set_damage(20)
        self.set_attack_radius(8)

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(10000)
        self.set_upgrade_name("Devastating Impact")
        self.set_damage(45)
        self.set_range(38)
        self.set_attack_sound(pygame.mixer.Sound('sounds/proton.ogg'))

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_cost(25000)
        self.set_upgrade_name("Event Horizon")
        self.set_air_flag(True)
        self.set_damage(90)
        self.set_attack_delay(90)
        self.set_attack_radius(13)

    def upgrade5(self):
        super().upgrade5()  # Fixed this, now calls the correct base method
        self.set_upgrade_cost(0)
        self.set_damage(200)
        self.set_attack_radius(15)
        self.set_range(40)
# endregion

# region Farm
class Farm(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Farm'
        self.cost = 200
        self.total_cost = self.cost
        self.set_damage(0)
        self.set_attack_delay(-1)
        self.set_range(3)
        self.set_color(COLOR.LIGHT)
        self.set_text_color(COLOR.BLACK)
        self.set_id(8)
        self.set_upgrade_cost(200)
        self.set_upgrade_name("Cottage Crop")
        self.money = 50  # Specific to this class, leave as assignment

    @property
    def info(self):
        return f"{Unicode.money} {self.money}"

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(400)
        self.set_upgrade_name("Cropstead")
        self.money = 100  # Specific to this class, leave as assignment

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(750)
        self.set_upgrade_name("Golden Acres")
        self.money = 200  # Specific to this class, leave as assignment

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(2500)
        self.set_upgrade_name("Overgrowth")
        self.money = 500  # Specific to this class, leave as assignment

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_cost(7500)
        self.set_upgrade_name("Golden Empire")
        self.money = 1000  # Specific to this class, leave as assignment

    def upgrade5(self):
        super().upgrade5()
        self.set_upgrade_cost(0)
        self.money = 2500  # Specific to this class, leave as assignment
# endregion

# region Electrocutioner
class Electrocutioner(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.set_name("Electrocutioner")
        self.set_cost(750)
        self.set_total_cost(self.cost)
        self.set_damage(1)
        self.set_attack_delay(60)
        self.set_attack_radius(3)
        self.max_targets = 3
        self.stun_delay = 10
        self.set_range(15)
        self.set_metal_flag(True)
        self.set_color(COLOR.DARK_TEAL)
        self.set_attack_color(COLOR.TEAL)
        self.set_id(9)
        self.set_upgrade_cost(250)
        self.set_upgrade_name("Tesla Coil")
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

        # Custom targeting and attacking functions
        self.attack_func = self.chain_attack
        self.target_func = self.find_chain_target

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
        return f"{first_line}{Unicode.damage} {round((self.damages[0]*self.attack_damage_boost_multiplier)+self.attack_damage_boost_addend)}\n{Unicode.delay} {round((self.attack_delays[0]/self.attack_speed_multiplier)/FPS, 2)}\n{Unicode.range} {(round(self.ranges[0]*self.attack_range_multiplier, 2))}\n{Unicode.link} {self.max_targets}\n{Unicode.targets} {self.attack_radii[0]}\n{Unicode.stun} {round(self.stun_delay/FPS, 2)}s"

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(750)
        self.set_upgrade_name("Charged Arc")
        self.set_attack_delay(55)
        self.set_attack_radius(5)
        self.set_range(17)

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(3000)
        self.set_upgrade_name("Lightning Rod")
        self.set_damage(2)
        self.air_flag = True
        self.max_targets = 5

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(7500)
        self.set_upgrade_name("Circuit Overload")
        self.set_damage(8)
        self.set_attack_radius(7)
        self.stun_delay = 15
        self.set_range(20)
        self.attack_sound = pygame.mixer.Sound('sounds/laser.ogg')

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_cost(20000)
        self.set_upgrade_name("Voltaic Storm")
        self.set_damage(12)
        self.max_targets = 10

    def upgrade5(self):
        super().upgrade5()
        self.set_upgrade_cost(0)
        self.set_damage(20)
        self.set_attack_radius(10)
        self.max_targets = 10000
        self.stun_delay = 20
        self.set_range(22)
        self.attack_sound = pygame.mixer.Sound('sounds/strong_laser.ogg')
# endregion

# region Bard
class Bard(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.set_name("Bard")
        self.set_cost(1500)
        self.total_cost = self.cost
        self.set_damage(0)
        self.set_attack_delay(-1)
        self.set_range(10)
        self.set_color(COLOR.DARK_ORANGE)
        self.set_attack_color(COLOR.ORANGE)
        self.set_id(10)
        self.set_upgrade_cost(250)
        self.set_upgrade_name("Bardic Inspiration")
        self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

        # Custom buffing attributes
        self.attack_speed_boost = 1.05
        self.attack_range_boost = 1.0
        self.attack_damage_boost_flat = 0
        self.attack_damage_boost_percent = 1.0
        self.money_boost = 1.0

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(750)
        self.set_upgrade_name("Rhythm of War")
        self.set_range(12)
        self.attack_speed_boost = 1.1
        self.attack_range_boost = 1.1

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(3000)
        self.set_upgrade_name("Ballad of the Hero")
        self.set_range(14)
        self.attack_speed_boost = 1.15
        self.attack_damage_boost_flat = 1
        self.attack_damage_boost_percent = 1.0

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(7500)
        self.set_upgrade_name("Symphony of Victory")
        self.set_range(16)
        self.attack_speed_boost = 1.2
        self.attack_damage_boost_flat = 2
        self.attack_damage_boost_percent = 1.05
        self.attack_range_boost = 1.15

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_cost(0)
        self.set_range(20)
        self.attack_speed_boost = 1.25
        self.attack_damage_boost_flat = 3
        self.attack_damage_boost_percent = 1.1
        self.attack_range_boost = 1.2
        self.money_boost = 1.1

    def init_effects(self, towers: dict[int, Tower]):
        distances = {
            k: sqrt(((tower.x - self.x) ** 2) +
                    ((tower.y - self.y) ** 2))
            for k, tower in towers.items()
        }

        towers_in_range = [k for k, distance in distances.items() if distance <= (self.ranges[0]*self.attack_range_multiplier)]

        for tower in towers_in_range:
            if type(towers[tower]) != Bard:
                towers[tower].attack_speed_multiplier = max(towers[tower].attack_speed_multiplier, self.attack_speed_boost)
                towers[tower].attack_range_multiplier = max(towers[tower].attack_range_multiplier, self.attack_range_boost)
                towers[tower].attack_damage_boost_addend = max(towers[tower].attack_damage_boost_addend, self.attack_damage_boost_flat)
                towers[tower].attack_damage_boost_multiplier = max(towers[tower].attack_damage_boost_multiplier, self.attack_damage_boost_percent)
                towers[tower].money_multiplier = max(towers[tower].money_multiplier, self.money_boost)

    def remove_effects(self, towers: dict[int, Tower]):
        for tower in towers.values():
            towers[tower].attack_speed_multiplier = 1
            towers[tower].attack_range_multiplier = 1
            towers[tower].attack_damage_boost_addend = 0
            towers[tower].attack_damage_boost_multiplier = 1
            towers[tower].money_multiplier = 1

        # in case other artisans are nearby
        for tower in towers.values():
            if type(tower) == Bard:
                tower.init_effects(towers)
# endregion

# region Mage
class Mage(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.set_name("Mage")
        self.set_cost(600)
        self.set_total_cost(self.cost)
        self.set_damage(3)
        self.set_attack_delay(45)
        self.set_range(12)
        self.set_color(COLOR.DARK_BLUE_PURPLE)
        self.set_attack_color(COLOR.BLUE_PURPLE)
        self.set_id(11)
        self.set_upgrade_cost(250)
        self.set_upgrade_name("Arcane Apprentice")
        self.set_attack_sound(pygame.mixer.Sound('sounds/electric_buzz.ogg'))
        self.set_attack_name("Basic Spell")

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(750)
        self.set_upgrade_name("Elemental Initiate")
        self.set_ranges(13)
        self.set_damage(5)
        self.set_attack_delay(40)
        self.add_attack(name='Arcane Bolt', damage=15, delay=120, type=Attacking.CHAIN, attack= self.chain_attack, targeting=self.find_chain_target,
                         sound=pygame.mixer.Sound('sounds/throw.ogg'), attack_range=13, color=COLOR.LIGHT_GREEN, size=3, radius=1)
        self.max_targets = 3

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(3000)
        self.set_upgrade_name("Mystical Adept")

        # Basic Spell
        self.set_damage(8)

        # Arcane Bolt
        self.set_damage(25, 1)
        self.set_attack_delay(90, 1)
        self.max_targets = 4

        # Fireball
        self.add_attack(name='Fireball', damage=8, delay=30, type=Attacking.AOE, attack=self.multi_attack, targeting=self.find_multi_target,
                         sound=pygame.mixer.Sound('sounds/fire.ogg'), color=COLOR.ORANGE, size=2, radius=3, 
                         status=Burn(
                             name='Burn',
                             frequency=30,
                             duration=90,
                             effect=1,
                             color=COLOR.ORANGE,
                             damage=1
                         ))
        
        # Ice Blast
        self.add_attack(name='Ice Blast', damage=15, delay=60, type=Attacking.AOE, attack=self.multi_attack, targeting=self.find_multi_target,
                         sound=pygame.mixer.Sound('sounds/ice3.ogg'), color=COLOR.LIGHT_BLUE, size=3, radius=5, 
                         status=Slow(
                             name='Slow',
                             frequency=1,
                             duration=90,
                             effect=1,
                             color=COLOR.LIGHT_BLUE
                         ))

        # Lightning Bolt
        self.add_attack(name='Lightning Bolt', damage=50, delay=120, type=Attacking.RANGED, attack=self.normal_attack, targeting=self.find_single_target,
                         sound=pygame.mixer.Sound('sounds/electric_zap.ogg'), color=COLOR.YELLOW, size=4, radius=1)

        self.set_ranges(15)

    def upgrade3(self, selection = 0):
        super().upgrade3()
        self.set_upgrade_cost(7500)
        self.selection = selection
        self.set_upgrade_name(["Fire Wizard", "Ice Wizard", "Lightning Wizard"][selection])
        # Basic Spell
        self.set_damage(12)
        self.set_attack_delay(35)

        # Arcane Bolt
        self.set_damage(35, 1)

        # Fireball
        self.set_damage(15, 2)
        self.set_attack_status(Burn(
                                name='Burn',
                                frequency=20,
                                duration=100,
                                effect=1,
                                color=COLOR.ORANGE,
                                damage=1
                            ), 2)

        # Ice Blast
        self.set_damage(25, 3)

        # Lightning Bolt
        self.set_damage(120, 4)

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_cost(20000)

        # Basic Spell
        self.set_damage(20)
        self.set_attack_delay(30)
        self.set_ranges(20)

        if self.selection == 0:
            # Fire Path
            self.set_upgrade_name("Solar Radiation")
            self.set_damage(35, 2)
            self.set_attack_delay(10, 2)
            self.set_attack_status(Burn(
                                name='Burn',
                                frequency=15,
                                duration=105,
                                effect=1,
                                color=COLOR.ORANGE,
                                damage=3
                            ), 2)

        elif self.selection == 1:
            # Ice Path
            self.set_upgrade_name("Absolute Zero")
            self.set_damage(50, 3)
            self.set_attack_delay(20, 3)
            self.set_attack_size(4, 3)
            self.set_attack_radius(7, 3)
            
        elif self.selection == 2:
            # Lightning Path
            self.set_upgrade_name("Overcharged Superbolt")
            self.set_damage(300, 4)
            self.set_attack_delay(60, 4)

    def upgrade5(self):
        super().upgrade5()
        self.set_upgrade_cost(0)
        # Basic Spell
        self.set_damage(50)
        self.set_attack_delay(30)
        if self.selection == 0:
            # Radiation
            self.add_attack(name='Radiation', damage=1, delay=0, type=Attacking.RANGED, attack=self.normal_attack, targeting=self.find_single_target,
                            sound=pygame.mixer.Sound('sounds/fire.ogg'), color=COLOR.RED, size=1, radius=1, 
                            status=Burn(
                                name='Harsh Burn',
                                frequency=5,
                                duration=120,
                                effect=1,
                                color=COLOR.ORANGE,
                                damage=5
                            ))

            # Ice Blast
            self.set_damage(25, 3)

            # Lightning Bolt
            self.set_damage(120, 4)
            
        elif self.selection == 1:
            # Blizzard Bomb
            self.add_attack(name='Blizzard Bomb', damage=100, delay=45, type=Attacking.RANGED, attack=self.multi_attack, targeting=self.find_multi_target,
                            sound=pygame.mixer.Sound('sounds/ice2.ogg'), color=COLOR.WHITE, size=10, radius=10)

            # Fireball
            self.set_damage(15, 2)

            # Lightning Bolt
            self.set_damage(120, 4)
            
        elif self.selection == 2:
            # Superbolt
            self.add_attack(name='Superbolt', damage=1000, delay=120, type=Attacking.RANGED, attack=self.normal_attack, targeting=self.find_single_target,
                            sound=pygame.mixer.Sound('sounds/thunder2.ogg'), color=COLOR.DARK_YELLOW, size=6, radius=1)

            # Fireball
            self.set_damage(15, 2)

            # Ice Blast
            self.set_damage(25, 3)

class Artisan(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.set_name("Artisan")
        self.set_cost(900)
        self.set_total_cost(900)
        self.set_damage(1)
        self.set_attack_delay(60)
        self.set_range(15)
        self.discount = 0.05
        self.set_metal_flag(True)
        self.set_color(COLOR.DARK_YELLOW)
        self.set_attack_color(COLOR.LIGHT_BROWN)
        self.set_upgrade_name("Efficient Production")
        self.set_id(12)
        self.set_upgrade_cost(1000)
        self.set_attack_sound(pygame.mixer.Sound('sounds/electric_buzz.ogg'))

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_cost(3000)
        self.set_upgrade_name("Mercantile Knowledge")
        self.set_attack_delay(50)
        self.set_damage(2)
        self.discount = 0.1

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(7500)
        self.set_upgrade_name("Transparent Dealings")
        self.money = 100  # Specific to this class, leave as assignment
        self.add_attack(name='Coin Toss', damage=5, delay=120, type=Attacking.RANGED, attack=self.multi_attack, targeting=self.find_multi_target,
                        sound=pygame.mixer.Sound('sounds/boop.ogg'), color=COLOR.GOLD, size=3, radius=5)
        self.set_ranges(20)

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(20000)
        self.set_upgrade_name("Crafted Masterpiece")
        self.set_attack_delay(40)
        self.set_damage(4)
        self.set_ranges(23)
        self.discount = 0.15
        # reveal hidden

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_cost(0)
        self.set_attack_delay(30)
        self.set_damage(6)
        self.set_range(25)
        self.discount = 0.25
        # reveal air and metal

    def init_effects(self, towers: dict[int, Tower]):
        distances = {
            k: sqrt(((tower.x - self.x) ** 2) +
                    ((tower.y - self.y) ** 2))
            for k, tower in towers.items()
        }

        towers_in_range = [k for k, distance in distances.items() if distance <= (self.ranges[0]*self.attack_range_multiplier)]

        print(self.id)
        for tower in towers_in_range:
            print(tower)
            if type(towers[tower]) != Artisan:
                print(f"Changed {towers[tower].name} discount multiplier from {towers[tower].discount_multiplier} to {min(1-self.discount, self.discount_multiplier)}")
                towers[tower].discount_multiplier = min(1-self.discount, towers[tower].discount_multiplier)

    def remove_effects(self, towers: dict[int, Tower]):
        for tower in towers.values():
            towers[tower].discount_multiplier = 1

        # in case other artisans are nearby
        for tower in towers.values():
            if type(tower) == Artisan:
                tower.init_effects(towers)
    

class General(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.set_name("General")
        self.set_cost(2000)
        self.set_total_cost(2000)
        self.set_damage(1)
        self.set_attack_delay(60)
        self.set_range(15)
        self.set_metal_flag(True)
        self.set_color(COLOR.DARK_BLUE)
        self.set_attack_color(COLOR.DARK_GRAY)
        self.set_id(13)
        self.set_upgrade_cost(1000)
        self.set_upgrade_name("Strategic Command")
        self.set_attack_sound(pygame.mixer.Sound('sounds/pistol1.ogg'))
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
        self.set_upgrade_cost(2000)
        self.set_upgrade_name("Heavy Arsenal")
        self.set_attack_delay(50)
        self.spawn_armored_infantry = True
        self.total_infantry_spawn_delay = 300
        self.infantry_level = 2

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_cost(5000)
        self.set_upgrade_name("Aerial Dominance")
        self.set_attack_delay(40)
        self.set_damage(2)
        self.spawn_artillery = True

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_cost(10000)
        self.set_upgrade_name("Total Warfare")
        self.set_attack_delay(30)
        self.spawn_combat_aviation = True
        self.total_infantry_spawn_delay = 200
        self.total_armored_infantry_spawn_delay = 400
        self.infantry_level = 3
        self.armored_infantry_level = 2

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_cost(0)
        self.set_attack_delay(20)
        self.set_damage(5)
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
        self.set_name("Troop")
        self.set_total_walk_delay(5)
        self.set_current_walk_delay(5)
        self.set_max_health(10)
        self.set_health(10)
        self.set_damage(1)
        self.set_attack_delay(30)
        self.set_range(10)
        self.set_invisible_flag(True)
        self.set_color(COLOR.DARK_BLUE)
        self.set_attack_color(COLOR.DARK_GRAY)
        self.set_id(14)
        self.set_attack_sound(pygame.mixer.Sound('sounds/pistol1.ogg'))

    def set_total_walk_delay(self, delay) -> None:
        self.total_walk_delay = delay

    def set_current_walk_delay(self, delay) -> None:
        self.current_walk_delay = delay

    def set_max_health(self, health) -> None:
        self.max_health = health

    def set_health(self, health) -> None:
        self.health = health

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
        self.set_name("Infantry")
        self.set_max_health(10 + 10 * (level - 1))
        self.set_health(self.max_health)
        self.set_damage(1 * level)
        self.set_attack_delay(30 - 3 * (level - 1))
        self.set_range(10 + 2 * (level - 1))
        self.set_color(COLOR.LIGHT)

class ArmoredInfantry(Troop):
    def __init__(self, level) -> None:
        super().__init__()
        self.set_name("Armored Infantry")
        self.set_max_health(35 + 35 * (level - 1))
        self.set_health(self.max_health)
        self.set_damage(2 * level)
        self.set_total_walk_delay(8)
        self.set_current_walk_delay(self.total_walk_delay)
        self.set_attack_delay(30 - 3 * (level - 1))
        self.set_range(10 + 2 * (level - 1))
        self.set_color(COLOR.DARK_GRAY)

class Artillery(Troop):
    def __init__(self, level) -> None:
        super().__init__()
        self.set_name("Artillery")
        self.set_damage(50 + 25 * (level - 1))
        self.set_attack_delay(100 - 10 * (level - 1))
        self.set_max_health(100 + 60 * (level - 1))
        self.set_total_walk_delay(12)
        self.set_current_walk_delay(self.total_walk_delay)
        self.set_health(self.max_health)
        self.set_range(30)
        self.set_metal_flag(True)
        self.set_air_flag(True)
        self.set_color(COLOR.DARK_GREEN)
        self.set_attack_sound(pygame.mixer.Sound('sounds/cannon.wav'))

class CombatAviation(Troop):
    def __init__(self, level) -> None:
        super().__init__()
        self.set_name("Combat Aviation")
        self.set_damage(25 + 15 * (level - 1))
        self.set_attack_delay(10 - 1 * (level - 1))
        self.set_range(25)
        self.set_total_walk_delay(3)
        self.set_current_walk_delay(self.total_walk_delay)
        self.set_metal_flag(True)
        self.set_air_flag(True)
        self.set_color(COLOR.GRAY)
        self.set_attack_sound(pygame.mixer.Sound('sounds/firework.ogg'))
        self.add_attack(name="Missile", damage=200+100*(level - 1), delay=50-3*(level - 1), radius=5, color=COLOR.RED, sound=pygame.mixer.Sound('sounds/missile-blast.ogg'),
                        type=Attacking.RANGED, attack=self.multi_attack, targeting=self.find_multi_target, size=4)

class Alchemist(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.set_name("Alchemist")
        self.set_cost(1100)
        self.set_total_cost(self.cost)
        self.set_damage(6)
        self.set_attack_delay(60)
        self.set_attack_radius(3)
        self.set_range(15)
        self.set_metal_flag(True)
        self.set_color(COLOR.DARK_PURPLE)
        self.set_attack_color(COLOR.PURPLE)
        self.set_id(15)
        self.set_upgrade_name("Toxic Chemicals")
        self.set_upgrade_cost(400)
        self.set_attack_sound(pygame.mixer.Sound('sounds/shatter.ogg'))

    def upgrade1(self):
        super().upgrade1()
        self.set_upgrade_name("Explosive Chemicals")
        self.set_upgrade_cost(1200)
        self.add_attack(name="Toxic Chemicals", damage=6, delay=60, radius=3, color=COLOR.DARK_GREEN, sound=pygame.mixer.Sound('sounds/shatter.ogg'),
                        type=Attacking.RANGED, attack=self.multi_attack, targeting=self.find_multi_target, size=3)
        self.set_ranges(17)

    def upgrade2(self):
        super().upgrade2()
        self.set_upgrade_name("Mad Scientist")
        self.set_upgrade_cost(2500)
        self.add_attack(name="Explosive Chemicals", damage=20, delay=60, radius=5, color=COLOR.DARK_ORANGE, sound=pygame.mixer.Sound('sounds/shatter.ogg'),
                        type=Attacking.RANGED, attack=self.multi_attack, targeting=self.find_multi_target, size=4)
        self.set_ranges(20)

    def upgrade3(self):
        super().upgrade3()
        self.set_upgrade_name("Regenerative Chemicals")
        self.set_upgrade_cost(5000)
        self.add_attack(name="Explosive Chemicals", damage=600, delay=60, radius=3, color=COLOR.DARK_GREEN, sound=pygame.mixer.Sound('sounds/shatter.ogg'),
                        type=Attacking.RANGED, attack=self.multi_attack, targeting=self.find_multi_target, size=4)
        self.set_ranges(25)

    def upgrade4(self):
        super().upgrade4()
        self.set_upgrade_name("Chemical Warfare")
        self.set_upgrade_cost(5000)
        self.add_attack(name="Explosive Chemicals", damage=600, delay=60, radius=3, color=COLOR.DARK_GREEN, sound=pygame.mixer.Sound('sounds/shatter.ogg'),
                        type=Attacking.RANGED, attack=self.multi_attack, targeting=self.find_multi_target, size=4)
        self.set_ranges(30)

# class PlagueDoctor(Tower):
#     def __init__(self) -> None:
#         super().__init__()
#         self.name = "Plague Doctor"
#         self.cost = 1300
#         self.total_cost = self.cost
#         self.damage = 1
#         self.attack_delay = 60
#         self.attack_radius = 3
#         self.max_targets = 3
#         self.stun_delay = 10
#         self.range = 15
#         self.metal_flag = True
#         self.color = COLOR.DARK_PURPLE
#         self.attack_color = COLOR.PURPLE
#         self.id = 14
#         self.upgrade_cost = 250
#         self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

# class Toxicologist(Tower):
#     def __init__(self) -> None:
#         super().__init__()
#         self.name = "Toxicologist"
#         self.cost = 1500
#         self.total_cost = self.cost
#         self.damage = 1
#         self.attack_delay = 60
#         self.attack_radius = 3
#         self.max_targets = 3
#         self.stun_delay = 10
#         self.range = 15
#         self.metal_flag = True
#         self.color = COLOR.DARK_PURPLE
#         self.attack_color = COLOR.PURPLE
#         self.id = 15
#         self.upgrade_cost = 250
#         self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

# class Pyromancer(Tower):
#     def __init__(self) -> None:
#         super().__init__()
#         self.name = "Pyromancer"
#         self.cost = 1200
#         self.total_cost = self.cost
#         self.damage = 1
#         self.attack_delay = 60
#         self.attack_radius = 3
#         self.max_targets = 3
#         self.stun_delay = 10
#         self.range = 15
#         self.metal_flag = True
#         self.color = COLOR.ORANGE
#         self.attack_color = COLOR.LIGHT_ORANGE
#         self.id = 16
#         self.upgrade_cost = 250
#         self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

# class Hypnotist(Tower):
#     def __init__(self) -> None:
#         super().__init__()
#         self.name = "Hypnotist"
#         self.cost = 700
#         self.total_cost = self.cost
#         self.damage = 1
#         self.attack_delay = 60
#         self.attack_radius = 3
#         self.max_targets = 3
#         self.stun_delay = 10
#         self.range = 15
#         self.metal_flag = True
#         self.color = COLOR.PINK
#         self.attack_color = COLOR.LIGHT_PURPLE
#         self.id = 15
#         self.upgrade_cost = 250
#         self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

# class Butcher(Tower):
#     def __init__(self) -> None:
#         super().__init__()
#         self.name = "Butcher"
#         self.cost = 900
#         self.total_cost = self.cost
#         self.damage = 1
#         self.attack_delay = 60
#         self.attack_radius = 3
#         self.max_targets = 3
#         self.stun_delay = 10
#         self.range = 15
#         self.metal_flag = True
#         self.color = COLOR.DARK_RED
#         self.attack_color = COLOR.RED
#         self.id = 17
#         self.upgrade_cost = 250
#         self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

# class Blacksmith(Tower):
#     def __init__(self) -> None:
#         super().__init__()
#         self.name = "Blacksmith"
#         self.cost = 1100
#         self.total_cost = self.cost
#         self.damage = 1
#         self.attack_delay = 60
#         self.attack_radius = 3
#         self.max_targets = 3
#         self.stun_delay = 10
#         self.range = 15
#         self.metal_flag = True
#         self.color = COLOR.DARK_RED
#         self.attack_color = COLOR.RED
#         self.id = 18
#         self.upgrade_cost = 250
#         self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

# class Miner(Tower):
#     def __init__(self) -> None:
#         super().__init__()
#         self.name = "Miner"
#         self.cost = 450
#         self.total_cost = self.cost
#         self.damage = 1
#         self.attack_delay = 60
#         self.attack_radius = 3
#         self.max_targets = 3
#         self.stun_delay = 10
#         self.range = 15
#         self.metal_flag = True
#         self.color = COLOR.BROWN
#         self.attack_color = COLOR.DARK_ORANGE
#         self.id = 16
#         self.upgrade_cost = 250
#         self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

# class Detonator(Tower):
#     def __init__(self) -> None:
#         super().__init__()
#         self.name = "Detonator"
#         self.cost = 800
#         self.total_cost = self.cost
#         self.damage = 1
#         self.attack_delay = 60
#         self.attack_radius = 3
#         self.max_targets = 3
#         self.stun_delay = 10
#         self.range = 15
#         self.metal_flag = True
#         self.color = COLOR.DARK_ORANGE
#         self.attack_color = COLOR.ORANGE
#         self.id = 17
#         self.upgrade_cost = 250
#         self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

# class Harvester(Tower):
#     def __init__(self) -> None:
#         super().__init__()
#         self.name = "Harvester"
#         self.cost = 1200
#         self.total_cost = self.cost
#         self.damage = 1
#         self.attack_delay = 60
#         self.attack_radius = 3
#         self.max_targets = 3
#         self.stun_delay = 10
#         self.range = 15
#         self.metal_flag = True
#         self.color = COLOR.DARK_GREEN
#         self.attack_color = COLOR.GREEN
#         self.id = 18
#         self.upgrade_cost = 250
#         self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

# class IceSoldier(Tower):
#     def __init__(self) -> None:
#         super().__init__()
#         self.name = "Ice Soldier"
#         self.cost = 1300
#         self.total_cost = self.cost
#         self.damage = 1
#         self.attack_delay = 60
#         self.attack_radius = 3
#         self.max_targets = 3
#         self.stun_delay = 10
#         self.range = 15
#         self.metal_flag = True
#         self.color = COLOR.DARK_BLUE
#         self.attack_color = COLOR.BLUE
#         self.id = 19
#         self.upgrade_cost = 250
#         self.attack_sound = pygame.mixer.Sound('sounds/electric_buzz.ogg')

if __name__ == "__main__":
    # print(Warrior().color)
    print(Tower(), Warrior())