import sys
import pygame
import Alien_Game_Functions as agf
from pygame.sprite import Sprite
from pygame.sprite import Group
import pygame.font

class Settings():
    """Class for the settings of the game"""
    def __init__(self):
        """Initializes the game settings"""
        self.scr_display_width = 1000
        self.scr_display_height = 700
        self.back_color = (64,32,128)

        #Initializes the ship settings
        self.ship_lives = 3

        #Initializes the bullet settings
        self.b_speed_factor = 1.1
        self.bullet_width = 10
        self.bullet_length = 15
        self.bullet_color = (224,224,224)
        self.bullet_limit = 5

        #Initializes the alien settings
        self.a_drop_factor = 10
        
        #Speedup factor
        self.speedup_factor = 1.15
        self.points_multiplier = 1.5
        self.changing_settings()

    def changing_settings(self):
        """Initlialize the settings that change - speed and direction"""
        self.s_speed_factor = 1.5
        self.b_speed_factor = 1.25
        self.a_speed_factor = 1
        #1 is right, -1 is left
        self.alien_direction = 1
        self.a_points = 20
    
    def level_up(self):
        """Increase the speed of different factors"""
        self.s_speed_factor *= self.speedup_factor
        self.a_speed_factor *= self.speedup_factor
        self.a_speed_factor *= self.speedup_factor
        self.a_points = int(self.a_points * self.points_multiplier)

class Statistics():
    """Class to track stats for the game"""
    def __init__(self, settings):
        """Initalizes static stats"""
        self.settings = settings
        self.game_on = False
        self.high_score = 0
        self.reset()

    def reset(self):
        """Initialize stats that will change"""
        self.ships_remaining = self.settings.ship_lives
        self.points = 0
        self.current_level = 1

class Scoreboard():
    """Creates a scoreboard to keep track of score"""
    def __init__(self, settings, screen, statistics):
        self.screen = screen
        self.settings = settings
        self.statistics = statistics
        self.s_rect = screen.get_rect()
        #Fonts
        self.t_color = (240,240,240)
        self.t_font = pygame.font.SysFont(None, 36)
        
        self.init_score(statistics)
        self.init_high_score(statistics)
        self.init_level(statistics)
        self.init_ship(statistics)
    
    def init_score(self, statistics):
        """Score --> Image"""
        rounded = round(statistics.points, -1)
        rounded2 = '{:,}'.format(rounded)
        string_score = 'Score: ' + rounded2
        self.score_img = self.t_font.render(string_score, True, self.t_color, self.settings.back_color)
        self.sc_rect = self.score_img.get_rect()
        self.sc_rect.right = self.s_rect.right - 15
        self.sc_rect.top = 15

    def init_high_score(self, statistics):
        """High Score --> Image"""
        rounded_hscore = round(statistics.high_score, -1)
        rounded_hscore2 = '{:,}'.format(rounded_hscore)
        rounded_hscore_str = 'High Score: ' + rounded_hscore2
        self.hscore_img = self.t_font.render(rounded_hscore_str, True, self.t_color, self.settings.back_color)

        #Center it at the top
        self.hs_rect = self.hscore_img.get_rect()
        self.hs_rect.centerx = self.s_rect.centerx
        self.hs_rect.top = self.s_rect.top

    def init_level(self, statistics):
        """Level --> Image"""
        self.level_img = self.t_font.render('Level: ' + str(statistics.current_level), True, self.t_color, self.settings.back_color)

        #Position below score
        self.l_rect = self.level_img.get_rect()
        self.l_rect.right = self.sc_rect.right
        self.l_rect.top = self.sc_rect.bottom + 15

    def init_ship(self, statistics):
        self.ships_group = Group()
        for ship in range(statistics.ships_remaining):
            new_ship = Ship(self.settings, self.screen)
            new_ship.rect.x = (ship*new_ship.rect.width) + 5
            new_ship.rect.y = 5
            self.ships_group.add(new_ship)

    def draw_score(self):
        """Draw the scoreboard and high score"""
        self.screen.blit(self.score_img, self.sc_rect)
        self.screen.blit(self.hscore_img, self.hs_rect)
        self.screen.blit(self.level_img, self.l_rect)
        self.ships_group.draw(self.screen)

class Button():
    """Creates a button to start the game"""
    def __init__(self, settings, screen, message):
        self.screen = screen
        self.settings = settings
        self.s_rect = screen.get_rect()
        self.message = message
        #Characteristics of the button
        self.b_width, self.b_height = 200, 50
        self.b_color = (92, 204, 206)
        self.t_color = (75, 37, 109)
        self.b_font = pygame.font.SysFont(None, 48)

        #Center the rect
        self.rect = pygame.Rect(0, 0, self.b_width, self.b_height)
        self.rect.center = self.s_rect.center

        #Message
        self.craft_message()

    def craft_message(self):
        """Creates an image for the message and it centers it"""
        self.message_img = self.b_font.render(self.message, True, self.t_color, self.b_color)
        self.m_rect = self.message_img.get_rect()
        self.m_rect.center = self.rect.center
    
    def draw_button(self):
        """Fills and draws button to screen"""
        self.screen.fill(self.b_color, self.rect)
        self.screen.blit(self.message_img, self.m_rect)



class Ship(Sprite):
    """Class to create the spaceship"""
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        #Load image and get its rect
        self.image = pygame.image.load("files\\spaceship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #Ship at bottom center
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        #Movement flags
        self.moving_right = False
        self.moving_left = False
        #Decimal value for ship center (since 1.75 is a decimal)
        self.image_center = float(self.rect.centerx)
    
    def draw_ship(self):
        """Draw the ship at the bottom center"""
        self.screen.blit(self.image, self.rect)
    
    def mvt_update(self):
        """Continuous rightward movement of the ship's center"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.image_center += self.settings.s_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.image_center -= self.settings.s_speed_factor

        #Save the new center as the center var
        self.rect.centerx = int(self.image_center)

    def center(self):
        """Centers the ship"""
        self.image_center = self.screen_rect.centerx


def start_game():
    #Initializes the game, creates a surface object, and creates a caption
    pygame.init()
    pygame.display.set_caption("Alien Invasion!")
   
   #Instantiating the various classes
    game_settings = Settings()
    scr_display = pygame.display.set_mode((game_settings.scr_display_width, game_settings.scr_display_height)) 
    new_ship = Ship(game_settings, scr_display)
    player_stats = Statistics(game_settings)

    start_button = Button(game_settings, scr_display, "Play now!")
    total_score = Scoreboard(game_settings, scr_display, player_stats)
    #Group to store bullets and alien
    bullets_group = Group()
    aliens_group = Group()
   
    #Alien fleet
    agf.create_alien_fleet(game_settings, scr_display, aliens_group, new_ship)
    #for alien in aliens_group:
    #   print(alien.rect.x, alien.rect.y)
    #Main game loop
    while True:
        #Listens for events
        agf.event_checker(new_ship, game_settings, scr_display, bullets_group, player_stats, start_button, aliens_group, total_score)
        
        if player_stats.game_on:
            #print(game_stats.ships_remaining)
            #Checks for ship and bullet motion
            new_ship.mvt_update()

            agf.bullets_updater(bullets_group, aliens_group, game_settings, scr_display, new_ship, player_stats, total_score)
            agf.aliens_updater(aliens_group, game_settings, new_ship, scr_display, player_stats, bullets_group, total_score)
            #agf.move_alien(aliens_group)
            #Updates Screen
        agf.screen_updater(new_ship, game_settings, scr_display, bullets_group, aliens_group, player_stats, start_button, total_score)

start_game()





