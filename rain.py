import pygame
from settings import *

class Raindrop:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 5) 
        self.radius = 3 

    def update(self):
        """Called every frame to move the raindrop downwards."""
        self.pos += self.velocity

    def draw(self, surface):
        """Draws a small, pale blue circle for the raindrop."""
        rain_color = (125, 249, 255)
        pygame.draw.circle(surface, rain_color, (int(self.pos.x), int(self.pos.y)), self.radius)
        
    def is_off_screen(self):
        """Checks if the raindrop fell past the bottom of the window."""
        return self.pos.y > window_height