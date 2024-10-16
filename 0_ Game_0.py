import pygame
import math
import random

import os

from Crate import Crate, SolidCrate, check_player_crate_collision # Import the Crate classes

#--------------------------------------------------------------------------
# FILE MANAGEMENT
#--------------------------------------------------------------------------
# Set the working directory to the folder where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

#--------------------------------------------------------------------------

# -- Global Variables --
GL = 600  # Ground level
MAP_WIDTH = 1200
MAP_HEIGHT = 800
GRAVITY = 0.5
Class_picked = False
Boss_1_done = False
Boss_2_done = False
Boss_3_done = False

# -- Classes --

class Projectile:
    def __init__(self, sprite, bullet_speed, range, damage):
        self.sprite_carry = sprite
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.bullet_speed = bullet_speed
        self.range = range
        self.damage = damage
        self.position = (0, 0)
        self.direction = (0, 0)
        self.distance_travelled = 0
        self.active = True

    def move(self):
        if self.distance_travelled < self.range:
            self.position = (
                self.position[0] + self.direction[0] * self.bullet_speed,
                self.position[1] + self.direction[1] * self.bullet_speed,
            )
            self.distance_travelled += self.bullet_speed
        else:
            self.active = False

    def draw(self, surface):
        angle = math.degrees(math.atan2(-self.direction[1], self.direction[0]))
        rotated_sprite = pygame.transform.rotate(self.sprite, angle)
        rect = rotated_sprite.get_rect(center=self.position)
        surface.blit(rotated_sprite, rect.topleft)

class Weapon:
    def __init__(self, name, sprite, projectile, mag_size, reload_time, attackspeed, spread=0, use_mag=True):
        self.name = name
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.projectile = projectile
        self.mag_size = mag_size
        self.ammo = mag_size
        self.attackspeed = attackspeed
        self.reload_time = reload_time
        self.use_mag = use_mag
        self.last_shot_time = 0
        self.reloading = False
        self.reload_start_time = 0
        self.spread = spread
        self.position_x = 0
        self.position_y = 0

    def aim(self, cursor_pos):
        dx = cursor_pos[0] - self.position_x
        dy = cursor_pos[1] - self.position_y
        distance = math.hypot(dx, dy)

        if distance != 0:
            self.projectile.direction = (dx / distance, dy / distance)
        else:
            self.projectile.direction = (0, 0)

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_shot_time >= self.attackspeed * 1000 and
                self.ammo > 0 and not self.reloading):
            self.last_shot_time = current_time
            if self.use_mag:
                self.ammo -= 1

            # Create a new projectile
            new_projectile = Projectile(
                self.projectile.sprite_carry,
                self.projectile.bullet_speed,
                self.projectile.range,
                self.projectile.damage
            )

            # Set projectile's position
            new_projectile.position = [self.position_x, self.position_y]

            # Apply spread
            angle_variation = random.uniform(-self.spread, self.spread) * (math.pi / 180)  # Convert degrees to radians
            angle = math.atan2(self.projectile.direction[1], self.projectile.direction[0]) + angle_variation
            new_projectile.direction = (math.cos(angle), math.sin(angle))

            return new_projectile
        elif self.ammo <= 0 and not self.reloading:
            self.reload()
        
        return None

    def reload(self):
        current_time = pygame.time.get_ticks()
        if self.ammo < self.mag_size and not self.reloading:
            self.reloading = True
            self.reload_start_time = current_time

    def update_reload(self):
        if self.reloading:
            if pygame.time.get_ticks() - self.reload_start_time >= self.reload_time * 1000:
                self.ammo = self.mag_size
                self.reloading = False

    def draw(self, surface, mouse_pos):
        dx = mouse_pos[0] - self.position_x
        dy = mouse_pos[1] - self.position_y
        distance = math.hypot(dx, dy)
        angle = math.degrees(math.atan2(-dy, dx)) if distance != 0 else 0
        
        rotated_sprite = self.sprite
        if dx < 0:
            rotated_sprite = pygame.transform.flip(rotated_sprite, False, True)
        
        rotated_sprite = pygame.transform.rotate(rotated_sprite, angle)
        rect = rotated_sprite.get_rect(center=(self.position_x, self.position_y))
        surface.blit(rotated_sprite, rect.center)

