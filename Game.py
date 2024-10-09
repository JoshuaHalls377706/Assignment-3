#Import libraries
import pygame
import random

#Initialize pygame
pygame.init()

#Window settings
screenwidth, screenheight = 1000, 700
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Game")

#Import pygame.locals to access key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_LSHIFT,
    KEYDOWN,
    KEYUP,
    QUIT,
)

#Load the background images
background1 = pygame.image.load('background1.png').convert()
background2 = pygame.image.load('background2.png').convert()
background3 = pygame.image.load('background3.png').convert()
background4 = pygame.image.load('background4.png').convert()

background6 = pygame.image.load('background6.png').convert()

#Scale backgrounds to fit window
background6 = pygame.transform.scale(background6, (screenwidth, screenheight))

#Maintain Aspect Ratio
#Background1
aspect_ratio1 = background1.get_width() / background1.get_height()
new_height1 = screenheight
new_width1 = int(new_height1 * aspect_ratio1)
background1 = pygame.transform.scale(background1, (new_width1, new_height1))
#Background2
aspect_ratio2 = background2.get_width() / background2.get_height()
new_height2 = screenheight
new_width2 = int(new_height2 * aspect_ratio2)
background2 = pygame.transform.scale(background2, (new_width2, new_height2))
#Background3
aspect_ratio3 = background3.get_width() / background3.get_height()
new_height3 = screenheight
new_width3 = int(new_height3 * aspect_ratio3)
background3 = pygame.transform.scale(background3, (new_width3, new_height3))
#Background4
aspect_ratio4 = background4.get_width() / background4.get_height()
new_height4 = screenheight
new_width4 = int(new_height4 * aspect_ratio4)
background4 = pygame.transform.scale(background4, (new_width4, new_height4))

#PLAYER CODE
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('player.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (60, 120))
        self.rect = self.surf.get_rect()
        self.velocity_y = 0
        self.gravity = 0.03
        self.jump_strength = -10
        self.health = 100  
        self.alive = True
        self.facing_right = True
        self.last_jump_time = 0
        self.jump_cooldown = 400

    def update(self, pressed_keys):
        current_time = pygame.time.get_ticks()
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.health <= 0:
            self.alive = False

        #Floor collision
        if self.rect.bottom > floor1:
            self.rect.bottom = floor1
            self.velocity_y = 0
                    
        #Movement controls
        if pressed_keys[K_UP] and (current_time - self.last_jump_time > self.jump_cooldown):
            self.velocity_y = self.jump_strength
            self.last_jump_time = current_time 
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if not moving_camera:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-1, 0)
                self.facing_right = False
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(1, 0)           
                self.facing_right = True
        elif camera_stopped:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-1, 0)
                self.facing_right = False
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(1, 0)           
                self.facing_right = True
        else:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-0, 0)
                self.facing_right = False
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(0, 0)           
                self.facing_right = True
            
        #Boundaries checks
        self.rect.clamp_ip(pygame.Rect(0, 0, screenwidth, screenheight))

#PLAYER HEALTH BAR
def draw_player_health_bar(surface, x, y, health):
    bar_width = 100
    bar_height = 10
    fill = (health / 100) * bar_width  # Calculate fill proportion
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, (255, 0, 0), outline_rect)  # Red outline
    pygame.draw.rect(surface, (0, 255, 0), fill_rect)  # Green fill

