#Import libraries
import pygame

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
background = pygame.transform.scale(background1, (screenwidth, screenheight))

#Maintain Aspect Ratio
#Background2
aspect_ratio = background2.get_width() / background2.get_height()
new_height = screenheight
new_width = int(new_height * aspect_ratio)
background2 = pygame.transform.scale(background2, (new_width, new_height))
#Background3
aspect_ratio1 = background3.get_width() / background3.get_height()
new_height1 = screenheight
new_width1 = int(new_height1 * aspect_ratio1)
background3 = pygame.transform.scale(background3, (new_width1, new_height1))
#Background4
aspect_ratio2 = background4.get_width() / background4.get_height()
new_height2 = screenheight
new_width2 = int(new_height2 * aspect_ratio2)
background4 = pygame.transform.scale(background4, (new_width2, new_height2))

#Floor position
floor_y = screenheight - 74

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

    def update(self, pressed_keys, lvl2_boxes):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        if self.health <= 0:
            self.alive = False

        #LVL2 box collision if visible
        if lvl2boxes_visible:
            for box in lvl2_boxes:
                if self.rect.colliderect(box) and self.velocity_y > 0:
                    self.rect.bottom = box.top
                    self.velocity_y = 0
                    break

        #Floor collision
        if self.rect.bottom > floor_y:
            self.rect.bottom = floor_y
            self.velocity_y = 0

        #Movement controls
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -4)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)

        #Boundaries checks
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenwidth:
            self.rect.right = screenwidth
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screenheight:
            self.rect.bottom = screenheight
        if self.rect.bottom > floor_y:
            self.rect.bottom = floor_y

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
        if self.rect.left > screenwidth:  
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

#Create player
player = Player()

#Load class images
class_image1 = pygame.image.load('class1.png').convert_alpha()
class_image1 = pygame.transform.scale(class_image1, (80, 80))
class_image2 = pygame.image.load('class2.png').convert_alpha()
class_image2 = pygame.transform.scale(class_image2, (80, 80))
class_image3 = pygame.image.load('class3.png').convert_alpha()
class_image3 = pygame.transform.scale(class_image3, (80, 80))

#Load Lvl2 box images
lvl2box1 = pygame.image.load('lvl2box1.png').convert_alpha()
lvl2box1 = pygame.transform.scale(lvl2box1, (80, 150))
lvl2box2 = pygame.image.load('lvl2box1.png').convert_alpha()
lvl2box2 = pygame.transform.scale(lvl2box2, (80, 80))
lvl2box3 = pygame.image.load('lvl2box1.png').convert_alpha()
lvl2box3 = pygame.transform.scale(lvl2box3, (80, 150))

#Collision detection
#Classes
class1_col = class_image1.get_rect(topleft=(200, 300))
class2_col = class_image2.get_rect(topleft=(400, 300))
class3_col = class_image3.get_rect(topleft=(600, 300))
#Lvl2 boxes
lvl2box1_col = lvl2box1.get_rect(topleft=(270, 477))
lvl2box2_col = lvl2box2.get_rect(topleft=(420, 547))
lvl2box3_col = lvl2box3.get_rect(topleft=(570, 477))

#Boxes variable
lvl2_boxes = [lvl2box1_col, lvl2box2_col, lvl2box3_col]

#Game state
current_background = background
show_classes = True
enemy1 = None
enemy2 = None
lvl2boxes_visible = False

#Initial positions for backgrounds
background2_x = 0
background3_x = 0

#Lvl 2 and 3 camera stops
camera_stop_x_2 = -1785  
camera_stop_x_3 = -1785  

#Sprite groups
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

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
                bullets.add(bullet)
        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, lvl2_boxes)
    
#LEVEL1
    #Check for collision with class images
    if show_classes and (player.rect.colliderect(class1_col) or 
                         player.rect.colliderect(class2_col) or 
                         player.rect.colliderect(class3_col)):
        current_background = background2  #Change background on collision
        show_classes = False  #Hide class images

