from utils import Direction


class Enemy:

    def __init__(self, pygame) -> None:
        self.speed          # pixels per second
        self.health         # health ticks
        self.invisible_flag # camo
        self.tough_flag     # lead
        self.boss_flag      # blimp
        self.sprite         # source file 
        self.pygame 
        self.direction

    def place(self, x, y) -> None:
        self.x = x
        self.y = y
        self.draw()

    def draw(self) -> None:
        self.pygame.draw.rect()

    def walk(self) -> None:
         pass

    def __get_next_square(self) -> None:
        pass