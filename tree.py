# tree.py
import pygame
from settings import *

class BranchNode:
    def __init__(self, x, y, parent=None):
        self.pos = pygame.math.Vector2(x, y)
        self.parent = parent
        self.children = []  
        self.radius = 12  

    def add_child(self, angle_degrees, length):
        direction = pygame.math.Vector2(0, -length).rotate(angle_degrees)
        new_pos = self.pos + direction
        new_node = BranchNode(new_pos.x, new_pos.y, parent=self)
        self.children.append(new_node)
        
        return new_node

    def draw(self, surface):
        if self.parent:
            pygame.draw.line(surface, branch_color, self.parent.pos, self.pos, width=4)
        pygame.draw.circle(surface, node_color, (int(self.pos.x), int(self.pos.y)), self.radius)

        for child in self.children:
            child.draw(surface)

    def get_clicked_node(self, mouse_pos):
        mouse_vec = pygame.math.Vector2(mouse_pos)
        if self.pos.distance_to(mouse_vec) <= self.radius:
            return self
        for child in self.children:
            clicked_child = child.get_clicked_node(mouse_pos)
            if clicked_child:
                return clicked_child
        return None