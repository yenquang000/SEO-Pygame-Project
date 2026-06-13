import pygame
from settings import *

class Raindrop:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 5) 
        self.radius = 3 

    def update(self):
        self.pos += self.velocity

    def draw(self, surface):
        rain_color = (111, 143, 175)
        pygame.draw.circle(surface, rain_color, (int(self.pos.x), int(self.pos.y)), self.radius)
        
    def is_off_screen(self):
        return self.pos.y > window_height