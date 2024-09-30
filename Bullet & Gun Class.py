"""
What dose this Code do:
It makes a bullet using a class.
it then uses that bullet to design a gun.

Then runs a trial code to see how it behaves
"""

import time
import pygame
import math
import random

# -- Classes --

class Projectile:
    def __init__(self, sprite, bullet_speed, range, damage):
        self.sprite_carry = sprite
        self.sprite = pygame.image.load(sprite)
        self.bullet_speed = bullet_speed
        self.range = range
        self.damage = damage
        self.position = (0, 0)  # Starting position
        self.direction = (0, 0)  # Direction of movement
        self.distance_travelled = 0

    def move(self):
        if self.distance_travelled < self.range:
            self.position = (
                self.position[0] + self.direction[0] * self.bullet_speed,
                self.position[1] + self.direction[1] * self.bullet_speed,
            )
            self.distance_travelled += self.bullet_speed

    def draw(self, surface):
        angle = math.degrees(math.atan2(-self.direction[1], self.direction[0]))  # Calculate angle
        rotated_sprite = pygame.transform.rotate(self.sprite, angle)  # Rotate sprite
        rect = rotated_sprite.get_rect(center=self.position)  # Get new rect for positioning
        surface.blit(rotated_sprite, rect.topleft)

class Weapon:
    def __init__(self, name, sprite, projectile, mag_size, reload_time, attackspeed, spread=0, use_mag=True):
        self.name = name
        self.sprite = pygame.image.load(sprite)  # Load the weapon sprite image
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
        self.angle = 0

    def aim(self, mouse_pos, weapon_pos):
        """Calculate the direction to aim based on mouse and weapon position."""
        spread_offset_x = random.uniform(-self.spread, self.spread)
        spread_offset_y = random.uniform(-self.spread, self.spread)

        dx = (mouse_pos[0] + spread_offset_x) - weapon_pos[0]
        dy = (mouse_pos[1] + spread_offset_y) - weapon_pos[1]
        distance = math.hypot(dx, dy)

        if distance != 0:
            self.projectile.direction = (dx / distance, dy / distance)
        else:
            self.projectile.direction = (0, 0)

    def shoot(self, weapon_pos):
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_shot_time >= self.attackspeed * 1000 and
                self.ammo > 0 and not self.reloading):
            self.last_shot_time = current_time
            if self.use_mag:
                self.ammo -= 1
            new_projectile = Projectile(self.projectile.sprite_carry, self.projectile.bullet_speed, self.projectile.range, self.projectile.damage)
            new_projectile.position = weapon_pos
            new_projectile.direction = self.projectile.direction
            return new_projectile
        elif self.ammo <= 0:
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
                print('Weapon reloaded!')

    def draw(self, surface, weapon_pos, mouse_pos):
        dx = mouse_pos[0] - weapon_pos[0]
        dy = mouse_pos[1] - weapon_pos[1]
        distance = math.hypot(dx, dy)

        self.angle = math.degrees(math.atan2(-dy, dx)) if distance != 0 else 0
        
        y_scale_factor = 1 if (0 <= self.angle <= 90) or (270 <= self.angle <= 360) else 1

        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        width, height = rotated_sprite.get_size()
        scaled_sprite = pygame.transform.scale(rotated_sprite, (width, height * y_scale_factor))

        rect = scaled_sprite.get_rect(center=weapon_pos)
        surface.blit(scaled_sprite, rect.topleft)

# -- Functions --

# -- Actual Code --

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Weapon Test')

# Set the clock
clock = pygame.time.Clock()

# Sample projectile and weapon initialization

# sample_projectile = Projectile("Sprite.png", Bullet Speed, Distance to travel, Damage/bullet)
sample_projectile = Projectile("bullet.png", 10, 500, 25)
# sample_weapon = Weapon("Name", "Sprite.png", projectile, Mag Size, Time for Reload, Fire Rate, Spread, "Use_Mag = True")
sample_weapon = Weapon("Pistol", "Gun.png", sample_projectile, 15, 2, 0.0001, 100, True)

# List to hold projectiles
projectiles = []

def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        mouse_pos = pygame.mouse.get_pos()
        weapon_pos = (500, 500)

        # Aim the weapon
        sample_weapon.aim(mouse_pos, weapon_pos)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw projectiles
        for projectile in projectiles:
            projectile.draw(screen)

        # Draw the weapon sprite after aiming
        sample_weapon.draw(screen, weapon_pos, mouse_pos)

        # Shoot if left mouse button is pressed
        if pygame.mouse.get_pressed()[0]:
            new_projectile = sample_weapon.shoot(weapon_pos)
            if new_projectile:
                projectiles.append(new_projectile)

        # Reload if R key is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            sample_weapon.reload()

        # Update projectiles
        for projectile in projectiles[:]:
            projectile.move()
            if projectile.distance_travelled >= projectile.range:
                projectiles.remove(projectile)

        # Update reload status
        sample_weapon.update_reload()

        pygame.display.flip()
        clock.tick(60)

    return True

# Main game execution
if __name__ == "__main__":
    while True:
        if not game_loop():
            break

pygame.quit()