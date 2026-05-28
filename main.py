import pygame
from settings import *
pygame.init()
screen=pygame.display.set_mode((window_height),(window_width))
pygame.display.set_caption("SEO Project")
gameIsRunning = True
while gameIsRunning: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameIsRunning = False
    pygame.display.flip()
pygame.quit()