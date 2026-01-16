import pygame
from constants import CELL_SIZE
from utils import Direction, COLOR

# region Base Enemy Class

class Enemy:
    """Base Enemy Class
    """

    def __init__(self) -> None:
        self.name = "Pirate"
        self.speed_delay = 5
        self.max_health = 5                     # unchangable health, base health
        self.game_max_health = self.max_health  # max health in game, can be lowered by permanent damage from Butcher tower
        self.health = self.max_health           # current health
        self.invisible_flag = False
        self.metal_flag = False
        self.air_flag = False
        self.boss_flag = False
        self.defense = 0.0                      # 0.0-1.0
        self.current_delay = self.speed_delay
        self.color = COLOR.DARK_GREEN
        self.direction = Direction.right
        self.height = 2
        self.width = 3
        self.id = 101
        self.set_rect()
        self.status_effects = []
        self.shield = 0
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
        if self.shield > 0:
            self.shield -= amount
            if self.shield <= 0:
                self.shield = 0
            return None
        self.health -= (1 - self.defense) * amount
        if self.health <= 0:
            return self
        else:
            return None
        
    def break_shield_effect(self):
        pass
    
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

# endregion
# region Regular Enemies

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
        self.defense = 0.1

class Brute(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Brute"
        self.speed_delay = 8
        self.max_health = 40
        self.health = self.max_health
        self.color = COLOR.LIGHT
        self.id = 104
        self.defense = 0.2

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
        self.defense = 0.4

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
        self.defense = 0.3

class Juggernaut(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Juggernaut"
        self.speed_delay = 5
        self.max_health = 1000
        self.health = self.max_health
        self.color = COLOR.DARK_GREEN
        self.id = 112
        self.defense = 0.5

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
        self.max_health = 1000
        self.health = self.max_health
        self.boss_flag = True
        self.color = COLOR.DARK_GREEN
        self.id = 118
        self.height = 3
        self.width = 4
        self.set_rect()
        self.defense = 0.2

class PirateMate(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Pirate Mate"
        self.max_health = 5000
        self.health = self.max_health
        self.boss_flag = True
        self.color = COLOR.DARK_GREEN
        self.id = 119
        self.height = 4
        self.width = 5
        self.set_rect()
        self.defense = 0.2

class PirateCaptain(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Pirate Captain"
        self.max_health = 10000
        self.health = self.max_health
        self.boss_flag = True
        self.color = COLOR.DARK_GREEN
        self.id = 120
        self.height = 4
        self.width = 6
        self.set_rect()
        self.defense = 0.2

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
        self.defense = 0.2

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
        self.defense = 0.3

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
        self.shield = 500
        self.defense = 0.5

    def break_shield_effect(self):
        self.speed_delay = 5
        self.defense = 0

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

# endregion
# region Drowned Enemies

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
    def __init__(self) -> None:
        super().__init__()
        self.name = "Drowned Gunner"
        self.max_health = 1500
        self.health = self.max_health
        self.boss_flag = True
        self.color = COLOR.DARK_BLUE
        self.id = 118
        self.height = 3
        self.width = 4
        self.set_rect()
        self.defense = 0.3

class DrownedMate(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Drowned Mate"
        self.max_health = 7500
        self.health = self.max_health
        self.boss_flag = True
        self.color = COLOR.DARK_BLUE
        self.id = 119
        self.height = 4
        self.width = 5
        self.set_rect()
        self.defense = 0.3

class DrownedCaptain(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Drowned Captain"
        self.max_health = 15000
        self.health = self.max_health
        self.boss_flag = True
        self.color = COLOR.DARK_BLUE
        self.id = 120
        self.height = 4
        self.width = 6
        self.set_rect()
        self.defense = 0.3

class Mermaid(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Mermaid"
        self.speed_delay = 3
        self.max_health = 100
        self.health = self.max_health
        self.color = COLOR.DARK_BLUE
        self.id = 203

class Siren(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Siren"
        self.speed_delay = 3
        self.max_health = 500
        self.health = self.max_health
        self.color = COLOR.DARK_BLUE
        self.id = 204

class HardHatDiver(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Hard Hat Diver"
        self.speed_delay = 12
        self.max_health = 2000
        self.health = self.max_health
        self.color = COLOR.DARK_GRAY
        self.id = 202
        self.defense = 0.5

class AbyssalKing(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Abyssal King"
        self.speed_delay = 10
        self.max_health = 100000
        self.boss_flag = True
        self.health = self.max_health
        self.color = COLOR.DARK_BLUE
        self.id = 205
        self.height = 5
        self.width = 7
        self.set_rect()
        self.defense = 0.3

class MonsterOfTheDeep(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Monster of the Deep"
        self.speed_delay = 15
        self.max_health = 250000
        self.boss_flag = True
        self.health = self.max_health
        self.color = COLOR.BLACK
        self.id = 206
        self.height = 6
        self.width = 8
        self.set_rect()
        self.defense = 0.4

# endregion
# region Hell Enemies

################################################################################
#                                  Hell                                        #
################################################################################
class Undead(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Undead"
        self.speed_delay = 5
        self.max_health = 10
        self.health = self.max_health
        self.color = COLOR.GRAY
        self.id = 301

class Demon(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Demon"
        self.speed_delay = 5
        self.max_health = 40
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 302

class HellHound(Enemy):
    def __init__(self) -> None:
        super().__init__()      
        self.name = "Hell Hound"
        self.speed_delay = 3
        self.max_health = 60
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 303

class FallenAngel(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Fallen Angel"
        self.speed_delay = 4
        self.max_health = 80
        self.health = self.max_health
        self.color = COLOR.LIGHT_GRAY
        self.id = 312
        self.air_flag = True

class Immortal(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Immortal"
        self.speed_delay = 8
        self.max_health = 400
        self.health = self.max_health
        self.color = COLOR.LIGHT_GRAY
        self.id = 313

class Nightmare(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Nightmare"
        self.speed_delay = 6
        self.max_health = 120
        self.health = self.max_health
        self.color = COLOR.DARK_GRAY
        self.id = 314
        self.invisible_flag = True

class DoomBringer(Enemy): # summons demons periodically
    def __init__(self) -> None:
        super().__init__()
        self.name = "Doom Bringer"
        self.speed_delay = 10
        self.max_health = 2000
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 318
        self.boss_flag = True
        self.height = 3
        self.width = 4
        self.defense = 0.2

class Cerberus(Enemy): # shoots fireballs, stunning towers for a few seconds
    def __init__(self) -> None:
        super().__init__()
        self.name = "Cerberus"
        self.speed_delay = 5
        self.max_health = 5000
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 304  

class DemonPriest(Enemy): # applies shields to other enemies periodically
    def __init__(self) -> None:
        super().__init__()
        self.name = "Demon Priest"
        self.speed_delay = 8
        self.max_health = 1000
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 309
        self.boss_flag = True
        self.height = 3
        self.width = 4

class DemonPrince(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Demon Prince"
        self.speed_delay = 12
        self.max_health = 8000
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 310
        self.boss_flag = True
        self.defense = 0.2
        self.height = 4
        self.width = 6

class Titan(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Titan"
        self.speed_delay = 15
        self.max_health = 15000
        self.health = self.max_health
        self.color = COLOR.DARK_GRAY
        self.id = 315
        self.height = 6
        self.width = 8
        self.defense = 0.3

class CursedSoul(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Cursed Soul"
        self.speed_delay = 2
        self.max_health = 2500
        self.health = self.max_health
        self.color = COLOR.PURPLE
        self.id = 316
        self.shield = 1000

    def break_shield_effect(self): # stuns nearby towers for a short duration when shield breaks
        self.invisible_flag = True
        self.speed_delay = 5

class Conquest(Enemy): # first horseman of the apocalypse, shoots piercing arrows that stun towers for a short duration
    def __init__(self) -> None:
        super().__init__()
        self.name = "Conquest"
        self.speed_delay = 8
        self.max_health = 40000
        self.health = self.max_health
        self.color = COLOR.WHITE
        self.id = 305

class War(Enemy): # second horseman of the apocalypse, wields a sword that stuns nearby towers for a moderate duration
    def __init__(self) -> None:
        super().__init__()
        self.name = "War"
        self.speed_delay = 8
        self.max_health = 40000
        self.health = self.max_health
        self.color = COLOR.RED
        self.id = 306

class Famine(Enemy): # third horseman of the apocalypse, holds a pair of scales, reduces tower attack speed temporarily
    def __init__(self) -> None:
        super().__init__()
        self.name = "Famine"
        self.speed_delay = 8
        self.max_health = 40000
        self.health = self.max_health
        self.color = COLOR.BLACK
        self.id = 307

class Death(Enemy): # fourth horseman of the apocalypse, wields a scythe that reduces tower damage temporarily
    def __init__(self) -> None:
        super().__init__()
        self.name = "Death"
        self.speed_delay = 8
        self.max_health = 40000
        self.health = self.max_health
        self.color = COLOR.LIGHT_GREEN
        self.id = 308

class Hades(Enemy): # emerges after the horsemen, summons minions, shoots fireballs that stun towers for a moderate duration
    def __init__(self) -> None:
        super().__init__()
        self.name = "Hades"
        self.speed_delay = 12
        self.max_health = 500000
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 311
        self.boss_flag = True
        
# endregion
# region Corrupted Enemies

################################################################################
#                                Corrupted                                     #
################################################################################
class Corrupted(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Corrupted"
        self.speed_delay = 8
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.DARK_RED
        self.id = 400

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

# endregion
# region Santa's Workshop Enemies

################################################################################
#                            Santa's Workshop                                  #
################################################################################

class Elf(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Elf"
        self.speed_delay = 5
        self.max_health = 8
        self.health = self.max_health
        self.color = COLOR.LIGHT_GREEN
        self.id = 500

class GingerbreadMan(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Gingerbread Man"
        self.speed_delay = 3
        self.max_health = 10
        self.health = self.max_health
        self.color = COLOR.BROWN
        self.id = 501

class Snowman(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Snowman"
        self.speed_delay = 8
        self.max_health = 30
        self.health = self.max_health
        self.color = COLOR.WHITE
        self.id = 502

class Deer(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Deer"
        self.speed_delay = 3
        self.max_health = 50
        self.health = self.max_health
        self.color = COLOR.LIGHT_BROWN
        self.id = 503

class MallSanta(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Mall Santa"
        self.speed_delay = 8
        self.max_health = 100
        self.health = self.max_health
        self.color = COLOR.RED
        self.id = 504
        self.defense = 0.3

class SnowAngel(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Snow Angel"
        self.speed_delay = 5
        self.max_health = 30
        self.health = self.max_health
        self.color = COLOR.LIGHT_BLUE
        self.id = 505
        self.air_flag = True

class ChristmasTree(Enemy): # 4 elves holding a tree like a battering ram, turns into 4 elves after health reaches 0
    def __init__(self) -> None:
        super().__init__()
        self.name = "Christmas Tree"
        self.speed_delay = 3
        self.max_health = 1000
        self.health = self.max_health
        self.color = COLOR.DARK_GREEN
        self.id = 506

class Reindeer(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Reindeer"
        self.speed_delay = 3
        self.max_health = 200
        self.health = self.max_health
        self.color = COLOR.LIGHT_BROWN
        self.id = 507
        self.air_flag = True

class PolarBear(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Polar Bear"
        self.speed_delay = 5
        self.max_health = 500
        self.health = self.max_health
        self.color = COLOR.WHITE
        self.id = 508
        self.defense = 0.2

class FrozenOmegaBull(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Frozen Omega Bull"
        self.speed_delay = 3
        self.max_health = 1000
        self.health = self.max_health
        self.color = COLOR.LIGHT_BLUE
        self.id = 509

class Yeti(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Yeti"
        self.speed_delay = 8
        self.max_health = 2000
        self.health = self.max_health
        self.color = COLOR.BROWN
        self.id = 510
        self.defense = 0.4

class SantasSleigh(Enemy): # 8 reindeer emerge when health reaches 0
    def __init__(self) -> None:
        super().__init__()
        self.name = "Santa's Sleigh"
        self.speed_delay = 8
        self.max_health = 1000
        self.health = self.max_health
        self.color = COLOR.RED
        self.id = 511
        self.air_flag = True

class Grinch(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Grinch"
        self.speed_delay = 8
        self.max_health = 3000
        self.health = self.max_health
        self.color = COLOR.GREEN
        self.id = 512
        self.boss_flag = True

class AbominableSnowman(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Abominable Snowman"
        self.speed_delay = 12
        self.max_health = 5000
        self.health = self.max_health
        self.color = COLOR.WHITE
        self.id = 513
        self.defense = 0.5

class GhostOfChristmasPast(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ghost of Christmas Past"
        self.speed_delay = 5
        self.max_health = 2000
        self.health = self.max_health
        self.invisible_flag = True
        self.color = COLOR.LIGHT_PURPLE
        self.id = 516
        self.boss_flag = True

class GhostOfChristmasPresent(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ghost of Christmas Present"
        self.speed_delay = 8
        self.max_health = 5000
        self.health = self.max_health
        self.invisible_flag = True
        self.color = COLOR.LIGHT_GREEN
        self.id = 517
        self.boss_flag = True

class GhostOfChristmasFuture(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ghost of Christmas Future"
        self.speed_delay = 12
        self.max_health = 10000
        self.health = self.max_health
        self.invisible_flag = True
        self.color = COLOR.DARK_GRAY
        self.id = 518
        self.boss_flag = True

class Rudolph(Enemy): # drops to the ground when health reaches 2500
    def __init__(self) -> None:
        super().__init__()
        self.name = "Rudolph"
        self.speed_delay = 5
        self.max_health = 2500
        self.health = self.max_health
        self.color = COLOR.LIGHT_BROWN
        self.id = 514
        self.air_flag = True
        self.boss_flag = True
        self.shield = 2500

    def break_shield_effect(self):
        self.air_flag = False
        self.speed_delay = 3

class SantaClaus(Enemy): # summons minions (elf, reindeer, snowman, etc.)
    def __init__(self) -> None:
        super().__init__()
        self.name = "Santa Claus"
        self.speed_delay = 12
        self.max_health = 100000
        self.health = self.max_health
        self.color = COLOR.RED
        self.id = 515
        self.boss_flag = True

# endregion
# region Haunted Mansion Enemies

################################################################################
#                            Haunted Mansion                                   #
################################################################################

class Zombie(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Zombie"
        self.speed_delay = 5
        self.max_health = 18
        self.health = self.max_health
        self.color = COLOR.DARK_GREEN
        self.id = 600

class Skeleton(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Skeleton"
        self.speed_delay = 3
        self.max_health = 12
        self.health = self.max_health
        self.color = COLOR.WHITE
        self.id = 601

class HauntedMansionGhost(Enemy): # name already in use for regular levels
    def __init__(self) -> None:
        super().__init__()
        self.name = "Ghost"
        self.speed_delay = 5
        self.max_health = 30
        self.health = self.max_health
        self.color = COLOR.LIGHT_BLUE
        self.id = 602
        self.invisible_flag = True

class Witch(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Witch"
        self.speed_delay = 8
        self.max_health = 50
        self.health = self.max_health
        self.color = COLOR.PURPLE
        self.id = 603

class Bat(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Bat"
        self.speed_delay = 2
        self.max_health = 10
        self.health = self.max_health
        self.color = COLOR.BLACK
        self.id = 604
        self.air_flag = True

class Vampire(Enemy): # summons bats
    def __init__(self) -> None:
        super().__init__()
        self.name = "Vampire"
        self.speed_delay = 8
        self.max_health = 150
        self.health = self.max_health
        self.color = COLOR.DARK_PURPLE
        self.id = 605

class Wolf(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Wolf"
        self.speed_delay = 3
        self.max_health = 50
        self.health = self.max_health
        self.color = COLOR.BROWN
        self.id = 606

class Gravedigger(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Gravedigger"
        self.speed_delay = 8
        self.max_health = 100
        self.health = self.max_health
        self.color = COLOR.GRAY
        self.id = 607
        self.defense = 0.3

class Scarecrow(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Scarecrow"
        self.speed_delay = 5
        self.max_health = 200
        self.health = self.max_health
        self.color = COLOR.LIGHT_BROWN
        self.id = 608

class Necromancer(Enemy): # summons zombies
    def __init__(self) -> None:
        super().__init__()
        self.name = "Necromancer"
        self.speed_delay = 12
        self.max_health = 500
        self.health = self.max_health
        self.color = COLOR.PURPLE
        self.id = 609

class JackOLantern(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Jack O' Lantern"
        self.speed_delay = 5
        self.max_health = 500
        self.health = self.max_health
        self.color = COLOR.ORANGE
        self.id = 610
        self.defense = 0.3

class BroomWitch(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Witch"
        self.speed_delay = 8
        self.max_health = 500
        self.health = self.max_health
        self.color = COLOR.PURPLE
        self.id = 611
        self.air_flag = True

class Wraith(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Wraith"
        self.speed_delay = 5
        self.max_health = 1000
        self.health = self.max_health
        self.color = COLOR.LIGHT_GRAY
        self.id = 612
        self.air_flag = True

class Reaper(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Reaper"
        self.speed_delay = 5
        self.max_health = 2000
        self.health = self.max_health
        self.color = COLOR.DARK_GRAY
        self.id = 613
        self.defense = 0.2

class HauntedHayride(Enemy): # zombies, skeletons, scarecrows, etc. emerge when health reaches 0
    def __init__(self) -> None: 
        super().__init__()
        self.name = "Haunted Hayride"
        self.speed_delay = 12
        self.max_health = 5000
        self.health = self.max_health
        self.color = COLOR.DARK_YELLOW
        self.id = 614
        self.defense = 0.3

class Werewolf(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Werewolf"
        self.speed_delay = 5
        self.max_health = 1000
        self.health = self.max_health
        self.color = COLOR.BROWN
        self.id = 615

class BuriedSoul(Enemy): # emerges from the ground in the middle of the path instead of at the start
    def __init__(self) -> None:
        super().__init__()
        self.name = "Buried Soul"
        self.speed_delay = 6
        self.max_health = 250
        self.health = self.max_health
        self.color = COLOR.DARK_GRAY
        self.id = 616

class Frankenstein(Enemy): # regenerates Frankenstein's Monster's health over time, speed changes to 3 if monster dies
    def __init__(self) -> None:
        super().__init__()
        self.name = "Frankenstein"
        self.speed_delay = 8
        self.max_health = 200
        self.health = self.max_health
        self.color = COLOR.DARK_GRAY
        self.id = 617

class FrankensteinsMonster(Enemy): # speed changes to 12 if Frankenstein dies
    def __init__(self) -> None:
        super().__init__()
        self.name = "Frankenstein's Monster"
        self.speed_delay = 8
        self.max_health = 5000
        self.health = self.max_health
        self.color = COLOR.GREEN
        self.id = 618
        self.defense = 0.3

class HeadlessHorseman(Enemy): # puts zombies, skeletons, scarecrows, witches, and vampires on horseback (speed changes to 3)
    def __init__(self) -> None:
        super().__init__()
        self.name = "Headless Horseman"
        self.speed_delay = 3
        self.max_health = 3000
        self.health = self.max_health
        self.color = COLOR.DARK_ORANGE
        self.id = 619

class GrimReaper(Enemy): # heals 500 hp and does swiping animation every 5 seconds
    def __init__(self) -> None:
        super().__init__()
        self.name = "Grim Reaper"
        self.speed_delay = 8
        self.max_health = 10000
        self.health = self.max_health
        self.color = COLOR.BLACK
        self.id = 620

class HauntedSpirit(Enemy):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Haunted Spirit"
        self.speed_delay = 5
        self.max_health = 20000
        self.health = self.max_health
        self.color = COLOR.DARK_GRAY
        self.id = 621
        self.boss_flag = True

# endregion