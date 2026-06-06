import pygame
from settings import window_width, window_height

class UIManager:
    def __init__(self):
        pygame.font.init()
        self.font_large = pygame.font.SysFont("avenir", 48, bold=True)
        self.font_medium = pygame.font.SysFont("avenir", 32, bold=True)
        self.font_small = pygame.font.SysFont("avenir", 24)
        self.text_color = (245, 245, 245)
        self.accent_color = (144, 238, 144) 
        self.warning_color = (255, 100, 100)
        self.overlay_color = (30, 30, 30, 180) 
        self.restart_button_rect = None
    def draw_hud(self, surface, level, energy, branches, win_goal, tilt, max_tilt):
        top_bar = pygame.Surface((window_width, 50), pygame.SRCALPHA)
        top_bar.fill(self.overlay_color)
        surface.blit(top_bar, (0, 0))

       
        stats_text = self.font_small.render(f"Level: {level}   |   Energy: {energy}", True, self.text_color)
        surface.blit(stats_text, (20, 12))
        branch_text = self.font_small.render(f"Branches: {branches} / {win_goal}", True, self.text_color)
        branch_rect = branch_text.get_rect(center=(window_width // 2, 25))
        surface.blit(branch_text, branch_rect)
        tilt_color = self.warning_color if abs(tilt) > (max_tilt * 0.8) else self.text_color
        tilt_text = self.font_small.render(f"Tilt: {int(tilt)}", True, tilt_color)
        tilt_rect = tilt_text.get_rect(midright=(window_width - 20, 25))
        surface.blit(tilt_text, tilt_rect)

    def draw_message_overlay(self, surface, title, subtitle, color):
        """Helper method to draw centered screen overlays."""
        overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120)) 
        surface.blit(overlay, (0, 0))

        title_text = self.font_large.render(title, True, color)
        title_rect = title_text.get_rect(center=(window_width // 2, window_height // 2 - 20))
        
        subtitle_text = self.font_medium.render(subtitle, True, self.text_color)
        subtitle_rect = subtitle_text.get_rect(center=(window_width // 2, window_height // 2 + 30))

        surface.blit(title_text, title_rect)
        surface.blit(subtitle_text, subtitle_rect)

    def draw_limbo_warning(self, surface, tilt):
        """Shows the player exactly how to balance the tree to win."""
        direction = "RIGHT" if tilt < 0 else "LEFT"
        
        warning_box = pygame.Surface((window_width, 60), pygame.SRCALPHA)
        warning_box.fill((0, 0, 0, 200))
        surface.blit(warning_box, (0, window_height - 60))

        msg = f"Goal Reached! Build {direction} to balance the tree."
        text = self.font_medium.render(msg, True, self.accent_color)
        rect = text.get_rect(center=(window_width // 2, window_height - 30))
        surface.blit(text, rect)

    def draw_game_over(self, surface, reason="The tree snapped under its own weight."):
        self.draw_message_overlay(surface, "GAME OVER", reason, self.warning_color)
        

        button_width = 200
        button_height = 50
        self.restart_button_rect = pygame.Rect(
            window_width // 2 - button_width // 2,
            window_height // 2 + 70,
            button_width, 
            button_height
        )
        
        pygame.draw.rect(surface, self.accent_color, self.restart_button_rect, border_radius=10)
        
        restart_text = self.font_medium.render("Restart Game", True, (30, 30, 30)) 
        text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
        surface.blit(restart_text, text_rect)

        hint_text = self.font_small.render("or press [R]", True, self.text_color)
        hint_rect = hint_text.get_rect(center=(window_width // 2, window_height // 2 + 140))
        surface.blit(hint_text, hint_rect)

    def draw_blooming(self, surface, level):
        self.draw_message_overlay(surface, "PERFECT BALANCE", f"Level {level} Cleared!", self.accent_color)