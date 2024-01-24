class Tower:
    """Base Tower Class
    """

    def __init__(self) -> None:
        self.cost           # game currency
        self.damage         # health ticks
        self.attack_delay   # milliseconds
        self.range          # grid squares
        self.invisible_flag # camo
        self.metal_flag     # lead
        self.boss_flag      # blimp
        self.sprite         # sprite source file
        self.current_delay  # attack delay counter

    def place(self, x, y) -> None:
        self.x = x
        self.y = y
        self.draw()

    def draw(self) -> None:
        self.pygame.draw.rect()

    