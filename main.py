import pygame
import random
from settings import *
from tree import BranchNode
from rain import Raindrop
from ui import UIManager  

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("SPROUT")
clock = pygame.time.Clock()
ui = UIManager()
leaf_image = pygame.Surface((30, 15), pygame.SRCALPHA)
pygame.draw.ellipse(leaf_image, (144, 238, 144), (0, 0, 30, 15))

def create_tree():
    return BranchNode(
        window_width // 2, 
        window_height - 50, 
        leaf_img=leaf_image, 
    )

root = create_tree()
gameIsRunning = True
game_state = "PLAYING" 
loss_message = ""
MAX_TILT = 2000 
PERFECT_BALANCE_TOLERANCE = 100  #win from -100 to 100
level = 1
raindrops = []
energy = 5
bloom_timer = 0

while gameIsRunning: 
    win_goal = level * 10 #add 10 branches after every level
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameIsRunning = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "TUTORIAL":
                game_state = "PLAYING"
                
            elif game_state == "PLAYING" and energy > 0:
                mouse_pos = pygame.mouse.get_pos()
                clicked_node = root.get_clicked_node(mouse_pos)
                if clicked_node:
                    random_angle = random.uniform(-45, 45)
                    clicked_node.add_child(random_angle, length=60)
                    energy -= 1 
                    
            elif game_state == "LOST":
                if ui.restart_button_rect and ui.restart_button_rect.collidepoint(event.pos):
                    level = 1
                    energy = 5
                    raindrops.clear()
                    root = create_tree()
                    game_state = "TUTORIAL"

    if game_state == "PLAYING":
        if random.random() < 0.015: 
            random_x = random.randint(0, window_width)
            raindrops.append(Raindrop(random_x, 0))

        for drop in raindrops[:]: 
            drop.update()
            if root.check_rain_collision(drop.pos, drop.radius):
                raindrops.remove(drop)
                energy += 1 
            elif drop.is_off_screen():
                raindrops.remove(drop)
                
        current_tilt = root.calculate_balance(window_width // 2)
        total_branches = root.count_branches()
        #unbalanced tree, lost
        if abs(current_tilt) > MAX_TILT:
            game_state = "LOST"
            loss_message = "The tree is not balanced."

        #balanced tree, win
        elif total_branches >= win_goal:
            if abs(current_tilt) <= PERFECT_BALANCE_TOLERANCE:
                game_state = "BLOOMING"
                root.trigger_bloom()  
                bloom_timer = pygame.time.get_ticks()
            else:
                game_state = "LOST"
                loss_message = f"Out of branches! Final tilt was {int(current_tilt)}."
            
    elif game_state == "BLOOMING":
        pygame.display.set_caption(f"Perfect Balance! (Level {level} Cleared!)")
        
        if pygame.time.get_ticks() - bloom_timer > 3000:
            level += 1
            root = create_tree()
            energy += 5  
            raindrops.clear()
            game_state = "PLAYING"

    screen.fill(bg_color)
    base_x = window_width // 2
    base_y = window_height - 50
    mound_color = (101, 67, 33) 
    pygame.draw.ellipse(screen, mound_color, (base_x - 40, base_y - 15, 80, 30))
    root.draw(screen)
    for drop in raindrops:
        drop.draw(screen)
    if game_state == "PLAYING":
        ui.draw_hud(screen, level, energy, total_branches, win_goal, current_tilt, MAX_TILT)
            
    elif game_state == "LOST":
        ui.draw_game_over(screen, loss_message)
        
    elif game_state == "BLOOMING":
        ui.draw_blooming(screen, level)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()