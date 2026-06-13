import pygame
import math
from settings import window_width, window_height

class UIManager:
    def __init__(self):
        pygame.font.init()
        try:
            self.font_title = pygame.font.Font("Ole-Regular.ttf", 100)    # main menu
            self.font_header = pygame.font.Font("Ole-Regular.ttf", 55)     # card titles            
            self.font_large = pygame.font.Font("DancingScript-SemiBold.ttf", 40)  # hud numbers
            self.font_medium = pygame.font.Font("DancingScript-SemiBold.ttf", 32) # buttons, subtitles
            self.font_small = pygame.font.Font("DancingScript-SemiBold.ttf", 24)  # instructions, labels
        except FileNotFoundError:
            print("Return to system fonts if the ttf files are not found")
            self.font_title = pygame.font.SysFont("avenir", 100, bold=True)
            self.font_header = pygame.font.SysFont("avenir", 55, bold=True)
            self.font_large = pygame.font.SysFont("avenir", 40, bold=True)
            self.font_medium = pygame.font.SysFont("avenir", 32, bold=True)
            self.font_small = pygame.font.SysFont("avenir", 24)

        self.bg_color = (231, 244, 223)      
        self.leaf_color = (87, 109, 75)      
        self.branch_color = (51, 64, 45)     
        self.text_color = self.bg_color      
        self.accent_color = self.leaf_color  
        self.warning_color = (210, 100, 100) 
        self.overlay_color = (51, 64, 45, 160) 
        
        self.play_button_rect = None
        self.tutorial_button_rect = None
        self.tutorial_play_button_rect = None
        self.restart_button_rect = None
        self.home_button_rect = None
        self.reset_button_rect = None

        self.icon_water = self._create_hd_icon("water", 35)
        self.icon_branch = self._create_hd_icon("branch", 40)
        self.icon_home = self._create_hd_icon("home", 50)
        self.icon_reset = self._create_hd_icon("reset", 50)

    def draw_main_menu(self, surface):
        surface.fill(self.bg_color)
        title_surf = self.font_title.render("Sprout", True, self.branch_color)
        title_rect = title_surf.get_rect(midbottom=(window_width // 2, window_height // 2 - 50))
        surface.blit(title_surf, title_rect)

       # logo
        time_now = pygame.time.get_ticks()
        sway = math.sin(time_now / 400) * 12  
        base_x = window_width // 2
        base_y = window_height // 2 + 50
        branch_length = 60
        angle_rad = math.radians(-90 + sway)
        end_x = base_x + branch_length * math.cos(angle_rad)
        end_y = base_y + branch_length * math.sin(angle_rad)
        pygame.draw.ellipse(surface, (101, 67, 33), (base_x - 35, base_y - 10, 70, 25))
        pygame.draw.line(surface, self.branch_color, (base_x, base_y), (end_x, end_y), 8)

        # animated leaves
        pulse = abs(math.sin(time_now / 300)) * 4
        leaf_width = int(30 + pulse)
        leaf_height = int(15 + pulse)
        leaf_surf = pygame.Surface((leaf_width, leaf_height), pygame.SRCALPHA)
        pygame.draw.ellipse(leaf_surf, self.leaf_color, (0, 0, leaf_width, leaf_height))

        left_leaf = pygame.transform.rotate(leaf_surf, 135 - sway)
        left_rect = left_leaf.get_rect(center=(end_x - 10, end_y - 8))
        surface.blit(left_leaf, left_rect)
        right_leaf = pygame.transform.rotate(leaf_surf, -45 - sway)
        right_rect = right_leaf.get_rect(center=(end_x + 10, end_y + 8))
        surface.blit(right_leaf, right_rect)
        
        btn_width = 260
        btn_height = 70
        self.play_button_rect = pygame.Rect(
            (window_width // 2 - btn_width // 2, base_y + 70), 
            (btn_width, btn_height)
        )
        
        shadow_rect = self.play_button_rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(surface, (51, 64, 45, 60), shadow_rect, border_radius=35)
        pygame.draw.rect(surface, self.leaf_color, self.play_button_rect, border_radius=35)
        
        btn_text = self.font_medium.render("Start Growing", True, self.bg_color)
        btn_text_rect = btn_text.get_rect(center=self.play_button_rect.center)
        surface.blit(btn_text, btn_text_rect)

        self.tutorial_button_rect = pygame.Rect(
            (window_width // 2 - btn_width // 2, self.play_button_rect.bottom + 20), 
            (btn_width, btn_height)
        )
        
        tut_shadow_rect = self.tutorial_button_rect.copy()
        tut_shadow_rect.y += 4
        pygame.draw.rect(surface, (51, 64, 45, 60), tut_shadow_rect, border_radius=35)
        pygame.draw.rect(surface, self.branch_color, self.tutorial_button_rect, border_radius=35)
        
        tut_text = self.font_medium.render("Tutorial", True, self.bg_color)
        tut_text_rect = tut_text.get_rect(center=self.tutorial_button_rect.center)
        surface.blit(tut_text, tut_text_rect)

    def draw_tutorial(self, surface):
        overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        overlay.fill((231, 244, 223, 200))  
        surface.blit(overlay, (0, 0))
        card_width = 560
        card_height = 420
        card_rect = pygame.Rect((window_width // 2 - card_width // 2, 
                                 window_height // 2 - card_height // 2), 
                                (card_width, card_height))
        shadow_rect = card_rect.copy()
        shadow_rect.y += 6
        pygame.draw.rect(surface, (51, 64, 45, 60), shadow_rect, border_radius=25)
        pygame.draw.rect(surface, self.leaf_color, card_rect, border_radius=25)
        pygame.draw.rect(surface, self.bg_color, card_rect, width=4, border_radius=25)

        # title
        title_surf = self.font_large.render("How to Play", True, self.bg_color)
        title_rect = title_surf.get_rect(midtop=(card_rect.centerx, card_rect.top + 30))
        surface.blit(title_surf, title_rect)

        # instructions
        instructions = [
            "1. Click a branch to grow a new one.",
            "2. Growing costs Energy. Catch rain to recharge!",
            "3. Watch the Tilt! Keep the gravity balanced.",
            "4. Reach the branch goal with a tilt",
            "   between -100 and 100."
        ]
        
        start_y = title_rect.bottom + 35
        for i, text in enumerate(instructions):
            inst_surf = self.font_small.render(text, True, self.bg_color)
            inst_rect = inst_surf.get_rect(topleft=(card_rect.left + 40, start_y + (i * 45)))
            surface.blit(inst_surf, inst_rect)

        # "let's grow" button
        btn_width = 220
        btn_height = 60
        self.tutorial_play_button_rect = pygame.Rect(
            (card_rect.centerx - btn_width // 2, card_rect.bottom - 70), 
            (btn_width, btn_height)
        )
        
        pygame.draw.rect(surface, self.branch_color, self.tutorial_play_button_rect, border_radius=30)
        
        btn_text = self.font_medium.render("Let's Grow!", True, self.bg_color)
        btn_text_rect = btn_text.get_rect(center=self.tutorial_play_button_rect.center)
        surface.blit(btn_text, btn_text_rect)

    def _create_hd_icon(self, icon_type, final_size):
        import math
        large_size = final_size * 4
        surf = pygame.Surface((large_size, large_size), pygame.SRCALPHA)
        
        if icon_type == "water":
            # Draw Water Drop
            center_x, center_y = large_size // 2, int(large_size * 0.6)
            radius = int(large_size * 0.3)
            pygame.draw.circle(surf, (100, 170, 230), (center_x, center_y), radius)
            pygame.draw.polygon(surf, (100, 170, 230), [
                (center_x - radius, center_y), 
                (center_x + radius, center_y), 
                (center_x, int(large_size * 0.1))
            ])
            
        elif icon_type == "branch":
            # Draw Branch
            c = (120, 80, 50)
            pygame.draw.line(surf, c, (int(large_size*0.2), int(large_size*0.9)), (int(large_size*0.9), int(large_size*0.2)), 16)
            pygame.draw.line(surf, c, (int(large_size*0.5), int(large_size*0.6)), (int(large_size*0.8), int(large_size*0.8)), 12)
            pygame.draw.line(surf, c, (int(large_size*0.35), int(large_size*0.75)), (int(large_size*0.2), int(large_size*0.5)), 10)
            
        elif icon_type == "home":
            c = (20, 20, 20)
            pygame.draw.circle(surf, c, (large_size//2, large_size//2), (large_size//2) - 4, 12)
            pygame.draw.line(surf, c, (int(large_size*0.7), large_size//2), (int(large_size*0.3), large_size//2), 12)
            pygame.draw.line(surf, c, (int(large_size*0.3), large_size//2), (int(large_size*0.5), int(large_size*0.3)), 12)
            pygame.draw.line(surf, c, (int(large_size*0.3), large_size//2), (int(large_size*0.5), int(large_size*0.7)), 12)
            
        elif icon_type == "reset":
            c = (20, 20, 20)
            pygame.draw.circle(surf, c, (large_size//2, large_size//2), (large_size//2) - 4, 12)
            arc_rect = pygame.Rect(int(large_size*0.2), int(large_size*0.2), int(large_size*0.6), int(large_size*0.6))
            pygame.draw.arc(surf, c, arc_rect, math.radians(45), math.radians(315), 12)
            # Arrowhead
            pygame.draw.polygon(surf, c, [
                (int(large_size*0.7), int(large_size*0.2)), 
                (int(large_size*0.9), int(large_size*0.45)), 
                (int(large_size*0.5), int(large_size*0.45))
            ])
            
        return pygame.transform.smoothscale(surf, (final_size, final_size))

    def draw_hud(self, surface, level, energy, branches, win_goal, tilt, max_tilt):
        black = (20, 20, 20)
        top_y = 50
        bottom_y = 120

        self.home_button_rect = self.icon_home.get_rect(center=(50, top_y))
        surface.blit(self.icon_home, self.home_button_rect)

        lvl_text = self.font_large.render(f"Level {level}", True, black)
        lvl_rect = lvl_text.get_rect(center=(window_width // 2, top_y))
        surface.blit(lvl_text, lvl_rect)

        self.reset_button_rect = self.icon_reset.get_rect(center=(window_width - 50, top_y))
        surface.blit(self.icon_reset, self.reset_button_rect)

        water_rect = self.icon_water.get_rect(center=(60, bottom_y))
        surface.blit(self.icon_water, water_rect)
        e_text = self.font_large.render(f": {energy}", True, black)
        surface.blit(e_text, e_text.get_rect(midleft=(water_rect.right + 5, bottom_y)))

        b_text = self.font_large.render(f": {branches}/{win_goal}", True, black)
        total_branch_width = self.icon_branch.get_width() + 5 + b_text.get_width()
        start_x = (window_width // 2) - (total_branch_width // 2)        
        branch_rect = self.icon_branch.get_rect(midleft=(start_x, bottom_y))
        surface.blit(self.icon_branch, branch_rect)
        surface.blit(b_text, b_text.get_rect(midleft=(branch_rect.right + 5, bottom_y)))
        tilt_label = self.font_small.render("Tilt: ", True, black)
        tilt_label_rect = tilt_label.get_rect(midleft=(window_width - 140, bottom_y + 4))
        surface.blit(tilt_label, tilt_label_rect)
        tilt_color = self.warning_color if abs(tilt) > (max_tilt * 0.8) else black
        t_text = self.font_large.render(f"{int(tilt)}", True, tilt_color)
        t_text_rect = t_text.get_rect(midleft=(tilt_label_rect.right + 5, bottom_y))
        surface.blit(t_text, t_text_rect)

    def draw_overlay_card(self, surface, title, subtitle, branches, button_text="Plant Again"):
        overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        overlay.fill((231, 244, 223, 140))  
        surface.blit(overlay, (0, 0))

        card_width = 440
        card_height = 320
        card_rect = pygame.Rect((window_width // 2 - card_width // 2, 
                                 window_height // 2 - card_height // 2), 
                                (card_width, card_height))
        
        shadow_rect = card_rect.copy()
        shadow_rect.y += 6
        pygame.draw.rect(surface, (51, 64, 45, 60), shadow_rect, border_radius=25)
        
        pygame.draw.rect(surface, self.leaf_color, card_rect, border_radius=25)
        pygame.draw.rect(surface, self.bg_color, card_rect, width=4, border_radius=25)

        title_surf = self.font_large.render(title, True, self.bg_color)
        title_rect = title_surf.get_rect(midtop=(card_rect.centerx, card_rect.top + 40))
        surface.blit(title_surf, title_rect)

        sub_surf = self.font_small.render(subtitle, True, self.bg_color)
        sub_rect = sub_surf.get_rect(midtop=(card_rect.centerx, title_rect.bottom + 15))
        surface.blit(sub_surf, sub_rect)

        stats_surf = self.font_medium.render(f"Final Branches: {branches}", True, self.bg_color)
        stats_rect = stats_surf.get_rect(midtop=(card_rect.centerx, sub_rect.bottom + 30))
        surface.blit(stats_surf, stats_rect)

        btn_width = 220
        btn_height = 60
        self.restart_button_rect = pygame.Rect(
            (card_rect.centerx - btn_width // 2, card_rect.bottom - 80), 
            (btn_width, btn_height)
        )
        
        pygame.draw.rect(surface, self.branch_color, self.restart_button_rect, border_radius=30)
        
        btn_text = self.font_medium.render(button_text, True, self.bg_color)
        btn_text_rect = btn_text.get_rect(center=self.restart_button_rect.center)
        surface.blit(btn_text, btn_text_rect)

    def draw_game_over(self, surface, branches):
        self.draw_overlay_card(
            surface, 
            title="Game Over!", 
            subtitle="The center of gravity shifted too far.", 
            branches=branches,
            button_text="Try Again"
        )

    def draw_blooming(self, surface, branches):
        self.draw_overlay_card(
            surface, 
            title="Perfect Balance!", 
            subtitle="Your tree has fully bloomed.", 
            branches=branches,
            button_text="Grow Another"
        )