#main.py
import pygame
import random
from settings import *
from tree import BranchNode

pygame.init()
screen=pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("SEO Project")

root = BranchNode(window_width // 2, window_height-50)

gameIsRunning = True
while gameIsRunning: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameIsRunning = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_node = root.get_clicked_node(mouse_pos)
            if clicked_node:
                random_angle = random.uniform(-45, 45)
                clicked_node.add_child(random_angle, length=60)
    screen.fill(bg_color)
    root.draw(screen)
    pygame.display.flip()
pygame.quit()