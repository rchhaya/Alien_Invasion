import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class for the alien"""
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        #Load image and access rects
        self.image = pygame.image.load("files\\ufo.bmp")
        self.rect = self.image.get_rect()

        #Start at topleft, but offset by one UFO from each corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store float of the x-position
        self.alien_x = float(self.rect.x) #- this only causes 4 aliens to show up instead of the 24 needed
        #Debugging
        self.xnum = 0
        self.ynum = 0
    
    def draw_alien(self):
        """Draws alien at top left"""
        self.screen.blit(self.image, self.rect)

    def edge_checker(self):
        """True if alien is on edge"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Moves the alien to the right"""
        #print('*' + str(self.alien_x))
        self.alien_x += self.settings.a_speed_factor * self.settings.alien_direction             

        self.rect.x = self.alien_x
        #print(str(self.alien_x))

        
        