#LEVEL2
    #Side-scrolling mechanics for background2
    if current_background == background2:
        if background2_x > camera_stop_x_2:  #Check to stop scrolling
            if pressed_keys[K_RIGHT]:
                background2_x -= 3.5  #Move background left
            if pressed_keys[K_LEFT]:
                background2_x += 3.5  #Move background right

            #Prevent moving past the edges of the background2 image
            if background2_x > 0:
                background2_x = 0
            if background2_x < screenwidth - new_width:
                background2_x = screenwidth - new_width

        #Prevent player from moving off screen in level 2
        player.rect.clamp_ip(screen.get_rect())

    #Side-scrolling mechanics for background3
    if current_background == background3:
        if background3_x > camera_stop_x_3:  #Check to stop scrolling
            if pressed_keys[K_RIGHT]:
                background3_x -= 3.5  #Move background left
            if pressed_keys[K_LEFT]:
                background3_x += 3.5  #Move background right

            #Prevent moving past the edges of the background3 image
            if background3_x > 0:
                background3_x = 0
            if background3_x < screenwidth - new_width1:  
                background3_x = screenwidth - new_width1

        #Prevent player from moving off screen in level 3
        player.rect.clamp_ip(screen.get_rect())

    #Update bullets
    bullets.update()
    enemy_bullets.update()

    #Draw Assets
    screen.blit(current_background, (0, 0))

    if current_background == background2:
        screen.blit(background2, (background2_x, 0))

        #Check if the camera has stopped, then draw the lvl2 boxes
        if background2_x <= camera_stop_x_2:
            lvl2boxes_visible = True  #Enable boxes collision
            screen.blit(lvl2box1, lvl2box1_col.topleft)
            screen.blit(lvl2box2, lvl2box2_col.topleft)
            screen.blit(lvl2box3, lvl2box3_col.topleft)

            if enemy1 is None:
                enemy1 = Enemy((850, floor_y - 120))  #Enemy position

            #Update enemy position if boxes are visible
            if lvl2boxes_visible:
                enemy1.update(floor_y, current_time) 

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
                        current_background = background6  #Change background to background 6
                        lvl2boxes_visible = False

            #Check if the enemy's health is zero or less for next LVL
            if enemy1 and enemy1.health <= 0:
                current_background = background3  #Change background to background 3
                enemy1 = None  #Remove the enemy from the game
                lvl2boxes_visible = False #Hide LVL2 boxes
                player.health = 100 #Reset player health

            #Draw the health bar only if the enemy is still alive
            if enemy1:
                draw_health_bar(screen, 10, 10, enemy1.health)
                screen.blit(enemy1.surf, enemy1.rect)

    if current_background == background3:
        screen.blit(background3, (background3_x, 0))

#Level 3
        #Check if the camera has stopped
        if background3_x <= camera_stop_x_3:
            screen.blit(background3, (background3_x, 0))
            
            if enemy2 is None:
                enemy2 = Enemy2((850, floor_y - 120))  #Enemy position
                
            if enemy2:
                enemy2.update(floor_y, current_time)
                # Draw enemy
                screen.blit(enemy2.surf, enemy2.rect)

            #Draw the health bar only if the enemy is still alive
            if enemy2:
                draw_health_bar(screen, 10, 10, enemy2.health)
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
                current_background = background4  #Change background to background 4
                enemy2 = None  #Remove the enemy from the game
                player.health = 100
                
#LEVEL 4



#COMPLETION SCREEN

    # Draw player if alive
    if player.alive:
        screen.blit(player.surf, player.rect)

    # Draw player's health bar
    draw_player_health_bar(screen, 10, screenheight - 30, player.health)

    if show_classes:
        screen.blit(class_image1, class1_col.topleft)
        screen.blit(class_image2, class2_col.topleft)
        screen.blit(class_image3, class3_col.topleft)

    # Draw bullets
    for bullet in bullets:
        screen.blit(bullet.surf, bullet.rect)

    # Draw enemy bullets
    for enemy_bullet in enemy_bullets:
        screen.blit(enemy_bullet.surf, enemy_bullet.rect)

    pygame.display.flip()

pygame.quit()