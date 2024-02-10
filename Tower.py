import pygame.draw
import copy
from numpy import sqrt
from random import choice
from Enemy import Enemy
from utils import COLOR,Targeting,draw_circle_alpha
from constants import CELL_SIZE

class Tower:
    """Base Tower Class
    """

    def __init__(self) -> None:
        self.name = 'Warrior'           # name
        self.cost = 250                 # game currency
        self.damage = 1                 # health ticks
        self.attack_delay = 20           # milliseconds
        self.range = 20                 # grid squares
        self.invisible_flag = False     # camo
        self.metal_flag = False         # lead
        self.air_flag = False           # flying
        self.boss_flag = False          # blimp
        self.color = COLOR.GREEN        # look
        self.current_delay = self.attack_delay # attack delay counter
        self.width = 3                  # number of cells wide
        self.height = 3                 # number of cells tall
        self.id = 1                     # ID number for grid
        self.targeting = Targeting.FIRST   
        self.attack_color = COLOR.BLACK
        self.attack_type = 0
        self.upgrade_level = 0
        self.upgrade_cost = 0
        self.rect = pygame.Rect(0, 0, self.width * CELL_SIZE, self.height * CELL_SIZE)
        self.total_damage = 0
        # self.attack_sound = pygame.mixer.Sound('sounds/temp.ogg')

    def place(self, x, y, num) -> None:
        self.x = x
        self.y = y
        self.num = num

        self.rect.center = (self.x * CELL_SIZE, self.y * CELL_SIZE)

    def attack(self, screen, enemy: Enemy) -> None:
        start_pos = ((self.x+0.5)*CELL_SIZE, self.y*CELL_SIZE)
        end_pos = ((enemy.x + 0.5 + enemy.width // 2)*CELL_SIZE, (enemy.y + enemy.height // 2)*CELL_SIZE)
        pygame.draw.line(screen, self.attack_color, start_pos, end_pos, 2)
        self.current_delay = self.attack_delay
        killed = enemy.damage(self.damage)
        if killed:
            return [killed]
        return None
    
    def can_attack(self, enemy: Enemy):
        if enemy.invisible_flag or enemy.air_flag or enemy.metal_flag:
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
        self.upgrade_level = 1

    def upgrade2(self):
        self.upgrade_level = 2

    def upgrade3(self):
        self.upgrade_level = 3

    def upgrade4(self):
        self.upgrade_level = 4

    def upgrade5(self):
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

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 0
        self.damage = 4
        self.attack_delay = 10
        self.range = 27


class Archer(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Archer'
        self.cost = 350
        self.damage = 2
        self.attack_delay = 45
        self.range = 25
        self.air_flag = True
        self.color = COLOR.RED
        self.id = 2
        self.upgrade_cost = 150

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
    

class Deadeye(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Deadeye'
        self.cost = 600
        self.damage = 5
        self.attack_delay = 120
        self.range = 45
        self.invisible_flag = True
        self.air_flag = True
        self.color = COLOR.GRAY
        self.id = 3
        self.upgrade_cost = 400

    def can_attack(self, enemy: Enemy):
        if enemy.metal_flag:
            return False
        return True

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

class Berserker(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Berserker'
        self.cost = 800
        self.damage = 1
        self.delay_changes = {6: 30, 7: 0, 8: 0, 9: 0, 10: 0} # {6: 30, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        self.range_changes = {10: 6, 6: 7, 7: 8, 8: 9, 9: 10} # {30: 3, 3: 6, 6: 9, 9: 12, 12: 15, 15: 18, 18: 21, 21: 24, 24: 27, 27: 30}
        self.attack_delay = 45
        self.range = 10
        self.temp_range = 6
        self.color = COLOR.BLUE
        self.id = 4
        self.upgrade_cost = 200
        self.attack_color = COLOR.FAINT_BLUE

    def attack_round(self, screen):
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
        self.delay_changes = {6: 30, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0} # {6: 30, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        self.range_changes = {12: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12} # {30: 3, 3: 6, 6: 9, 9: 12, 12: 15, 15: 18, 18: 21, 21: 24, 24: 27, 27: 30}

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 3500
        self.attack_delay = 40
        self.range = 12

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 7000
        self.damage = 2
        self.delay_changes = {6: 30, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0} # {6: 30, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        self.range_changes = {15: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15} # {30: 3, 3: 6, 6: 9, 9: 12, 12: 15, 15: 18, 18: 21, 21: 24, 24: 27, 27: 30}

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 0
        self.damage = 5
        self.delay_changes = {6: 30, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0} # {6: 30, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
        self.range_changes = {20: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 13: 14, 14: 15, 15: 16, 16: 17, 17: 18, 18: 19, 19: 20} # {30: 3, 3: 6, 6: 9, 9: 12, 12: 15, 15: 18, 18: 21, 21: 24, 24: 27, 27: 30}

class Assassin(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Assassin'
        self.cost = 400
        self.damage = 1
        self.attack_delay = 10
        self.invisible_flag = True
        self.range = 15
        self.color = COLOR.BLACK
        self.id = 5
        self.upgrade_cost = 100

    def can_attack(self, enemy: Enemy):
        if enemy.air_flag or enemy.metal_flag:
            return False
        return True

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 500
        self.range = 17
        self.attack_delay = 9

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

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 0
        self.damage = 8
        self.attack_delay = 3

class Gunslinger(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Gunslinger'
        self.cost = 1000
        self.damage = 5
        self.attack_delay = 50
        self.range = 20
        self.boss_flag = True
        self.color = COLOR.ORANGE
        self.id = 6
        self.upgrade_cost = 200

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 200

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 500

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 0

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 0

    def upgrade5(self):
        super().upgrade4()
        self.upgrade_cost = 0

class Dragoon(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Dragoon'
        self.cost = 1500
        self.damage = 10
        self.attack_delay = 60
        self.attack_radius = 5
        self.range = 32
        self.metal_flag = True
        self.color = COLOR.PURPLE
        self.attack_color = COLOR.DARK_PURPLE
        self.id = 7
        self.upgrade_cost = 200

    def can_attack(self, enemy: Enemy):
        if enemy.invisible_flag or enemy.air_flag:
            return False
        return True

    def attack(self, screen, enemies: list) -> None:
        enemy = enemies[0]
        start_pos = ((self.x+0.5)*CELL_SIZE, self.y*CELL_SIZE)
        end_pos = ((enemy.x + 0.5 + enemy.width // 2)*CELL_SIZE, (enemy.y + enemy.height // 2)*CELL_SIZE)
        pygame.draw.line(screen, self.attack_color, start_pos, end_pos, 2)
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
        self.upgrade_cost = 200

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 500

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 0

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 0

    def upgrade5(self):
        super().upgrade4()
        self.upgrade_cost = 0

class Farm(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Farm'
        self.cost = 200
        self.damage = 0
        self.attack_delay = -1
        self.range = 3
        self.color = COLOR.WHITE
        self.id = 8
        self.upgrade_cost = 200
        self.money = 100

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 200
        self.money = 200

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 750
        self.money = 500

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 2500
        self.money = 1000

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 7500
        self.money = 2000

    def upgrade5(self):
        super().upgrade5()
        self.upgrade_cost = 15000
        self.money = 5000

class Electrocutioner(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Electrocutioner"
        self.cost = 750
        self.damage = 1
        self.attack_delay = 60
        self.attack_radius = 5
        self.range = 15
        self.metal_flag = True
        self.color = COLOR.DARK_TEAL
        self.attack_color = COLOR.TEAL
        self.id = 9
        self.upgrade_cost = 200

    def can_attack(self, enemy: Enemy):
        if enemy.invisible_flag or enemy.air_flag:
            return False
        return True

    def attack(self, screen, enemies: list) -> None:
        enemy = enemies[0]
        start_pos = ((self.x+0.5)*CELL_SIZE, self.y*CELL_SIZE)
        killed_list = []
        for enemy in enemies:
            enemy.current_delay += 10
            end_pos = ((enemy.x + 0.5 + enemy.width // 2)*CELL_SIZE, (enemy.y + enemy.height // 2)*CELL_SIZE)
            pygame.draw.line(screen, self.attack_color, start_pos, end_pos, 2)
            killed = enemy.damage(self.damage)
            if killed:
                killed_list.append(killed)
            start_pos = end_pos
        self.current_delay = self.attack_delay
        return killed_list

    def find_target(self, screen, enemies):
        temp_enemies = copy.deepcopy(enemies)
        print("Finding target")
        distances = {
            k: sqrt(((max(enemy.x, min(self.x, enemy.x + enemy.width))) - self.x) ** 2 +
                    ((max(enemy.y, min(self.y, enemy.y + enemy.height))) - self.y) ** 2)
            for k, enemy in temp_enemies.items()
        }
        target = None

        targets_in_range = [k for k, distance in distances.items() if distance <= self.range]
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
            print(f"Found target {target.num}")
            temp_enemies.pop(target_key)
        if target:
            targets = [target]
            done = False
            while not done and len(temp_enemies):
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
                        print(f"Found target {target.num}")
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
        self.upgrade_cost = 200

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 500

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 0

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 0

    def upgrade5(self):
        super().upgrade4()
        self.upgrade_cost = 0

if __name__ == "__main__":
    print(Warrior().color)