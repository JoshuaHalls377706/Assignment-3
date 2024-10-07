import pygame
import math
import random

# -- Classes --

class Projectile:
    def __init__(self, sprite, bullet_speed, range, damage):
        self.sprite_carry = sprite
        self.sprite = pygame.image.load(sprite).convert_alpha()  # Load the projectile sprite
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
        self.sprite = pygame.image.load(sprite).convert_alpha()  # Load the weapon sprite image
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

    def aim(self, mouse_pos, weapon_pos, camera_x):
        """Calculate the direction to aim based on mouse and weapon position."""
        # Adjust mouse position by adding the camera position
        adjusted_mouse_pos = (mouse_pos[0] + camera_x, mouse_pos[1])

        spread_offset_x = random.uniform(-self.spread, self.spread)
        spread_offset_y = random.uniform(-self.spread, self.spread)

        dx = (adjusted_mouse_pos[0] + spread_offset_x) - weapon_pos[0]
        dy = (adjusted_mouse_pos[1] + spread_offset_y) - weapon_pos[1]
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

        # Calculate the angle based on the direction
        self.angle = math.degrees(math.atan2(-dy, dx)) if distance != 0 else 0

        # Check if the weapon is facing left
        if dx < 0:  # If the weapon is facing left
            rotated_sprite = pygame.transform.flip(self.sprite, False, True)  # Flip vertically
        else:
            rotated_sprite = self.sprite

        rotated_sprite = pygame.transform.rotate(rotated_sprite, self.angle)
        rect = rotated_sprite.get_rect(center=weapon_pos)
        surface.blit(rotated_sprite, rect.topleft)

class Player:
    def __init__(self, name, health, lives, speed, weapon, sprites_walk):
        self.name = name
        self.health = health
        self.lives = lives
        self.speed = speed
        self.weapon = weapon
        
        # Load walking sprites
        self.sprites_walk = [pygame.image.load(f"LG_walk_side{i}.png").convert_alpha() for i in range(0, 2)]
        
        self.current_sprite = self.sprites_walk[0]
        self.sprite_index = 0
        self.sprite_animation_speed = 5  # Adjust to control speed of animation
        self.animation_counter = 0

        self.position = pygame.Vector2(100, 300)  # Starting position
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = True
        self.sprite_rect = self.current_sprite.get_rect()  # Get the sprite's rect

    def move(self, direction):
        self.position += direction * self.speed
        
        # Update sprite based on movement
        if direction.x != 0:  # If moving
            self.animation_counter += 1
            if self.animation_counter >= self.sprite_animation_speed:
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites_walk)
                if direction.x > 0:  # Moving right
                    self.current_sprite = self.sprites_walk[self.sprite_index]
                else:  # Moving left
                    self.current_sprite = pygame.transform.flip(self.sprites_walk[self.sprite_index], True, False)
                self.animation_counter = 0

    def jump(self):
        if self.on_ground:
            self.velocity.y = -15  # Jump height
            self.on_ground = False

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity.y += 0.5  # Gravity effect
            self.position.y += self.velocity.y
            if self.position.y >= 300:  # Ground level
                self.position.y = 300
                self.velocity.y = 0
                self.on_ground = True

    def draw(self, surface, camera_x):
        draw_x = self.position.x - camera_x - (self.sprite_rect.width / 2)
        draw_y = self.position.y - self.sprite_rect.height  # Align to the bottom
        surface.blit(self.current_sprite, (draw_x, draw_y))

# -- Functions --

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Weapon Test with Scrolling')

# Set the clock
clock = pygame.time.Clock()

# Sample projectile and weapon initialization
sample_projectile = Projectile("bullet.png", 10, 500, 25)
sample_weapon = Weapon("Pistol", "Gun.png", sample_projectile, 100, 2, 0.01, 30, True)

# Create the player
player = Player("Hero", 100, 3, 5, sample_weapon, "player.png")

# List to hold projectiles
projectiles = []

# Set the map size
MAP_WIDTH = 2400
MAP_HEIGHT = 800

# Define the areas with (x_position, width, color)
areas = [
    (0, 800, (255, 0, 0)),  # Red area
    (800, 800, (0, 255, 0)),  # Green area
    (1600, 800, (0, 0, 255)),  # Blue area
]

def draw_areas(surface, camera_x):
    for area in areas:
        area_x, area_width, area_color = area
        # Only draw the area if it's in the view of the camera
        if area_x + area_width > camera_x and area_x < camera_x + 1200:
            # Calculate the actual position based on camera
            draw_x = area_x - camera_x
            # Draw the rectangle for the area
            pygame.draw.rect(surface, area_color, (draw_x, 0, area_width, MAP_HEIGHT))

# Update the game_loop function to pass the mouse position
def game_loop():
    camera_x = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        weapon_pos = (player.position.x + 30, player.position.y - 10)  # Using offset for weapon position

        # Aim the weapon
        player.weapon.aim(mouse_pos, weapon_pos, camera_x)

        # Clear the screen
        draw_areas(screen, camera_x)

        # Handle player movement
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_a]:  # Move left
            direction.x = -1
        if keys[pygame.K_d]:  # Move right
            direction.x = 1

        player.move(direction)  # Move the player based on input

        # Jump if space key is pressed
        if keys[pygame.K_SPACE]:
            player.jump()

        # Apply gravity to the player
        player.apply_gravity()

        # Clamp player position to keep them within the map boundaries
        player.position.x = max(0, min(player.position.x, MAP_WIDTH))
        player.position.y = max(0, min(player.position.y, MAP_HEIGHT))

        # Update camera position to keep the player centered
        camera_x = max(0, min(player.position.x - 400, MAP_WIDTH - 1200))

        # Draw the player
        player.draw(screen, camera_x)

        # Calculate weapon position based on player position
        weapon_draw_pos = (player.position.x - camera_x, player.position.y - 100)

        # Draw projectiles
        for projectile in projectiles:
            projectile.draw(screen)

        # Draw the weapon sprite after aiming
        player.weapon.draw(screen, weapon_draw_pos, mouse_pos)

        # Shoot if left mouse button is pressed
        if pygame.mouse.get_pressed()[0]:
            new_projectile = player.weapon.shoot(weapon_draw_pos)
            if new_projectile:
                projectiles.append(new_projectile)

        # Reload if R key is pressed
        if keys[pygame.K_r]:
            player.weapon.reload()

        # Update projectiles
        for projectile in projectiles[:]:
            projectile.move()
            if projectile.distance_travelled >= projectile.range:
                projectiles.remove(projectile)

        # Update reload status
        player.weapon.update_reload()

        pygame.display.flip()
        clock.tick(60)

    return True

# Main game execution
if __name__ == "__main__":
    while True:
        if not game_loop():
            break

pygame.quit()