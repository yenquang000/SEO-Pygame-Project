import pygame
import math
from settings import *

class BranchNode:
    def __init__(self, x, y, parent=None, leaf_img=None, branch_img=None):
        self.pos = pygame.math.Vector2(x, y)
        self.parent = parent
        self.children = []  
        self.radius = 12  
        
        self.leaf_img = leaf_img
        self.leaf_surface = None
        self.leaf_rect = None
        self.angle = 0
        
        self.is_blooming = False
      
        if self.parent:
            self.calculate_geometry()

    def calculate_geometry(self):
        dx = self.pos.x - self.parent.pos.x
        dy = self.pos.y - self.parent.pos.y
        self.angle = math.degrees(math.atan2(-dy, dx)) 
        
        if self.leaf_img:
            
            self.leaf_surface = pygame.transform.rotate(self.leaf_img, self.angle)
        
            self.leaf_rect = self.leaf_surface.get_rect(center=(self.pos.x, self.pos.y))

    def add_child(self, angle_degrees, length):
        direction = pygame.math.Vector2(0, -length).rotate(angle_degrees)
        new_pos = self.pos + direction
        
        new_node = BranchNode(
            new_pos.x, 
            new_pos.y, 
            parent=self,
            leaf_img=self.leaf_img
        )
        self.children.append(new_node)
        return new_node

    def trigger_bloom(self):
        self.is_blooming = True
        for child in self.children:
            child.trigger_bloom()

    def draw(self, surface):
        
        if self.parent:
            pygame.draw.line(surface, branch_color, self.parent.pos, self.pos, width=8)

        for child in self.children:
            child.draw(surface)
            
        if self.leaf_surface:
            surface.blit(self.leaf_surface, self.leaf_rect.topleft)
            
            if self.is_blooming:
                flower_color = (255, 183, 197) 
                core_color = (255, 105, 180)
                pygame.draw.circle(surface, flower_color, (int(self.pos.x), int(self.pos.y)), 10)
                pygame.draw.circle(surface, core_color, (int(self.pos.x), int(self.pos.y)), 4)
            

    def get_clicked_node(self, mouse_pos):
        mouse_vec = pygame.math.Vector2(mouse_pos)
        if self.pos.distance_to(mouse_vec) <= self.radius:
            return self
        for child in self.children:
            clicked_child = child.get_clicked_node(mouse_pos)
            if clicked_child:
                return clicked_child
        return None
    
    def calculate_balance(self, center_x):
        tilt = self.pos.x - center_x
        for child in self.children:
            tilt += child.calculate_balance(center_x)
        return tilt
        
    def count_branches(self):
        total = 1 
        for child in self.children:
            total += child.count_branches()
        return total
    
    def check_rain_collision(self, drop_pos, drop_radius):
        if self.parent:
            A = self.parent.pos
            B = self.pos
            P = drop_pos
            
            AB = B - A
            AP = P - A
            
            length_squared = AB.length_squared()
            if length_squared > 0:
                t = max(0, min(1, AP.dot(AB) / length_squared))
                closest_point = A + t * AB
                if P.distance_to(closest_point) <= drop_radius + 3:
                    return True

        if self.pos.distance_to(drop_pos) <= self.radius + drop_radius:
            return True

        for child in self.children:
            if child.check_rain_collision(drop_pos, drop_radius):
                return True
                
        return False