import pygame.draw
from Enemy import Enemy
from utils import COLOR

class Tower:
    """Base Tower Class
    """

    def __init__(self) -> None:
        self.name = 'Warrior'           # name
        self.cost = 250                 # game currency
        self.damage = 1                 # health ticks
        self.attack_delay = 30           # milliseconds
        self.range = 10                 # grid squares
        self.invisible_flag = False     # camo
        self.metal_flag = False         # lead
        self.boss_flag = False          # blimp
        self.color = COLOR.GREEN        # look
        self.current_delay = self.attack_delay # attack delay counter
        self.width = 3                  # number of cells wide
        self.height = 3                 # number of cells tall
        self.id = 1                     # ID number for grid

    def place(self, x, y, num) -> None:
        self.x = x
        self.y = y
        self.num = num

    def attack(self, enemy: Enemy) -> None:
        if self.current_delay <= 0:
            self.current_delay = self.attack_delay
            return enemy.damage(self.damage)
        else:
            self.current_delay -= 1
            return None
        

class Warrior(Tower):
    def __init__(self) -> None:
        super().__init__()

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

class Deadeye(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Deadeye'
        self.cost = 600
        self.damage = 5
        self.attack_delay = 75
        self.range = 35
        self.color = COLOR.PURPLE
        self.id = 3

class Berserker(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Berserker'
        self.cost = 800
        self.damage = 10
        self.attack_delay = 30
        self.range = 5
        self.color = COLOR.BLUE
        self.id = 4

class Assassin(Tower):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'Assassin'
        self.cost = 400
        self.damage = 2
        self.attack_delay = 10
        self.range = 8
        self.invisible_flag = True
        self.color = COLOR.BLACK
        self.id = 5

if __name__ == "__main__":
    print(Warrior().color)