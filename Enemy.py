import pygame
from constants import CELL_SIZE
from utils import Direction, COLOR

class Enemy:
    """Base Enemy Class
    """

    def __init__(self) -> None:
        self.name = "Pirate"
        self.speed_delay = 5
        self.max_health = 5
        self.health = self.max_health
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
        self.set_rect()
        self.status_effects = []
        self.path_progress = 0

    def set_rect(self):
        self.rect = pygame.Rect(0, 0, self.width * CELL_SIZE, self.height * CELL_SIZE)

    def place(self, location, grid, num) -> None:
        self.x = location[0]
        self.y = location[1]
        self.num = num
        grid[self.y:self.y+self.height+1, self.x:self.x+self.width+1] = self.id

        self.rect.topleft = (self.x * CELL_SIZE, self.y * CELL_SIZE)

    def walk(self, grid, selected_map) -> bool:
        if self.current_delay <= 0:
            if self.x == selected_map.end[0] and self.y == selected_map.end[1] or self.path_progress == len(selected_map.path):
                return False
            grid[self.y:self.y+self.height+1, self.x:self.x+self.width+1] = 0
            self.direction = selected_map.path[self.path_progress]
            self.x += selected_map.path[self.path_progress][0]
            self.y += selected_map.path[self.path_progress][1]
            grid[self.y:self.y+self.height+1, self.x:self.x+self.width+1] = self.id
            # rotate self.rect if direction is up or down
            if self.direction == (0, -1) or self.direction == (0, 1):
                self.rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, self.width * CELL_SIZE, self.height * CELL_SIZE)
            self.current_delay = self.speed_delay
            self.path_progress += 1
            return True
        self.current_delay -= 1
        self.rect.topleft = (self.x * CELL_SIZE, self.y * CELL_SIZE)
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

class Pirate(Enemy):
    def __init__(self) -> None:
        super().__init__()

