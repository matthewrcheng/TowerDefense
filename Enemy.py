from utils import Direction, COLOR

class Enemy:
    """Base Enemy Class
    """

    def __init__(self, name="Basic", speed_delay=5, health=5, invisible_flag=False, metal_flag=False, boss_flag=False,
                 color=COLOR.DARK_GREEN, direction=Direction.right, height=2, width=3, id=101) -> None:
        self.name           = name
        self.speed_delay    = speed_delay       # pixels per second
        self.health         = health            # health ticks
        self.invisible_flag = invisible_flag    # camo
        self.metal_flag     = metal_flag        # lead
        self.boss_flag      = boss_flag         # blimp
        self.current_delay  = self.speed_delay  # current speed delay
        self.color          = color
        self.direction      = direction
        self.height         = height
        self.width          = width
        self.id             = id

    def place(self, location, grid) -> None:
        self.location       = location
        grid[self.location[1]:self.location[1]+self.height+1, self.location[0]:self.location[0]+self.width+1] = self.id

    def walk(self, grid) -> None:
        if self.current_delay == 0:
            if self.location + self.width >= len(grid[0]):
                return False
            grid[self.location[1]:self.location[1]+self.height+1, self.location[0]:self.location[0]+self.width+1] = 0
            self.location = (self.location[0]+1,self.location[1])
            grid[self.location[1]:self.location[1]+self.height+1, self.location[0]:self.location[0]+self.width+1] = self.id
            self.current_delay = self.speed_delay
            return True
        self.current_delay -= 1

    def __get_next_square(self) -> None:
        pass

class Basic(Enemy):
    placeholder = False

class Speedy(Enemy):
    def __init__(self, name="Speedy", speed_delay=3, health=3, invisible_flag=False, metal_flag=False, boss_flag=False,
                 color=COLOR.DARK_BLUE, direction=Direction.right, height=2, width=3, id=102) -> None:
        self.name           = name
        self.speed_delay    = speed_delay       # pixels per second
        self.health         = health            # health ticks
        self.invisible_flag = invisible_flag    # camo
        self.metal_flag     = metal_flag        # lead
        self.boss_flag      = boss_flag         # blimp
        self.current_delay  = self.speed_delay  # current speed delay
        self.color          = color
        self.direction      = direction
        self.height         = height
        self.width          = width
        self.id             = id

class Tough(Enemy):
    def __init__(self, name="Tough", speed_delay=8, health=8, invisible_flag=False, metal_flag=False, boss_flag=False,
                 color=COLOR.DARK_RED, direction=Direction.right, height=2, width=3, id=103) -> None:
        self.name           = name
        self.speed_delay    = speed_delay       # pixels per second
        self.health         = health            # health ticks
        self.invisible_flag = invisible_flag    # camo
        self.metal_flag     = metal_flag        # lead
        self.boss_flag      = boss_flag         # blimp
        self.current_delay  = self.speed_delay  # current speed delay
        self.color          = color
        self.direction      = direction
        self.height         = height
        self.width          = width
        self.id             = id