class Player:
    def __init__(self, name, health, lives, speed, weapon, sprite, effect):
        self.name = name
        self.maxhealth = health
        self.health = health
        self.lives = lives
        self.speed = speed
        self.speed_boost = 1
        self.weapon = weapon

        # Load animated sprites for player
        self.sprites = [
            pygame.image.load('LG_walk_side0.png'),
            pygame.image.load('LG_walk_side1.png'),
            pygame.image.load('LG_walk_side2.png')
        ]
        # Pre-flip sprites for left-facing direction
        self.flipped_sprites = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites]

        self.idle_sprite = pygame.image.load('LG_walk_side2.png')
        self.flipped_idle_sprite = pygame.transform.flip(self.idle_sprite, True, False)

        # Set initial sprite and position
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(100, GL)  # Set initial position
        self.velocity_y = 0
        self.is_jumping = False
        self.facing_right = True
        self.sprite_speed = speed
        self.original_ground_level = GL  # Store the original ground level
        self.ground_level = self.original_ground_level  # Set the current ground level

        # Gravity settings
        self.gravity = 1
        self.jump_speed = -25  # Jump height

        # Special Effect - Don't change here
        self.effect = effect
        self.effect_cooldown = 1
        self.last_effect_active = 0
        self.effect_active = False

    def move(self, direction):
        # Handle horizontal movement and sprite animation
        moving = False
        if direction.x != 0:
            self.position.x += direction.x * self.sprite_speed * self.speed_boost
            moving = True
            if direction.x > 0:  # Moving right
                if not self.facing_right:
                    self.facing_right = True
                    self.current_sprite = 0  # Reset sprite animation
                self.image = self.sprites[int(self.current_sprite)]
            else:  # Moving left
                if self.facing_right:
                    self.facing_right = False
                    self.current_sprite = 0  # Reset sprite animation
                self.image = self.flipped_sprites[int(self.current_sprite)]

        self.rect.topleft = (self.position.x - self.image.get_width() / 2, self.position.y - self.image.get_height())

        # Animate the player when moving
        if moving:
            self.current_sprite += 0.1
            player_sound.play()
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
        else:
            # Set idle sprite based on facing direction
            if self.facing_right:
                self.image = self.idle_sprite
            else:
                self.image = self.flipped_idle_sprite

    def jump(self):
        # Handle jumping logic
        if not self.is_jumping:
            self.is_jumping = False
            self.velocity_y = self.jump_speed

    def apply_gravity(self):
        self.velocity_y += self.gravity
        new_position_y = self.position.y + self.velocity_y

        # Combine platforms and crates for collision checking
        all_platforms = platforms + crates

        on_platform = False  # Track if the player is standing on a platform

        keys = pygame.key.get_pressed()

        # Check for collision with platforms
        if not keys[pygame.K_s]:
            for platform in all_platforms:
                if (self.position.x + (self.image.get_width() / 2) > platform.rect.left and
                    self.position.x - (self.image.get_width() / 2) < platform.rect.right):
                    
                    # Check if coming from above
                    if new_position_y >= platform.rect.top and self.position.y <= platform.rect.top:
                        self.position.y = platform.rect.top  # Sit on top of the platform
                        self.velocity_y = 0  # Reset vertical velocity
                        self.is_jumping = False
                        return  # Exit early as we've handled the collision

                    # Check if coming from below
                    elif new_position_y <= platform.rect.bottom and self.position.y >= platform.rect.bottom:
                        self.position.y = platform.rect.top  # Sit on top of the platform
                        self.is_jumping = False  # <-- Add this here to allow jumping again
                        return  # Exit early as we've handled the collision
                    
        # If no collision was detected, update the position
        self.position.y = new_position_y

        # Reset position if player falls below ground level
        if self.position.y >= GL:
            self.position.y = GL
            self.velocity_y = 0  # Reset vertical velocity
            self.on_ground = True  # Player is grounded

    def draw(self, surface, camera_x):
        # Draw the player sprite on the screen relative to the camera
        draw_x = self.position.x - (self.image.get_width() / 2) - camera_x
        draw_y = self.position.y - self.image.get_height()
        surface.blit(self.image, (draw_x, draw_y))

        # Draw weapon
        self.weapon.position_x = self.position.x-20 - camera_x
        self.weapon.position_y = self.position.y-40 - self.image.get_height() / 2
        self.weapon.draw(surface, pygame.mouse.get_pos())

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.lives -= 1
            self.respawn()

    def respawn(self):
        if    your_dead():
            self.health = self.maxhealth
            self.position = pygame.Vector2(100, 300)
            self.is_jumping = False
            theme_song.play(loops=-1) 

    def draw_Stats(self, surface):
        # Drawing player stats (same as original)
        my_font = pygame.font.SysFont('Comic Sans MS', 40)
        x = 50
        y = 20
        y_spacer = 30

        # Remaining Lives
        text_Lives = my_font.render(f'{self.lives}x', True, (0, 150, 255))
        surface.blit(text_Lives, (995, 720))

        # Health Bar
        health_bar_length = 160
        health_ratio = self.health / self.maxhealth
        pygame.draw.rect(surface, (255, 0, 0), (60, 58, health_bar_length, 20))  # Background
        pygame.draw.rect(surface, (255, 255, 0), (60, 58, health_bar_length * health_ratio, 20))  # Health

        # Ammo Bar
        if self.weapon:
            AmmoMax = self.weapon.mag_size
            AmmoCurrent = self.weapon.ammo

            # Render the text
            if not self.weapon.reloading:
                text_Ammo = my_font.render(f'{AmmoCurrent}/{AmmoMax}', True, (255, 255, 0))
            else:
                text_Ammo = my_font.render('Reloading...', True, (0, 150, 255))

            # Draw text on surface at the specified coordinates
            surface.blit(text_Ammo, (980, 50))

    def Player_effect(self, player):
        self.effect(player)

class Platform:
    def __init__(self, x, y, width, height, image_path =None, type = "Platform", colour = (139, 69, 19)):
        self.rect = pygame.Rect(x, y, width, 1)
        self.type = type
        self.height = height
        self.colour = colour
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))  # Stretch image to fit platform dimensions
        else:
            self.image = None

    def draw(self, surface, camera_x):
        # Adjust the rectangle's position based on the camera
        adjusted_rect = self.rect.move(-camera_x, 0)
        
        if self.image:
            # Blit the image if it exists
            surface.blit(self.image, adjusted_rect)
        else:
            # Fallback to color drawing if no image is provided
            pygame.draw.rect(surface, self.colour, adjusted_rect)

class Effect_box:
    def __init__(self, x, y, Size, color, effect, used=False):
        self.rect = pygame.Rect(x, y, Size, Size)
        self.effect = effect  # Function to apply the effect on the player
        self.used = used
        self.color = color

    def draw(self, surface, camera_x):
        if not self.used:
            adjusted_rect = self.rect.move(-camera_x, 0)
            pygame.draw.rect(surface, self.color, adjusted_rect)  # Gold color for the box

    def interact(self, player):
        if not self.used:
            player_rect = player.image.get_rect(topleft=(player.position.x - player.image.get_width()/2, player.position.y - player.image.get_height() + 1))
            # Check if the player rectangle collides with the effect box
            if self.rect.colliderect(player_rect):
                self.effect(player)  # Apply the effect when interacted with
                self.used = True  # Indicate that it was interacted with

