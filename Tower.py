import pygame.draw
from utils import COLOR
class Tower:
    """Base Tower Class
    """

    def __init__(self, name='Soldier', cost=250, damage=1, attack_delay=1, range=10, invisible_flag=False, metal_flag=False,
                 boss_flag=False, color=COLOR.GREEN, width=3, height=3, id=1) -> None:
        self.name           = name              # name
        self.cost           = cost              # game currency
        self.damage         = damage            # health ticks
        self.attack_delay   = attack_delay      # milliseconds
        self.range          = range             # grid squares
        self.invisible_flag = invisible_flag    # camo
        self.metal_flag     = metal_flag        # lead
        self.boss_flag      = boss_flag         # blimp
        self.color          = color             # look
        self.current_delay  = self.attack_delay # attack delay counter
        self.width          = width             # number of cells wide
        self.height         = height            # number of cells tall
        self.id             = id                # ID number for grid

    def place(self, x, y) -> None:
        self.x = x
        self.y = y
        self.draw()

    def draw(self) -> None:
        self.pygame.draw.rect()

Soldier = Tower()
Archer = Tower('Archer', 350, 2, 2, 25, color=COLOR.RED, id=2)
Deadeye = Tower('Deadeye', 600, 5, 3, 35, color=COLOR.PURPLE, id=3)
Berserker = Tower('Berserker', 800, 10, 1, 5, color=COLOR.BLUE, id=4)
Assassin = Tower('Assassin', 400, 2, 1, 8, True, color=COLOR.BLACK, id=5)