#PLAYER BULLET
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load('Bullet.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (20, 10))
        self.rect = self.surf.get_rect(center=pos)
        self.speed = 1

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > screenwidth  or self.rect.right < 0:
            self.kill()

#ENEMY1
class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('enemy1.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (60, 120))
        self.rect = self.surf.get_rect(topleft=position)
        self.health = 10  
        self.speed = 0.7  
        self.direction = 1
        self.last_shot_time = 0
        self.shoot_interval = 1000  

    def update(self, floor_y, current_time):
        self.rect.y += self.speed * self.direction

        if self.rect.top < floor_y - 600 or self.rect.bottom > floor_y:
            self.direction *= -1

        #Shoot bullet
        if current_time - self.last_shot_time > self.shoot_interval:
            self.shoot()
            self.last_shot_time = current_time

    def shoot(self):
        #Create an enemy bullet and add it to the bullet group
        enemy_bullet = EnemyBullet(self.rect.center)
        enemy_bullets.add(enemy_bullet)

    def take_damage(self, amount):
        self.health -= amount

#ENEMY1 HEALTH BAR
def draw_health_bar(surface, x, y, health):
    bar_width = 100
    bar_height = 10
    fill = (health / 100) * bar_width  #Calculate fill proportion
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, (255, 0, 0), outline_rect)  #Red outline
    pygame.draw.rect(surface, (0, 255, 0), fill_rect)  #Green fill

#ENEMY1 BULLET
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(EnemyBullet, self).__init__()
        self.surf = pygame.image.load('Enemy1bullet.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (20, 10))
        self.rect = self.surf.get_rect(center=pos)
        self.speed = 1

    def update(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.kill()

#ENEMY2
class Enemy2(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Enemy2, self).__init__()
        self.surf = pygame.image.load('enemy1.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (60, 120))
        self.rect = self.surf.get_rect(topleft=position)
        self.health = 10  
        self.last_shot_time = 0
        self.shoot_interval = 1000  

        #Shoot bullet
        if current_time - self.last_shot_time > self.shoot_interval:
            self.shoot()
            self.last_shot_time = current_time

    def shoot(self):
        #Create an enemy bullet and add it to the bullet group
        enemy_bullet = EnemyBullet(self.rect.center)
        enemy_bullets.add(enemy_bullet)

    def take_damage(self, amount):
        self.health -= amount

#ENEMY2 HEALTH BAR
def draw_health_bar(surface, x, y, health):
    bar_width = 100
    bar_height = 10
    fill = (health / 100) * bar_width  # Calculate fill proportion
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, (255, 0, 0), outline_rect)  # Red outline
    pygame.draw.rect(surface, (0, 255, 0), fill_rect)  # Green fill

#ENEMY2 BULLET
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(EnemyBullet, self).__init__()
        self.surf = pygame.image.load('Enemy1bullet.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (20, 10))
        self.rect = self.surf.get_rect(center=pos)
        self.speed = 1

    def update(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.kill()
            
#Rain
class Rain(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Rain, self).__init__()
        self.surf = pygame.image.load('rain.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (20, 10))
        self.rect = self.surf.get_rect(center=pos)
        self.speed = 1
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > floor1:
            self.kill()
            
#Classes
#Load images
class_image1 = pygame.image.load('class1.png').convert_alpha()
class_image1 = pygame.transform.scale(class_image1, (80, 80))
class_image2 = pygame.image.load('class2.png').convert_alpha()
class_image2 = pygame.transform.scale(class_image2, (80, 80))
class_image3 = pygame.image.load('class3.png').convert_alpha()
class_image3 = pygame.transform.scale(class_image3, (80, 80))
#Collision detection
class1_col = class_image1.get_rect(topleft=(200, 300))
class2_col = class_image2.get_rect(topleft=(400, 300))
class3_col = class_image3.get_rect(topleft=(600, 300))

#LVL2 Boxes
#Load images
lvl2box1 = pygame.image.load('lvl2box1.png').convert_alpha()
lvl2box1 = pygame.transform.scale(lvl2box1, (80, 150))
lvl2box2 = pygame.image.load('lvl2box1.png').convert_alpha()
lvl2box2 = pygame.transform.scale(lvl2box2, (80, 80))
lvl2box3 = pygame.image.load('lvl2box1.png').convert_alpha()
lvl2box3 = pygame.transform.scale(lvl2box3, (80, 150))
#Collision detection
lvl2box1_col = lvl2box1.get_rect(topleft=(3500, 477))
lvl2box2_col = lvl2box2.get_rect(topleft=(3700, 547))
lvl2box3_col = lvl2box3.get_rect(topleft=(3900, 477))
#LVL3 updated location
lvl2box1_background3 = (240, 477) 
lvl2box2_background3 = (440, 547)
lvl2box3_background3 = (640, 477)
#Combined Variable
lvl2_tall_boxes = [lvl2box1_col, lvl2box3_col]

#Create player
player = Player()

#Game state
current_background = background1
floor1 = screenheight - 74
camera_stopped = False
moving_camera = False
show_classes = True
background2_x = 0
camera_stop1 = screenwidth - new_width2
level2_start = False
enemy_delay = 1000 
level2_start_time = None 
enemy1 = None
background3_x = 0
level3_start = False
level3_start_time = None 
camera_stop2 = screenwidth - new_width3
enemy2 = None
background4_x = 0

#Sprite groups
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
rain = pygame.sprite.Group()

#GAME LOOP
running = True

while running:
    current_time = pygame.time.get_ticks()  

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LSHIFT:
                bullet = Bullet(player.rect.center)
                bullet.speed = 1 if player.facing_right else -1
                bullets.add(bullet)
        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    if current_background == background1:
        screen.blit(background1, (0, 0))  # Draw background1 for level 1
    elif current_background == background2:
        screen.blit(background2, (background2_x, 0))  # Draw background2
    elif current_background == background3:
        screen.blit(background3, (background3_x, 0))  # Draw background3
    elif current_background == background4:
        screen.blit(background4, (background4_x, 0))  # Draw background4
    elif current_background == background6:
        screen.blit(background6, (0, 0))  # Draw background1 for level 1

    #Camera Movement
    #Background2
    if current_background == background2:
        if pressed_keys[K_RIGHT] and moving_camera == True:
            background2_x -= 5  # Move background left
            camera_stopped = False
            if background2_x < screenwidth - new_width2:
                background2_x = screenwidth - new_width2
        if pressed_keys[K_LEFT] and moving_camera == True:
            background2_x += 5  # Move background right
            # Prevent moving beyond the left edge of the background
            if background2_x > 0:
                background2_x = 0
                camera_stopped = True
             
    #Camera Stop        
    if background2_x <= camera_stop1:
        moving_camera = False
        if level2_start_time is None: 
            level2_start_time = current_time
        if current_time - level2_start_time >= enemy_delay:
            level2_start = True
        
    #Background3
    if current_background == background3:
        if pressed_keys[K_RIGHT] and moving_camera == True:
            background3_x -= 5  # Move background left
            if background3_x < screenwidth - new_width3:
                background3_x = screenwidth - new_width3
        if pressed_keys[K_LEFT] and moving_camera == True:
            background3_x += 5  # Move background right
            # Prevent moving beyond the left edge of the background
            if background3_x > 0:
                background3_x = 0
    #Camera Stop        
    if background3_x <= camera_stop2:
        moving_camera = False
        if level3_start_time is None: 
            level3_start_time = current_time
        if current_time - level3_start_time >= enemy_delay:
            level3_start = True
                
#LEVEL1           
    #Check for collision with class images
    if show_classes and (player.rect.colliderect(class1_col) or 
                         player.rect.colliderect(class2_col) or 
                         player.rect.colliderect(class3_col)):
        current_background = background2  #Change background on collision
        show_classes = False  #Hide class images
        moving_camera = True
         
#LEVEL2
    #Update bullets
    bullets.update()
    enemy_bullets.update()  
    
    if level2_start:
        if player.alive:
            if enemy1 is None:
                enemy1 = Enemy((850, floor1 - 120))  #Enemy position
            enemy1.update(floor1, current_time) 
            
            #Check for collisions with bullets
            for bullet in bullets:
                if bullet.rect.colliderect(enemy1.rect):
                    enemy1.take_damage(10)  #Deal damage
                    bullet.kill()  #Remove bullet
            
            #Check for collisions with enemy bullets
            for enemy_bullet in enemy_bullets:
                if enemy_bullet.rect.colliderect(player.rect):
                    player.health -= 20  #Deal damage
                    enemy_bullet.kill()  #Remove bullet
                    #Player Dead
                    if player.health <= 0:
                        player.health = 0  #Ensure health doesn't go negative
                        player.alive = False
                        current_background = background6
    
            #Check if the enemy's health is zero or less for next LVL
            if enemy1 and enemy1.health <= 0:
                moving_camera = True
                background2_x = 0
                current_background = background3
                enemy1 = None
                level2_start = False
                player.health = 100 #Reset player health
                
            #Draw the health bar only if the enemy is still alive
            if enemy1:
                draw_health_bar(screen, 10, 10, enemy1.health)
                screen.blit(enemy1.surf, enemy1.rect)
#LEVEL3
    rain.update()
    
    if level3_start:
        if player.alive:
            if enemy2 is None:
                enemy2 = Enemy2((850, floor1 - 120))  #Enemy position
            enemy2.update(floor1, current_time) 
            screen.blit(enemy2.surf, enemy2.rect)
                
            #Check for collisions with bullets
            for bullet in bullets:
                if bullet.rect.colliderect(enemy2.rect):
                    enemy2.take_damage(10)  #Deal damage
                    bullet.kill()  #Remove bullet
                
                        #Check for collisions with bullets
            for bullet in bullets:
                if bullet.rect.colliderect(enemy2.rect):
                    enemy2.take_damage(10)  #Deal damage
                    bullet.kill()  #Remove bullet

            # Check for collisions with enemy bullets
            for enemy_bullet in enemy_bullets:
                if enemy_bullet.rect.colliderect(player.rect):
                    player.health -= 20  #Deal damage
                    enemy_bullet.kill()  #Remove bullet
                    # Player Dead
                    if player.health <= 0:
                        player.health = 0  #Ensure health doesn't go negative
                        current_background = background6  #Change background to background 6
                        
                        #Check if the enemy's health is zero or less for next LVL
            if enemy2 and enemy2.health <= 0:
                moving_camera = True
                background3_x = 0
                current_background = background4
                enemy2 = None
                level3_start = False
                player.health = 100 #Reset player health
            
            if enemy2:
                draw_health_bar(screen, 10, 10, enemy2.health)
                screen.blit(enemy2.surf, enemy2.rect)
                
            max_raindrops = 5
            if len(rain) < max_raindrops:    
                if random.randint(0, 100) <1:  # Adjust the chance of rain
                    raindrop = Rain((random.randint(0, screenwidth), 0))
                    rain.add(raindrop)
                
            for raindrop in rain:
                if raindrop.rect.colliderect(player.rect):
                    player.health -= 5  # Deal damage to the player
                    raindrop.kill()  # Remove the raindrop after collision
                    if player.health <= 0:
                        player.alive = False
                        player.health = 0  #Ensure health doesn't go negative
                        current_background = background6  #Change background to background 6
                
            for raindrop in rain:
                screen.blit(raindrop.surf, raindrop.rect)
            
#LEVEL4

#COMPLETION
#PAUSE
#FAIL



    #Update bullets
    bullets.update()
    enemy_bullets.update()
    
    #Drawing
    #Lvl2 boxes
    if current_background == background2:
        screen.blit(lvl2box1, (lvl2box1_col.x + background2_x, lvl2box1_col.y)) 
        screen.blit(lvl2box2, (lvl2box2_col.x + background2_x, lvl2box2_col.y))
        screen.blit(lvl2box3, (lvl2box3_col.x + background2_x, lvl2box3_col.y))
    elif current_background == background3:
        screen.blit(lvl2box1, (lvl2box1_background3[0] + background3_x, lvl2box1_background3[1])) 
        screen.blit(lvl2box2, (lvl2box2_background3[0] + background3_x, lvl2box2_background3[1]))
        screen.blit(lvl2box3, (lvl2box3_background3[0] + background3_x, lvl2box3_background3[1]))
    
    #Player if alive
    if player.alive:
        screen.blit(player.surf, player.rect)

    #Player's health bar
    draw_player_health_bar(screen, 10, screenheight - 30, player.health)

    #Draw Classes
    if show_classes:
        screen.blit(class_image1, class1_col.topleft)
        screen.blit(class_image2, class2_col.topleft)
        screen.blit(class_image3, class3_col.topleft)
        
    #Player bullets
    for bullet in bullets:
        screen.blit(bullet.surf, bullet.rect)
        
    # Draw enemy bullets
    for enemy_bullet in enemy_bullets:
        screen.blit(enemy_bullet.surf, enemy_bullet.rect)

    pygame.display.flip()

pygame.quit()