class Effect_space:
    def __init__(self, x, y, width, size, image_path, effect, used=False, overlap_x=0, overlap_y=0, plane='x'):
        self.rect = pygame.Rect(x, y, width, size)
        self.effect = effect  # Function to apply the effect on the player
        self.image = pygame.image.load(image_path).convert_alpha() if image_path else None  # Load the image
        self.used = used  # Track if the effect has been used
        self.overlap_x = overlap_x  # Overlap amount for the x-plane
        self.overlap_y = overlap_y  # Overlap amount for the y-plane
        self.plane = plane  # Determine if tiling occurs in the x-plane or y-plane

        if self.plane == 'y' and self.image:
            # Rotate the image by 90 degrees for the y-plane
            self.image = pygame.transform.rotate(self.image, 90)

    def draw(self, surface, camera_x):
        adjusted_rect = self.rect.move(-camera_x, 0)

        if self.image:
            if self.plane == 'x':
                # Tile the image with horizontal overlap (x-plane)
                for i in range(0, adjusted_rect.width, self.image.get_width() - self.overlap_x):
                    for j in range(0, adjusted_rect.height, self.image.get_height()):
                        surface.blit(self.image, (adjusted_rect.x + i, adjusted_rect.y + j))
            elif self.plane == 'y':
                # Tile the image with vertical overlap (y-plane) and rotated image
                for i in range(0, adjusted_rect.width, self.image.get_width()):
                    for j in range(0, adjusted_rect.height, self.image.get_height() - self.overlap_y):
                        surface.blit(self.image, (adjusted_rect.x + i, adjusted_rect.y + j))
        else:
            # Draw a solid color rectangle if no image
            pygame.draw.rect(surface, (255, 255, 255), adjusted_rect)

    def interact(self, player):
        player_rect = player.image.get_rect(topleft=(player.position.x, player.position.y - player.image.get_height() + 1))
        if self.rect.colliderect(player_rect):
            self.effect(player)

class Enemy:
    def __init__(self, health, damage, shoot_range, projectile, position, sprite):
        self.max_health = health
        self.health = health
        self.position = pygame.Vector2(position)
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (60, 120))

        self.last_shot_time = 0
        self.attack_speed = 10  # time in seconds between shots
        self.damage = damage
        self.shoot_range = shoot_range
        self.spread_angle = 50  # Example spread angle in degrees
        self.projectile = projectile        

        self.alive = True  # Track if the enemy is alive

    def update(self, player_position):
        if not self.alive:
            return []  # Return an empty list if the enemy is dead

        distance_to_player = self.position.distance_to(player_position)

        if distance_to_player <= self.shoot_range:
            current_time = pygame.time.get_ticks()  # Convert milliseconds to seconds
            if current_time - self.last_shot_time > self.attack_speed * 1000:
                projectiles = self.shoot(player_position)
                self.last_shot_time = current_time
                return projectiles  # Return newly created projectiles

        return []  # Return an empty list if no projectiles were shot

    def shoot(self, player_position, camera_x):
        projectile_direction = (player_position - self.position)
        num_projectiles = 3  # Number of projectiles to shoot
        spread_amount = self.spread_angle / (num_projectiles - 1)

        for i in range(num_projectiles):
            angle_offset = -self.spread_angle / 2 + i * spread_amount
            angle_variation = random.uniform(-self.spread_angle / 2, self.spread_angle / 2) * (math.pi / 180)  # Convert degrees to radians

            new_projectile = Projectile(
                self.projectile.sprite_carry,
                self.projectile.bullet_speed,
                self.projectile.range,
                self.projectile.damage
            )
            new_projectile.position = (self.position.x - camera_x, self.position.y - self.sprite.get_height()/2)
            angle = math.atan2(projectile_direction.y, projectile_direction.x) + angle_variation
            new_projectile.direction = (math.cos(angle), math.sin(angle))

            projectiles.append(new_projectile)  # Add projectile to the list

        return new_projectile  # Return the list of new projectiles

    def draw(self, surface, camera_x):
        if self.alive:
            draw_x = self.position.x - (self.sprite.get_width() / 2) - camera_x
            draw_y = self.position.y - self.sprite.get_height()

            surface.blit(self.sprite, (draw_x, draw_y))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.alive = False  # Mark the enemy as dead

    def get_health_percentage(self):
        return self.health / self.max_health  # Returns a value between 0 and 1

