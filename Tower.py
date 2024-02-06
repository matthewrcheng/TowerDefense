import pygame.draw
from Enemy import Enemy
from utils import COLOR,Targeting
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
        return enemy.damage(self.damage)
        
    def set_targeting(self, targeting: Targeting):
        self.targeting = targeting

    def reset_delay(self):
        self.current_delay = self.attack_delay

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
        self.color = COLOR.RED
        self.id = 2
        self.upgrade_cost = 150

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 350

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 1000

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 0
    

class Deadeye(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Deadeye'
        self.cost = 600
        self.damage = 5
        self.attack_delay = 120
        self.range = 45
        self.invisible_flag = True
        self.color = COLOR.GRAY
        self.id = 3
        self.upgrade_cost = 400

    def upgrade1(self):
        super().upgrade1()
        self.upgrade_cost = 1000

    def upgrade2(self):
        super().upgrade2()
        self.upgrade_cost = 2000

    def upgrade3(self):
        super().upgrade3()
        self.upgrade_cost = 4000

    def upgrade4(self):
        super().upgrade4()
        self.upgrade_cost = 0

class Berserker(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Berserker'
        self.cost = 800
        self.damage = 10
        self.attack_delay = 30
        self.range = 10
        self.color = COLOR.BLUE
        self.id = 4
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

class Assassin(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Assassin'
        self.cost = 400
        self.damage = 1
        self.attack_delay = 10
        self.invisible_flag = True
        self.range = 15
        self.invisible_flag = True
        self.color = COLOR.BLACK
        self.id = 5
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
        self.range = 32
        self.metal_flag = True
        self.color = COLOR.PURPLE
        self.id = 7
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

if __name__ == "__main__":
    print(Warrior().color)