class Bandit(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Bandit"
        self.speed_delay = 3
        self.max_health = 3
        self.health = self.max_health
        self.color = COLOR.DARK_BLUE
        self.id = 102

class Thug(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Thug"
        self.speed_delay = 8
        self.max_health = 12
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 103

class Brute(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Brute"
        self.speed_delay = 8
        self.max_health = 40
        self.health = self.max_health
        self.color = COLOR.LIGHT
        self.id = 104

class Ghost(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ghost"
        self.speed_delay = 4
        self.max_health = 15
        self.health = self.max_health
        self.invisible_flag = True
        self.color = COLOR.PURPLE
        self.id = 105
        
class Phantom(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Phantom"
        self.speed_delay = 3
        self.max_health = 50
        self.health = self.max_health
        self.invisible_flag = True
        self.air_flag = True
        self.color = COLOR.WHITE
        self.id = 106

class Armored(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Armored"
        self.speed_delay = 8
        self.max_health = 60
        self.health = self.max_health
        self.metal_flag = True
        self.color = COLOR.GRAY
        self.id = 107

class Paratrooper(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Paratrooper"
        self.speed_delay = 4
        self.max_health = 30
        self.health = self.max_health
        self.air_flag = True
        self.color = COLOR.LIGHT_BLUE
        self.id = 108

class Drone(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Drone"
        self.speed_delay = 7
        self.max_health = 250
        self.health = self.max_health
        self.metal_flag = True
        self.air_flag = True
        self.color = COLOR.DARK_GRAY
        self.id = 109

class Ectoplasmite(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ectoplasmite"
        self.speed_delay = 8
        self.max_health = 400
        self.health = self.max_health
        self.metal_flag = True
        self.invisible_flag = True
        self.color = COLOR.LIGHT_PURPLE
        self.id = 110

class UFO(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "UFO"
        self.speed_delay = 5
        self.max_health = 1000
        self.health = self.max_health
        self.metal_flag = True
        self.invisible_flag = True
        self.air_flag = True
        self.color = COLOR.LIGHT_GRAY
        self.id = 111

class Juggernaut(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Juggernaut"
        self.speed_delay = 5
        self.max_health = 1000
        self.health = self.max_health
        self.color = COLOR.DARK_GREEN
        self.id = 112

class Marauder(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Marauder"
        self.speed_delay = 3
        self.max_health = 250
        self.health = self.max_health
        self.color = COLOR.LIGHT_GRAY
        self.id = 113

class Smuggler(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Smuggler"
        self.speed_delay = 2
        self.max_health = 100
        self.health = self.max_health
        self.color = COLOR.LIGHT_GRAY
        self.id = 114

class Raider(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Raider"
        self.speed_delay = 3
        self.max_health = 1000
        self.health = self.max_health
        self.color = COLOR.LIGHT_GRAY
        self.id = 115

class Saboteur(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Saboteur"
        self.speed_delay = 5
        self.max_health = 250
        self.health = self.max_health
        self.color = COLOR.LIGHT_GRAY
        self.id = 116

class Hooligan(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Hooligan"
        self.speed_delay = 8
        self.max_health = 500
        self.health = self.max_health
        self.color = COLOR.LIGHT_GRAY
        self.id = 117

class PirateGunner(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Pirate Gunner"
        self.max_health = 100
        self.health = self.max_health
        self.boss_flag = True
        self.color = COLOR.DARK_GREEN
        self.id = 118
        self.height = 3
        self.width = 4
        self.set_rect()

class PirateMate(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Pirate Mate"
        self.max_health = 500
        self.health = self.max_health
        self.boss_flag = True
        self.color = COLOR.DARK_GREEN
        self.id = 119
        self.height = 4
        self.width = 5
        self.set_rect()

class PirateCaptain(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Pirate Captain"
        self.max_health = 2500
        self.health = self.max_health
        self.boss_flag = True
        self.color = COLOR.DARK_GREEN
        self.id = 120
        self.height = 4
        self.width = 6
        self.set_rect()

class DreadPirate(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Dread Pirate"
        self.max_health = 50000
        self.speed_delay = 10
        self.health = self.max_health
        self.boss_flag = True
        self.color = COLOR.DARK_GREEN
        self.id = 121
        self.height = 5
        self.width = 7
        self.set_rect()

class GhostPirate(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ghost Pirate"
        self.max_health = 200
        self.health = self.max_health
        self.invisible_flag = True
        self.boss_flag = True
        self.color = COLOR.PURPLE
        self.id = 122
        self.height = 3
        self.width = 4
        self.set_rect()

class BruteEnforcer(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Brute Enforcer"
        self.max_health = 20000
        self.speed_delay = 10
        self.health = self.max_health
        self.boss_flag = True
        self.color = COLOR.LIGHT
        self.id = 123
        self.height = 3
        self.width = 4
        self.set_rect()

class Infiltrator(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Infiltrator"
        self.speed_delay = 1
        self.max_health = 1000
        self.boss_flag = False
        self.health = self.max_health
        self.color = COLOR.LIGHT_GRAY
        self.id = 124

class TrojanHorse(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Trojan Horse"
        self.speed_delay = 5
        self.max_health = 500
        self.health = self.max_health
        self.color = COLOR.DARK_BROWN
        self.id = 125

# TODO: something related to prison break

# TODO: magic book guy

# TODO: witch and witchs' coven

################################################################################
#                                 Drowned                                      #
################################################################################
class Drowned(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Drowned"
        self.speed_delay = 5
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_BLUE
        self.id = 201

class DrownedGunner(Enemy):
    pass

class DrownedMate(Enemy):
    pass

class DrownedCaptain(Enemy):
    pass

class Mermaid(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Mermaid"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_BLUE
        self.id = 203

class Siren(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Siren"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_BLUE
        self.id = 204

class AbyssalKing(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Abyssal King"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 103

class MonsterOfTheDeep(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Monster of the Deep"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 103
        
################################################################################
#                                  Hell                                        #
################################################################################
class Undead(Enemy):
    pass

class Demon(Enemy):
    pass

class HellHound(Enemy):
    def __init__(self) -> None:
        super().__init__()      
        self.name = "Thug"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 103

class FallenAngel(Enemy):
    pass

class Immortal(Enemy):
    pass

class Nightmare(Enemy):
    pass

class Cerberus(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Thug"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 103  

class Conquest(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Thug"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.WHITE
        self.id = 103

class War(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Thug"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.RED
        self.id = 103

class Famine(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Thug"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.BLACK
        self.id = 103

class Death(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Thug"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.FAINT
        self.id = 103

class DemonPriest(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Demon Priest"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 103

class DemonPrince(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Demon Prince"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 103

class Hades(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Thug"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 103
        
################################################################################
#                                Corrupted                                     #
################################################################################
class Corrupted(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Thug"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 103

class Diseased(Enemy):
    pass

class Defect(Enemy):
    pass

class Aberration(Enemy):
    pass

class Abomination(Enemy):
    pass

class Pestilence(Enemy):
    pass