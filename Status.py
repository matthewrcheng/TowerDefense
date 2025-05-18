import random
import pygame
from Enemy import Enemy
from constants import CELL_SIZE


class Status:
    """
    Basic class used to store status effects
    """
    def __init__(self, name, frequency, duration, effect, color):
        self.name = name
        self.frequency = frequency
        self.frequency_timer = frequency
        self.duration = duration
        self.effect = effect
        self.color = color
        self.animation_stages = 10
        self.current_stage = 0

    def __str__(self):
        return self.name
    
    def draw_effect(self, screen: pygame.Surface, target: Enemy):
        # bottom left corner
        enemy_x = target.x * CELL_SIZE
        enemy_y = target.y * CELL_SIZE + target.height * CELL_SIZE

        stage_height = CELL_SIZE / self.animation_stages

        current_y = enemy_y - self.current_stage * stage_height

        for _ in range(10):
            bubble_x = enemy_x + random.randint(0, int(target.width * CELL_SIZE))
            bubble_y = current_y + random.randint(0, int(stage_height))
            pygame.draw.circle(screen, self.color, (bubble_x, bubble_y), 2)

        self.current_stage = (self.current_stage + 1) % self.animation_stages

    
    def game_tick(self, screen: pygame.Surface, target: Enemy):
        self.duration -= 1
        self.frequency_timer -= 1
        # draw effect
        self.draw_effect(screen, target)
        if self.frequency_timer == 0:
            self.frequency_timer = self.frequency
            return self.action(target)

    def action(self, target):
        # effect
        return 

class DamagingStatus(Status):
    def __init__(self, name, frequency, duration, effect, color, damage):
        super().__init__(name, frequency, duration, effect, color)
        self.damage = damage

    def action(self, target: Enemy) -> Enemy:
        print(f"{self.name} dealing {self.damage} damage to {target.name}")
        return target.damage(self.damage)

class Poison(DamagingStatus):
    def __init__(self, name, frequency, duration, effect, color, damage):
        super().__init__(name, frequency, duration, effect, color, damage)

class Burn(DamagingStatus):
    def __init__(self, name, frequency, duration, effect, color, damage):
        super().__init__(name, frequency, duration, effect, color, damage)

class FrostBite(DamagingStatus):
    def __init__(self, name, frequency, duration, effect, color, damage):
        super().__init__(name, frequency, duration, effect, color, damage)

class Frozen(Status):
    def __init__(self, name, frequency, duration, effect, color):
        super().__init__(name, frequency, duration, effect, color)

class Slow(Status):
    def __init__(self, name, frequency, duration, effect, color):
        super().__init__(name, frequency, duration, effect, color)

class Regen(Status):
    def __init__(self, name, frequency, duration, effect, color):
        super().__init__(name, frequency, duration, effect, color)