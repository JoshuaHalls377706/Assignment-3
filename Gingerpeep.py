import pygame
import math
import random

GL = 600  # Define GL 

# Gingerpeep's animation frames
GINGERPEEP_FRAMES = [f"B_ging_Sprite {i}.png" for i in range(11)]

# Gingerpeep's projectile frames (add more as needed)
GINGERPEEP_PROJECTILES = [f"B_ging_Projectile {i}.png" for i in range(5)]  # Random projectiles

class Boss_Gingerpeep(pygame.sprite.Sprite):
    def __init__(self, health, damage, shoot_range, projectile_sprites, position, sprite_frames, game_manager, screen_width, score):
        super().__init__()
        self.max_health = health
        self.health = health
        self.position = pygame.Vector2(position)
        self.score = score  # Store the score object to update it on death
        
        # Load animation frames for the boss (these should all stay in the Gingerpeep class)
        self.frames = [pygame.image.load(sprite).convert_alpha() for sprite in sprite_frames]
        self.current_frame = 0
        self.animation_counter = 0
        self.image = self.frames[self.current_frame]  # Start with the first frame

        # Initialize projectile sprites and properties
        self.projectile_sprites = projectile_sprites  # List of projectile sprites to choose from
        self.last_shot_time = 0
        self.attack_speed = 2  # time in seconds between shots
        self.damage = damage
        self.shoot_range = shoot_range
        self.alive = True
        self.game_manager = game_manager
        self.screen_width = screen_width
        self.direction = 1  # 1 for moving right, -1 for moving left
        self.movement_speed = 2  # Speed at which the boss moves side to side
        self.drop_cooldown = 1000  # Cooldown for dropping projectiles in milliseconds
        self.animation_speed = 10  # How quickly the frames should change

    def update(self, player_position):
        if not self.alive:
            return

        # Move side to side within the screen bounds
        self.position.x += self.direction * self.movement_speed
        if self.position.x <= 0 or self.position.x + self.image.get_width() >= self.screen_width:
            self.direction *= -1  # Change direction when hitting screen edges

        # Animate the boss's movement by cycling through frames
        self.animate()

        # Randomly drop projectiles aimed at the player
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.drop_cooldown:
            self.drop_projectile(player_position)
            self.last_shot_time = current_time

    def animate(self):
        # Update the animation timer
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            # Move to the next frame
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def drop_projectile(self, player_position):
        # Randomly choose a projectile sprite
        projectile_sprite = random.choice(self.projectile_sprites)

        # Create a new projectile aimed at the player's position
        dx = player_position.x - self.position.x
        dy = player_position.y - self.position.y
        distance = math.hypot(dx, dy)

        if distance != 0:
            direction = (dx / distance, dy / distance)
        else:
            direction = (0, 0)

        new_projectile = Projectile(
            projectile_sprite,  # Use the randomly selected projectile sprite
            self.projectile.bullet_speed,
            self.projectile.range,
            self.projectile.damage
        )
        new_projectile.position = self.position.xy  # Set the position of the projectile
        new_projectile.direction = direction  # Set the direction toward the player

        # Return the projectile to add it to the game
        return new_projectile

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        # Mark the boss as dead
        self.alive = False

        # Add 1000 points to the score on death
        self.score.increment(1000)

        # Trigger progression to the next level in the GameManager
        if self.game_manager:
            self.game_manager.next_level()  # Progress to the next stage

    def draw(self, surface, camera_x):
        # Draw the boss sprite on the screen relative to the camera
        draw_x = self.position.x - (self.image.get_width() / 2) - camera_x
        draw_y = self.position.y - self.image.get_height()
        surface.blit(self.image, (draw_x, draw_y))

#--------------------------------------