class Enemy_bird(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, damage):
        super().__init__()
        self.frames = [
            pygame.image.load('bird_0.png').convert_alpha(),
            pygame.image.load('bird_1.png').convert_alpha()
        ]
        self.frames = [pygame.transform.scale(frame, (width, height)) for frame in self.frames]
        self.current_frame = 0
        self.animation_counter = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.damage = damage
        self.health = 100  # Health of the enemy
        self.start_x = x
        self.start_y = y
        self.movement_speed = 2
        self.movement_counter = 0
        self.falling = False
        self.fall_distance = 0

    def update(self, player_position):
        if self.health > 0:
            # Animate the bird
            self.animation_counter += 1
            if self.animation_counter >= 10:  # Change frame every 10 updates
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                self.animation_counter = 0

            # Move towards the player if close enough, otherwise follow W shape
            self.movement_counter += 1
            distance_to_player = self.rect.centerx - player_position.x

            # If player is close, move towards the player, else follow W path
            if abs(distance_to_player) < 10:  # Change 300 to adjust detection range
                if distance_to_player > 0:
                    self.rect.x -= self.movement_speed  # Move left
                else:
                    self.rect.x += self.movement_speed  # Move right
            else:
                self.rect.x = self.start_x + math.sin(self.movement_counter * 0.05) * 100
                self.rect.y = self.start_y + math.sin(self.movement_counter * 0.1) * 50

        elif self.falling:
            # Make the bird fall when dead
            self.rect.y += 5
            self.fall_distance += 5
            if self.fall_distance >= 300:
                self.kill()

    def draw(self, surface, camera_x):
        # Draw the enemy bird sprite on the screen relative to the camera
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y
        surface.blit(self.image, (draw_x, draw_y))

    def deal_damage(self, player):
        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.image = pygame.image.load('bird_dead.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            self.falling = True
            self.alive = False  # Mark the enemy as dead

class CandyRollEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, damage, score, points=10):
        super().__init__()
        self.images = [
            pygame.image.load("Croll_0.png").convert_alpha(),
            pygame.image.load("Croll_1.png").convert_alpha(),
            pygame.image.load("Croll_2.png").convert_alpha()
        ]
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = speed
        self.y_level = y
        self.direction = 1
        self.animation_timer = 0
        self.animation_speed = 20
        self.damage = damage  # Store the damage this enemy deals
        self.alive = True
        self.score = score
        self.points = points

    def take_damage(self, amount):
        # Die immediately on any damage
        self.image = pygame.image.load('Croll_dead.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.alive = False  # Mark the enemy as dead
        self.score.increment(self.points)

    def deal_damage(self, player):
        # Inflict damage to the player when the enemy collides with them
        if self.rect.colliderect(player.rect):  # Check for collision before dealing damage
            player.take_damage(self.damage)

    def update(self, dt, platforms, crates, player):
        # Animate the rolling ball
        self.animate(dt)
        
        # Move the rolling ball left and right
        self.rect.x += self.speed * self.direction
        
        # Check collision with platforms and crates
        if pygame.sprite.spritecollide(self, platforms, False) or pygame.sprite.spritecollide(self, crates, False):
            self.direction *= -1  # Reverse direction if hit platform or crate
            self.rect.x += self.speed * self.direction
        
        # Ensure the ball stays at the set y level
        self.rect.y = self.y_level

        # Only check collision with the player and deal damage if they collide
        if self.rect.colliderect(player.rect):
            self.deal_damage(player)

    def animate(self, dt):
        # Update the animation timer
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            # Move to the next frame
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

    def draw(self, surface, camera_x):
        # Adjust the position relative to the camera
        adjusted_rect = self.rect.move(-camera_x, 0)
        surface.blit(self.image, adjusted_rect)

class Collectable:
    def __init__(self, x, y, width, height, sprite, value=1, is_life=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.value = value #adds points
        self.is_life = is_life  # Indicates if the collectable grants a life
        self.collected = False

    def draw(self, surface, camera_x):
        if not self.collected:
            adjusted_rect = self.rect.move(-camera_x, 0)
            surface.blit(self.sprite, adjusted_rect)

    def interact(self, player, score):
        player_rect = player.image.get_rect(topleft=(player.position.x - player.image.get_width() / 2, player.position.y - player.image.get_height() + 1))
        if self.rect.colliderect(player_rect) and not self.collected:
            self.collected = True
            if self.is_life:
                player.lives += 1  # Increase player's lives
                life_sound.play()
            else:
                score.increment(self.value)  # Increase score for regular collectable
                lempoints_sound.play()

class Score:
    def __init__(self):
        self.value = 0  # Initial score

    def increment(self, points):
        self.value += points

    def draw(self, surface):
        my_font = pygame.font.SysFont('Comic Sans MS', 40)
        score_text = my_font.render(f'{self.value}', True, (0,150,255))
        surface.blit(score_text, (130, 720))

class GameManager:
    def __init__(self):
        self.levels = {
            1: self.level_1,
            2: self.level_2,
            3: self.level_3
            # Add additional levels here
        }
        self.current_level = 1
        self.level_loaded = False

    def load_level(self):
        if not self.level_loaded:
            if self.current_level in self.levels:
                self.levels[self.current_level]()
                self.level_loaded = True
            else:
                print("No such level exists.")

    def reset_level(self):
        self.level_loaded = False

    def next_level(self):
        if self.current_level + 1 in self.levels:
            self.current_level += 1
            self.reset_level()  # Reset to allow loading the next level
            self.load_level()

    def progress_manager(self):
        # Check if the player has met the criteria to progress to the next level
        if self.player_completed_level():  # Placeholder for your completion condition
            self.next_level()

    def player_completed_level(self):
        if not player.health <= 0:
            if self.current_level == 1:
                return self.check_level_1_conditions()
            elif self.current_level == 2:
                return self.check_level_2_conditions()
            elif self.current_level == 3:
                return self.check_level_3_conditions()
            return False  # Default to not completed
        else:
            return self.Gameover()

#--------------------------------------------------------------------------------------------------LEVEL 1---BEGINNING

    def level_1(self):
        global projectiles, platforms, Effect_boxes, MAP_WIDTH, MAP_HEIGHT, enemies, collectables, crates, score
        MAP_WIDTH = 1200
        MAP_HEIGHT = 800
        projectiles = []
        platforms = []      
        Effect_boxes = [
            Effect_box(300, GL - 100, 50, (255, 0, 0), class_change_Assasin),  ## can we change these to different weapon choices or do you want the character to change? Slingshot
            Effect_box(600, GL - 100, 50, (0, 255, 0), class_change_Tank),     ## can we change these to different weapon choices? Pistol
            Effect_box(900, GL - 100, 50, (0, 0, 255), class_change_Soldier)   # can we change these to different weapon choices? Juice Gun
        ]
        enemies = []
        crates = [
            Crate(250, GL -120, crate_break_sound,score),
            Crate(550, GL -120, crate_break_sound,score),
            Crate(850, GL -120, crate_break_sound,score),
        ]
        collectables = [
            Collectable(270, 380, 40, 40, "Lempoints.png", 20),
            Collectable(820, 380, 40, 40, "Lempoints.png", 20),
            Collectable(1060, 410, 40, 40, "Lempoints.png", 20),
        ]     
        score.increment(0)

        print("Level 1 loaded.")

    def check_level_1_conditions(self):
        # Implement specific conditions for level 1
        global Class_picked
        if Class_picked:
            player.position = pygame.Vector2(100, GL)
            return True
#--------------------------------------------------------------------------------------------------LEVEL 2---BEGINNING
    def level_2(self):
        global projectiles, platforms, Effect_boxes, MAP_WIDTH, MAP_HEIGHT, enemies, collectables, crates, score
        MAP_WIDTH = 5000
        MAP_HEIGHT = 800
        projectiles = []
        platforms = [
            #Platform(200, GL - 100, 100, 20,"PF_0.png"),
            #Platform(400, GL - 100, 100, 20,"PF_0.png"),
            #Platform(600, GL - 200, 200, 20,"PF_0.png"),
            #Platform(1200, GL - 100, 500, 20,"PF_0.png"),
            #Platform(1000, GL - 250, 500, 20,"PF_0.png"),
            #Platform(3800, GL - 150, 300, 20,"PF_0.png")
        ]
        Effect_boxes = [
            #Effect_space(500, GL-40, 500, 110, "SP_0.png", Damage_player, overlap_x=10, plane='x'),
            #Effect_space(2000, GL - 200, 50, 150, "SP_0.png", Damage_player, overlap_y=10, plane='y'),
            #Effect_space(2000, GL - 850, 20, 300, "SP_0.png", Damage_player, overlap_y=10, plane='y'),
            #Effect_space(2700, GL, 500, 100, "SP_0.png", Damage_player, overlap_x=10, plane='x'),
            #Effect_space(3600, GL, 700, 110, "SP_0.png", Damage_player, overlap_x=10, plane='x')
        ]
        crates = [
            #Crate(350, GL - 120, crate_break_sound,score),
            #Crate(3120, GL - 120, crate_break_sound,score),
            #Crate(3580, GL - 120, crate_break_sound,score),
            #Crate(4535, GL - 120, crate_break_sound,score),
            #Crate(2200, GL - 120, crate_break_sound,score),
            #Crate(1560, 365, crate_break_sound,score),
            #Crate(1000, GL - 150,crate_break_sound,score),
            #SolidCrate(1000, GL - 250, crate_break_sound,score),
            #SolidCrate(100, GL - 120, crate_break_sound,score),
        ]
        enemies = [
            #Enemy_bird(1000, 200, 50, 50, damage=0),   
            #Enemy_bird(2300, 200, 50, 50, damage=0),   
            #Enemy_bird(3360, 200, 50, 50, damage=0),   
            #Enemy_bird(4535, 200, 50, 50, damage=0),  
            #CandyRollEnemy(1500, 550, speed=3, damage=0.1, score=score, points=50),
            Enemy(50, 5, 500,Starting_projectile,(1200, GL-100), "enemy1.png")
        ]
        collectables = [
            #Collectable(500, 180, 40, 40, "LemLife.png", 100, is_life=True),
            #Collectable(2250, 150, 40, 40, "LemLife.png", 100, is_life=True),
            #Collectable(2250, 100, 40, 40, "Lempoints.png", 20),
            #Collectable(2200, 150, 40, 40, "Lempoints.png", 20),
            #Collectable(2300, 150, 40, 40, "Lempoints.png", 20),
            #Collectable(2250, 200, 40, 40, "Lempoints.png", 20),
            #Collectable(280, 380, 40, 40, "Lempoints.png", 20),
            #Collectable(1625, 100, 40, 40, "Lempoints.png", 20),
            #Collectable(1634, 200, 40, 40, "Lempoints.png", 20),
            #Collectable(1625, 300, 40, 40, "Lempoints.png", 20),
            #Collectable(1305, 450, 40, 40, "Lempoints.png", 20),
            #Collectable(970, 500, 40, 40, "Lempoints.png", 20),
            #Collectable(1210, 200, 40, 40, "Lempoints.png", 20),
            #Collectable(2755, 310, 40, 40, "Lempoints.png", 20),
            #Collectable(2845, 250, 40, 40, "Lempoints.png", 20),
            #Collectable(2955, 300, 40, 40, "Lempoints.png", 20),
            #Collectable(3075, 350, 40, 40, "Lempoints.png", 20),
            #Collectable(4080, 550, 40, 40, "Lempoints.png", 20),
            #Collectable(1210, 200, 40, 40, "Lempoints.png", 20),
            #Collectable(3600, 180, 40, 40, "Lempoints.png", 20),
            #Collectable(4580, 180, 40, 40, "Lempoints.png", 20),
            #Collectable(4300, 310, 40, 40, "Lempoints.png", 20)
    
        ]
        score.increment(0)
        print("Level 2 loaded.")

    def check_level_2_conditions(self):
        global Boss_1_done
        if Boss_1_done:
            return True
#--------------------------------------------------------------------------------------------------LEVEL 3---BEGINING----GO GO GO
    def level_3(self):
        global projectiles, platforms, Effect_boxes, MAP_WIDTH, MAP_HEIGHT, enemies, crates, collectables, score
        MAP_WIDTH = 5000
        MAP_HEIGHT = 800
        projectiles = []
        platforms = [
            Platform(400, GL - 100, 100, 20, "PF_0.png"),
            Platform(600, GL - 150, 150, 20, "PF_0.png"),
            Platform(800, GL - 200, 200, 20, "PF_0.png"),
            Platform(1200, GL - 100, 500, 20, "PF_0.png"),
            Platform(1600, GL - 250, 500, 20, "PF_0.png"),
            Platform(2000, GL - 400, 500, 20, "PF_0.png")
        ]
        Effect_boxes = []
        crates = [
            Crate(100, GL - 50, crate_break_sound,score),
            SolidCrate(500, GL - 50,crate_break_sound,score)  # Create a solid crate
        ]
        enemies = []
        collectables = [
            Collectable(200, GL - 40, 40, 40, "LemLife.png", 5),
            Collectable(500, GL - 40, 40, 40, "Lempoints.png", 10)
        ]
        score.increment(0)
        print("Level 3 loaded.")

    def check_level_3_conditions(self):
        global Boss_2_done
        if Boss_2_done:
            return True
#--------------------------------------------------------------------------------------------------LEVEL 3---END WORKING

    def Gameover(self):
        player.position = pygame.Vector2(100, GL)
        player.health = player.maxhealth
        player.lives -= 1
        if player.lives >= 0:
            self.reset_level()
            self.load_level()
        else:
            pygame.quit()
# -- Functions --

def update_camera(player_pos):
    camera_x = player_pos.x - screen.get_width() // 2  # Center camera on player
    return max(0, min(camera_x, MAP_WIDTH - screen.get_width()))  # Clamp to map edges

def class_change_Assasin(Player):
    global Class_picked

    player.name = "Assasin"
    player.maxhealth = 50000
    player.health = Player.maxhealth
    player.speed = 10
    new_projectile = Projectile("bullet_sm.png", 75, 5000, 100)
    new_weapon = Weapon("Sniper", "Juice Gun_.png", new_projectile, 3, 2, 0.5, 0, True)
    
    player.weapon.projectile.sprite = new_projectile.sprite
    player.weapon.projectile.sprite_carry = new_projectile.sprite_carry
    player.weapon.sprite = new_weapon.sprite
    player.weapon = new_weapon

    player.weapon = new_weapon

    player.effect = Player_Effect_Dash
    player.effect_cooldown = 2

    Class_picked = True

def class_change_Tank(Player):
    global Class_picked

    player.name = "Tank"
    player.maxhealth = 200
    player.health = Player.maxhealth
    player.speed = 3
    new_projectile = Projectile("D2.png", 30, 300, 20)
    new_weapon = Weapon("Shotgun", "Slingshot Empty.png", new_projectile, 6, 1, 0, 30, True)
    
    player.weapon.projectile.sprite = new_projectile.sprite
    player.weapon.projectile.sprite_carry = new_projectile.sprite_carry
    player.weapon.sprite = new_weapon.sprite
    player.weapon = new_weapon
    
    player.weapon = new_weapon
    Class_picked = True

    player.effect = Player_Effect_Heal
    player.effect_cooldown = 10

def class_change_Soldier(Player):
    global Class_picked

    player.name = "Soldier"
    player.maxhealth = 100
    player.health = Player.maxhealth
    player.speed = 5
    new_projectile = Projectile("bullet.png", 40, 600, 30)
    new_weapon = Weapon("Machine Gun", "Gun.png", new_projectile, 30, 1.5, 0.2, 10, True)
    
    player.weapon.projectile.sprite = new_projectile.sprite
    player.weapon.projectile.sprite_carry = new_projectile.sprite_carry
    player.weapon.sprite = new_weapon.sprite
    player.weapon = new_weapon
    
    player.weapon = new_weapon
    Class_picked = True

    player.effect = Player_Effect_Sprint

def heal_player(player):
    player.health += 20 # Heal up to max health

def Damage_player(player):
    player.health -= 1  # Damage up to health

def increase_ammo(player):
    player.weapon.ammo = min(player.weapon.ammo + 5, player.weapon.mag_size)  # Increase ammo
    print("Ammo increased!")

def boost_speed(player):
    player.speed += 2  # Temporarily increase player speed
    print("Speed boosted!")

def Player_Effect_Dash(player):
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    # Duration for how long the dash effect lasts (in milliseconds)
    dash_duration = 0.2 * 1000  # 200 ms
    dash_speed = 4

    # Check if the player is trying to dash
    if keys[pygame.K_LSHIFT] and not player.effect_active:
        # Check if enough time has passed since the last dash
        if (current_time - player.last_effect_active > player.effect_cooldown * 1000):
            player.last_effect_active = current_time
            player.speed_boost = dash_speed  # Set the speed boost during dash
            player.effect_active = True  # Set the dashing flag to True
    else:
        # Reset speed boost if the dash duration has passed
        if player.effect_active and (current_time - player.last_effect_active >= dash_duration):
            player.speed_boost = 1  # Reset to normal speed
            player.effect_active = False  # Reset the dashing flag

def Player_Effect_Sprint(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT]:
        player.speed_boost = 3
    else:
        player.speed_boost = 1

def Player_Effect_Heal(player):
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    # Duration for how long the dash effect lasts (in milliseconds)
    Heal_duration = 2 * 1000  # 200 ms
    Heal_ammount = 25
    speed_deacrease = 0.75

    # Check if the player is trying to dash
    if keys[pygame.K_LSHIFT] and not player.effect_active:
        # Check if enough time has passed since the last dash
        if (current_time - player.last_effect_active > player.effect_cooldown * 1000):
            player.last_effect_active = current_time

            player.speed_boost = speed_deacrease  # Set the speed boost during dash
            if player.health + Heal_ammount >= player.maxhealth:
                player.health = player.maxhealth
            else:
                player.health += Heal_ammount
            
            player.effect_active = True  # Set the dashing flag to True
    else:
        # Reset speed boost if the dash duration has passed
        if player.effect_active and (current_time - player.last_effect_active >= Heal_duration):
            player.speed_boost = 1  # Reset to normal speed
            player.effect_active = False  # Reset the dashing flag

#Respawn/Dead
def display_your_dead_message():
    screen.fill((0, 0, 0))  # Clear the screen
    screen.blit(you_died_options, (0, 0))  # Blit the final death screen

    # The End message split into lines
    lines = [
        "ATTENTION OUR DEAR HERO:",
        "...there really is no easy way to say this...",
        "...You laugh in the face of danger no more!",
        "...You have kicked the bucket...",
        "...You're pushing up daisies...",                        
        "",
        "",
        "...[awkward silence]...",
        "...YOU ARE DEAD...",
        "In good news you are a fictional character so you can simply begin again!",
        "...Press ESC to exit...                                                                      ...ENTER to begin again...",
    ]

    # Get the center of the screen for message text
    screen_rect = screen.get_rect()

    # Adjust text rendering (center each line)
    total_text_height = len(lines) * 50  # Calculate total height of the text block
    base_y = screen_rect.centery - total_text_height // 2  # Starting Y position (centered vertically)

    # Render and center each line of text
    for i, line in enumerate(lines):
        pause_text = font.render(line, True, (41, 148, 214))  # Render the line
        text_rect = pause_text.get_rect()  # Get the bounding rectangle of the text
        text_rect.center = (screen_rect.centerx, base_y + i * 50)  # Center horizontally and space vertically
        screen.blit(pause_text, text_rect)  # Display the text

    pygame.display.flip()

def your_dead():
    paused = True
    frame = 0  # Track the animation frame
    theme_song.stop()
    Lastwords.play()  # Play the death sound
    animation_done = False  # Track if the animation has finished

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press Esc to quit the game
                    pygame.quit()

                elif event.key == pygame.K_RETURN:  # Press Enter to restart the game
                    Lastwords.stop()
                    return True  # Resume the game and respawn

        if not animation_done:
            if frame < len(you_died):  # Play the animation
                screen.fill((0, 0, 0))  # Clear the screen
                screen.blit(you_died[frame], (0, 0))  # Display the current death frame
                frame += 1  # Go to the next frame
                pygame.time.delay(600)  # Control the speed of the animation
            else:
                animation_done = True  # End the animation

        else:
            display_your_dead_message()  # Display the final death screen

        pygame.display.flip()

    return False  # End the death state and resume

#Pause Screen Layout
def display_pause_message():
    screen.fill((0, 0, 0))  # Clear the screen
    screen.blit(pause_image, (0, 0))  # Blit it at the top-left corner
    screen.blit(transparency_image, image_rect.topleft)  # Blit it at the top-left corner

    # The pause message split into lines
    lines = [
        "ATTENTION OUR DEAR HERO:", #potential to add name funct at the start
        "There is NO ESCAPE, the only way out is through!",
        "You must take this moment to FIGHT ON!",
        "'our hero fist pumps the air ...'",
        "... and presses ENTER to return to the game.",
        ".... OR ...",
        "Press escape again to sprint away bravely...",
        "... into the arms of shame!",
    ]

    # Get the center of the screen
    screen_rect = screen.get_rect()

    # Set the base height (e.g., 1/3rd from the top of the screen)
    base_y = screen_rect.centery - 180  # Adjust the starting height here

    # Render and center each line of text
    for i, line in enumerate(lines):
        pause_text = font.render(line, True, (41, 148, 214))  # Render the line
        text_rect = pause_text.get_rect()  # Get the bounding rectangle of the text
        text_rect.center = (screen_rect.centerx, base_y + i * 50)  # Center the text
        screen.blit(pause_text, text_rect)  # Display the text
    pygame.display.flip()

def pause_game():
    paused = True
    pause_sound.play()  # Play the sound when the game is paused
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press Esc to quit the game
                    pygame.quit()
                    return

                elif event.key == pygame.K_RETURN:  # Press Enter to resume the game
                    paused = False

        display_pause_message()

#---------------------------------------------------------------------------------------------------------------------------------------------
# -- Initialize Game ---------------------------------------------------------------------------------------------------------------------------
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Game Thingy mabob')

#Audio initialisations
pygame.mixer.init()

# Load the sound effects
theme_song = pygame.mixer.Sound("Theme.WAV")
life_sound = pygame.mixer.Sound("FreeLife.mp3")
lempoints_sound = pygame.mixer.Sound("Lempoints.mp3")
player_sound = pygame.mixer.Sound("Footsteps.mp3")
crate_break_sound = pygame.mixer.Sound("Cratebreak.mp3")
pause_sound = pygame.mixer.Sound("pause.WAV") 
Lastwords = pygame.mixer.Sound("LGQuote_End Game.mp3")

# Create mixer channels
theme_song_channel = pygame.mixer.Channel(0)  # Channel 0 for theme song
life_sound_channel = pygame.mixer.Channel(1)  # Channel 1 for life sound
lempoints_channel = pygame.mixer.Channel(2)  # Channel 2 for lempoints sound
player_sound_channel = pygame.mixer.Channel(3)  # Channel 3 for player sound
crate_break_channel = pygame.mixer.Channel(4)  # Channel 4 for crate break sound
pause_sound_channel = pygame.mixer.Channel(5)  # Channel 5 for pause sound
lastwords_channel = pygame.mixer.Channel(6)  # Channel 6 for Lastwords sound

# Set the volume to 50% (0.5)
theme_song.set_volume(0.8)
life_sound.set_volume(0.5)
lempoints_sound.set_volume(0.7)
crate_break_sound.set_volume(0.7)
player_sound.set_volume(0.1)
Lastwords.set_volume(.8)

#Loop theme tune
theme_song.play(loops=-1)

# Set the clock
clock = pygame.time.Clock()

#Graphic initialisations
background0_image = pygame.image.load("BG_0.png").convert()
#In Game Headingsdddd
Ammo = pygame.image.load("M0.png").convert_alpha()
Juicebar = pygame.image.load("M1.png").convert_alpha()
Lives = pygame.image.load("M2.png").convert_alpha()
LemPoints = pygame.image.load("M3.png").convert_alpha()
PF_small = pygame.image.load("PF_0.png").convert_alpha()
PD_spike = pygame.image.load("SP_0.png").convert_alpha()

# Load the pause screens
pause_image = pygame.image.load('BGpause.png')
pause_image = pygame.transform.scale(pause_image, (1200,800))  # Scale image to screen size
transparency_image = pygame.image.load('Transparency_alpha.png')
transparency_image = pygame.transform.scale(transparency_image, (1200,800))  # Scale image to screen size
transparency_image.set_alpha(230)  # Set the alpha for transparency (0-255; 255 is fully opaque)
image_rect = transparency_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

# Load the death sequence for animation
you_died = [pygame.transform.scale(pygame.image.load(f"LG_die_{i}.png"), (1200,800)) for i in range(0, 15)]
you_died_options = pygame.transform.scale(pygame.image.load("LG_die_15.png"), (1200,800))

# Font for the warning message
font = pygame.font.SysFont(None, 30)

# Sample projectile and weapon initialization
Starting_projectile = Projectile("bullet.png", 50, 600, 1)
Starting_weapon = Weapon("Pistol", "Gun.png", Starting_projectile, 6, 1, 0.3, 0, True)

# Create the playera
player = Player("No Class", 100, 3, 5, Starting_weapon, "player.png", Player_Effect_Sprint)

# Initialize global projectile list, platforms and Effect_boxes-------------------------------------------------------------------INITIALISE ITEM LISTS
Game_Manager = GameManager()
projectiles = []
platforms = []
Effect_boxes= []
enemies = []
collectables = []
crates = []
score = Score()

#For placing out items
def print_player_position(player):
    print(f"Player position: x = {player.position.x}, y = {player.position.y}")

def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # Check for key press events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pause the game on Esc
                    pause_game()         
        if player.health <= 0:  # Check if player is dead
            your_dead()
            player.respawn()  # Respawn the player after the death sequence

        print_player_position(player)
        # This controls what is on the map runn by global veriables
        Game_Manager.load_level()
        Game_Manager.progress_manager() 

        #initial background - move to levels?
        screen.blit(background0_image, (0, 0))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Update camera position based on player
        camera_x = update_camera(player.position)

        # Draw projectiles, platforms, Effect Boxes and Enemys
        for projectile in projectiles:
            projectile.draw(screen)

        player.apply_gravity()

        for platform in platforms:
            if isinstance(platform, Platform):
                platform.draw(screen, camera_x)
            elif isinstance(platform, Crate):
                # Draw crate relative to the camera
                adjusted_position = platform.rect.move(-camera_x, 0)
                screen.blit(platform.image, adjusted_position.topleft)

        for box in Effect_boxes:
            box.draw(screen, camera_x)
            box.interact(player)

        for enemy in enemies:
            if isinstance(enemy, CandyRollEnemy):
                # Pass the necessary arguments for CandyRollEnemy
                enemy.update(1/60, platforms, crates, player)  # Assuming 'dt' is approximately 1/60 for 60 FPS
            else:
                # Use the regular update for other enemies
                enemy.update(player.position)

            enemy.draw(screen, camera_x)

            # If the enemy has a 'shoot' method, then it can shoot at the player
            if hasattr(enemy, 'shoot'):
                enemy_projectiles = enemy.shoot(player.position, camera_x)
                if enemy_projectiles:
                    # The `shoot()` method should return a list of projectilesdd
                    projectiles.extend(enemy_projectiles)

            # Check for collision between projectiles and enemies
            for projectile in projectiles:
                if hasattr(enemy, 'take_damage'):
                    if projectile.sprite.get_rect(center=projectile.position).colliderect(enemy.rect):
                        enemy.take_damage(projectile.damage)
                        projectile.active = False  # Remove the projectile after it hits
                        break

        for collectable in collectables:
            collectable.draw(screen, camera_x)
            collectable.interact(player, score)#need to interact with JB score

        screen.blit(Ammo, (950, 60))
        screen.blit(Lives, (1050, 720))
        screen.blit(LemPoints, (70, 725))
        score.draw(screen)

        # -- Handle player movement --
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_a]:  # Move left
            direction.x = -1
        if keys[pygame.K_d]:  # Move right
            direction.x = 1

        player.move(direction)

        # Jump if space key is pressed
        if keys[pygame.K_SPACE]:
            player.jump()

        for crate in crates[:]:
            crate.update()
            # If the crate animation is complete, remove it from the collision check
            if crate.broke_done:
                crates.remove(crate)
            else:
                # Draw crate relative to the camera
                adjusted_position = crate.rect.move(-camera_x, 0)
                screen.blit(crate.image, adjusted_position.topleft)

        # Check player-crate collision AFTER player movement and gravity
        for crate in crates:
            check_player_crate_collision(player, crate)

        # Clamp player position to keep them within the map boundaries
        player.position.x = max(0, min(player.position.x, MAP_WIDTH))
        player.position.y = max(0, min(player.position.y, MAP_HEIGHT))

        # Draw the player relative to the camera
        player.draw(screen, camera_x)
        
        #-- Handle player Weapon and effect --

        player.Player_effect(player)

        # Aim the weapon using the mouse position then draw it
        player.weapon.aim(mouse_pos)
        player.weapon.draw(screen, mouse_pos)

        # Shoot if left mouse button is pressed
        if pygame.mouse.get_pressed()[0]:
            new_projectile = player.weapon.shoot()
            if new_projectile:
                projectiles.append(new_projectile)

        # Reload if R key is pressed
        if keys[pygame.K_r]:
            player.weapon.reload()

        #all_sprites.update()#not sure if this one is needed
        #enemies.update() 

        for enemy in enemies:
            if hasattr(enemy, 'deal_damage'):
                enemy.deal_damage(player)    

        # Update projectiles - to move and delete if they move to far
        for projectile in projectiles[:]:
            projectile.move()
            if not projectile.active:
                projectiles.remove(projectile)

                    # Remove dead enemies
        for enemy in enemies[:]:
            if not enemy.alive:
                enemies.remove(enemy)

        # Update reload status
        player.weapon.update_reload()

        # Draw Player Stats
        player.draw_Stats(screen)

        screen.blit(Juicebar, (30, 40))

        pygame.display.flip()
        clock.tick(60)

    return True

# Main game execution
if __name__ == "__main__":
    while True:
        if not game_loop():
            break

pygame.quit()