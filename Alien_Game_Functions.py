import sys
import pygame
from Bullets import Bullet
from Aliens import Alien
from time import sleep


def keypress_events(event, ship, settings, screen, bullets):
    """Responds to key presses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)

def keyup_events(event, ship):
    """Responds to key releases"""
    #If right, move the rect of the ship right (note, same variable name as used in the Ship init() function: ship.rect, ship.moving_right)
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def button_checker(statistics, button, x, y, aliens, bullets, settings, screen, ship, score):
    """Turns game on if user clicks play"""
    if button.rect.collidepoint(x,y) and not statistics.game_on:
        pygame.mouse.set_visible(False)
        settings.changing_settings()
        statistics.game_on = True
        reset_game(statistics, aliens, bullets, settings, screen, ship)
        
        #Resets game stats and re-displays them
        statistics.reset()
        score.init_score(statistics)
        score.init_high_score(statistics)
        score.init_level(statistics)
        score.init_ship(statistics)

    

def event_checker(ship, settings, screen, bullets, statistics, button, aliens, score):
    """Responds to key and mouse events"""
    for event in pygame.event.get():
        #Quitting out of the game window
        if event.type == pygame.QUIT:
            sys.exit()
        #Keypress
        elif event.type == pygame.KEYDOWN:
            keypress_events(event, ship, settings, screen, bullets)
        #Key up        
        elif event.type == pygame.KEYUP:
            keyup_events(event, ship)
        #Mouseclick
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_xpos , mouse_ypos = pygame.mouse.get_pos()
            button_checker(statistics, button, mouse_xpos, mouse_ypos, aliens, bullets, settings, screen, ship, score)

def screen_updater(ship, settings, screen, bullets, aliens, statistics, button, score):
    """Updates images on the screen and flips it to update"""
    #Redraws the screen and ship each loop iteration
    screen.fill(settings.back_color)
    #Draws a bullet for every bullet in the group
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    score.draw_score()
    ship.draw_ship()
    aliens.draw(screen)

    if not statistics.game_on:
        button.draw_button()
        
    #Updates the screen to the most recent one    
    pygame.display.flip()

def bullets_updater(bullets, aliens, settings, screen, ship, statistics, score):
    """Updates bullet position and deletes offscreen ones"""
    #Groups have a function 'update' that calls update on all items
    bullets.update()
    
    #Get rid of dead bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    collision_checker(bullets, aliens, screen, settings, ship, statistics, score)

def collision_checker(bullets, aliens, screen, settings, ship, statistics, score):
    """Check for collisions and empty fleet"""
    #Delete collisions with aliens
    collide = pygame.sprite.groupcollide(bullets, aliens, True, True)
    #print(len(aliens))
    if collide:
        for alien_hits in collide.values():
            statistics.points += (settings.a_points)*len(alien_hits)
            score.init_score(statistics)
            high_score_checker(statistics, score)
    #If all aliens are shot, create a new fleet
    if len(aliens) == 0:
        bullets.empty()
        settings.level_up()
        create_alien_fleet(settings, screen, aliens, ship)
        statistics.current_level += 1
        score.init_level(statistics)

def fire_bullet(settings, screen, ship, bullets):
    """Fire a bullet"""
    if len(bullets) < settings.bullet_limit:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)

def create_alien(settings, screen, aliens, alien_xnum, alien_ynum):
    new_alien = Alien(settings, screen)
    alien_width = new_alien.rect.width
    alien_height = new_alien.rect.height
    #Offset by 1 width from the edge and 2 widths per alien
    new_alien.rect.x = alien_width + (2*alien_width*alien_xnum)
    #Update the value used in the updater to the new x-rect attribute
    new_alien.alien_x = new_alien.rect.x
    #Offset by 1 from the top and 2 heights per alien
    new_alien.rect.y = alien_height + (2*alien_height*alien_ynum)
    
    #print(str(alien_xnum) + ' '+ str(alien_ynum) + ' ' + str(new_alien.rect.x) + ' ' + str(new_alien.rect.y))
    #Adds it to the group
    aliens.add(new_alien)

def create_alien_fleet(settings, screen, aliens, ship):
    """Creates a full alien fleet"""
    #Figure out the width of an alien
    trial_alien = Alien(settings, screen)
    alien_width = trial_alien.rect.width
    alien_height = trial_alien.rect.height

    #Figure out how many aliens in a row
    horizontal_space = settings.scr_display_width - 2*alien_width
    horizontal_aliens = int(horizontal_space / (2*alien_width))

    #Figure out how many alien rows total that leaves 2 heights at the bottom and 1 at top
    vertical_space = settings.scr_display_height - ship.rect.height -(3*alien_height)
    vertical_aliens = int(vertical_space / (2*alien_height))

    #Nested for loop to add each alien within a row, and the total rows too
    for alien_ynum in range (vertical_aliens):
        for alien_xnum in range(horizontal_aliens):
            create_alien(settings, screen, aliens, alien_xnum, alien_ynum)

        
def aliens_updater(aliens, settings, ship, screen, statistics, bullets, score):
    """Updates alien positions"""
    fleet_edge_checker(aliens, settings)
    #for alien in aliens:
     #   alien.rect.x += settings.a_speed_factor * settings.alien_direction
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_attack(settings, statistics, screen, ship, aliens, bullets, score)
    check_bottom(settings, screen, statistics, ship, aliens, bullets, score)

def fleet_edge_checker(aliens, settings):
    """Moves fleet if it hits edge"""
    for alien in aliens:
        if alien.edge_checker():
            fleet_change_direction(aliens, settings)
            break

def fleet_change_direction(aliens, settings):
    """Drops fleet and changes direction"""
    settings.alien_direction *= -1
    for alien in aliens:
        alien.rect.y += settings.a_drop_factor

def ship_attack(settings, statistics, screen, ship, aliens, bullets, score):
    """Responds to ship being hit by alien"""
    if statistics.ships_remaining >= 1: 
        #Remove a ship from ships left
        statistics.ships_remaining -= 1
        reset_game(statistics, aliens, bullets, settings, screen, ship)
        score.init_ship(statistics)
        sleep(0.5)
    else: 
        statistics.game_on = False
        pygame.mouse.set_visible(True)

def check_bottom(settings, screen, statistics, ship, aliens, bullets, score):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom > screen_rect.bottom:
            #Consider this an attack on ship
            ship_attack(settings, statistics, screen, ship, aliens, bullets, score)

def reset_game(statistics, aliens, bullets, settings, screen, ship):
    """Empties bullets/aliens, creates a new fleet, and centers ship"""
    aliens.empty()
    bullets.empty()
    create_alien_fleet(settings, screen, aliens, ship)
    ship.center()

def high_score_checker(statistics, score):
    if statistics.points > statistics.high_score:
        statistics.high_score = statistics.points
        score.init_high_score(statistics)
