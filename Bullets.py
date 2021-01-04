import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Manages bullets that are fired"""
    def __init__(self, settings, screen, ship):
        super().__init__()
        self.screen = screen

        #Create a bullet rect and align it
        self.rect = pygame.Rect(0,0,settings.bullet_width, settings.bullet_length)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        #Attributes of bullet
        self.bullet_color = settings.bullet_color
        self.bullet_speed = settings.b_speed_factor
        #Store vertical position of bullet in a float
        self.bullet_y = float(self.rect.y)

    def update(self):
        """Moved bullet up"""
        self.bullet_y -= self.bullet_speed
        self.rect.y = self.bullet_y
    
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)