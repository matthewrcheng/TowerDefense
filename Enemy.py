from utils import Direction, COLOR

class Enemy:
    """Base Enemy Class
    """

    def __init__(self) -> None:
        self.name = "Basic"
        self.speed_delay = 5
        self.health = 5
        self.invisible_flag = False
        self.metal_flag = False
        self.air_flag = False
        self.boss_flag = False
        self.current_delay = self.speed_delay
        self.color = COLOR.DARK_GREEN
        self.direction = Direction.right
        self.height = 2
        self.width = 3
        self.id = 101

    def place(self, location, grid, num) -> None:
        self.x = location[0]
        self.y = location[1]
        self.num = num
        grid[self.y:self.y+self.height+1, self.x:self.x+self.width+1] = self.id

    def walk(self, grid) -> bool:
        if self.current_delay <= 0:
            if self.x + self.width >= len(grid[0]):
                return False
            grid[self.y:self.y+self.height+1, self.x:self.x+self.width+1] = 0
            self.x += self.direction[0]
            self.y += self.direction[1]
            grid[self.y:self.y+self.height+1, self.x:self.x+self.width+1] = self.id
            self.current_delay = self.speed_delay
            return True
        self.current_delay -= 1
        return True
    
    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return self
        else:
            return None
    
    def face_right(self) -> None:
        self.direction = Direction.right
    
    def face_left(self) -> None:
        self.direction = Direction.left
    
    def face_up(self) -> None:
        self.direction = Direction.up

    def face_down(self) -> None:
        self.direction = Direction.down     
    
    def kill(self, grid):
        grid[self.y:self.y+self.height+1, self.x:self.x+self.width+1] = 0

    def __get_next_square(self) -> None:
        pass

    def __str__(self):
        return self.name

class Basic(Enemy):
    def __init__(self) -> None:
        super().__init__()

class Speedy(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Speedy"
        self.speed_delay = 3
        self.health = 3
        self.color = COLOR.DARK_BLUE
        self.id = 102

class Slow(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Slow"
        self.speed_delay = 8
        self.health = 8
        self.color = COLOR.DARK_RED
        self.id = 103

class Tough(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Tough"
        self.speed_delay = 8
        self.health = 40
        self.color = COLOR.LIGHT
        self.id = 104

class Ghost(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ghost"
        self.speed_delay = 4
        self.health = 15
        self.invisible_flag = True
        self.color = COLOR.PURPLE
        self.id = 105
        
class Phantom(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Phantom"
        self.speed_delay = 3
        self.health = 50
        self.invisible_flag = True
        self.air_flag = True
        self.color = COLOR.WHITE
        self.id = 106

class Metallic(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Metallic"
        self.speed_delay = 8
        self.health = 60
        self.metal_flag = True
        self.color = COLOR.GRAY
        self.id = 107

class Airborne(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Airborne"
        self.speed_delay = 4
        self.health = 30
        self.air_flag = True
        self.color = COLOR.LIGHT_BLUE
        self.id = 108