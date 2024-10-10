import os
import pygame
import sys

#---------------------------------------------------------------------------------------------------------
# Game setup 
#---------------------------------------------------------------------------------------------------------

# Set working directory to where the script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
clock = pygame.time.Clock()

#----------------------------------------------------------------------------------------------------------------
# Game Screen load
#----------------------------------------------------------------------------------------------------------------

# Screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("From the teammate who doesnt contribute")

# BG pic test
background_image = pygame.image.load("background2.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale it to fit the screen

#----------------------------------------------------------------------------------------------------------------
# Define crate animation speed and timer
#----------------------------------------------------------------------------------------------------------------
crate_animation_speed = 0.1  # Controls how fast the crate breaks
STAND_TIME_BEFORE_ANIMATING = 5000  # 5 seconds in milliseconds

#----------------------------------------------------------------------------------------------------------------
# Game Object broken crate class definition
#----------------------------------------------------------------------------------------------------------------

class Crate(pygame.sprite.Sprite):
    def __init__(crateobject, pos_x, pos_y):
        super().__init__()
        crateobject.idle_sprite = pygame.image.load('crate_idle.png')  # Crate before broken
        crateobject.broke_sprites = [
            pygame.image.load(f'crate_{i}.png') for i in range(2)
        ]  # Load broken sprites
        crateobject.current_sprite = 0
        crateobject.image = crateobject.idle_sprite
        crateobject.rect = crateobject.image.get_rect()
        crateobject.rect.topleft = [pos_x, pos_y]

        # States
        crateobject.player_on_crate = False  # Whether the player is currently on the crate
        crateobject.arming = False  # Whether the crate is "armed" and ready to explode
        crateobject.broken = False  # Whether the crate is in the broken state
        crateobject.broke_done = False  # Whether the broken animation has finished

        # Timer for how long the player stands on the crate
        crateobject.start_time_on_crate = None  # Initialize as None

    def update(self):
        # Handle broken animation
        if self.broken and not self.broke_done:
            print("Crate is breaking...")  # Debugging print statement
            self.current_sprite += crate_animation_speed  # Advance through the broken frames
            if int(self.current_sprite) >= len(self.broke_sprites):
                self.broke_done = True  # Broken animation complete
                print("Crate has fully broken.")  # Debugging print statement
            else:
                self.image = self.broke_sprites[int(self.current_sprite)]
        # If the crate is armed but not yet broken, keep idle sprite
        elif self.arming:
            self.image = self.idle_sprite  # Crate looks idle but is "armed"

#----------------------------------------------------------------------------------------------------------------
# Game Sprite_The Hero_Lemon Guy
#----------------------------------------------------------------------------------------------------------------

sprite_speed = 5  # Adjust this number to change the player's movement speed

# Define the ground level as a constant
ORIGINAL_GROUND_LEVEL = 660  # Adjust the ground level as needed

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('LG_walk_side0.png'))
        self.sprites.append(pygame.image.load('LG_walk_side1.png'))
        self.sprites.append(pygame.image.load('LG_walk_side2.png'))

        # Load the idle sprite image
        self.idle_sprite = pygame.image.load('LG_walk_side2.png')

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        # Variables for jumping
        self.is_jumping = False
        self.jump_speed = -20  # Initial jump velocity
        self.gravity = 1  # Gravity pulling the player down
        self.velocity_y = 0  # Current vertical speed

        # Set ground level to the original ground level
        self.ground_level = ORIGINAL_GROUND_LEVEL  # Start with the original ground level

    def update(self):
        global moving

        # Handle animation when moving
        if moving:
            self.current_sprite += 0.1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
        else:
            self.image = self.idle_sprite  # Set to idle sprite when not moving

        # Apply gravity when jumping or falling
        if self.is_jumping or self.rect.bottom < self.ground_level:
            self.velocity_y += self.gravity  # Apply gravity
            self.rect.y += self.velocity_y  # Update the player's vertical position

            # Check if the player has landed (on the ground or crate)
            if self.rect.bottom >= self.ground_level:  # Use rect.bottom to check if player's feet hit the ground
                self.rect.bottom = self.ground_level  # Set player's bottom to the ground level
                self.velocity_y = 0   # Stop vertical velocity when landing
                self.is_jumping = False  # Stop jumping

    def jump(self):
        if not self.is_jumping:  # Allow jumping only if the player is on the ground or crate
            self.is_jumping = True
            self.velocity_y = self.jump_speed  # Set the initial velocity for jumping

# Initialize player using the original ground level
player = Player(200, ORIGINAL_GROUND_LEVEL) 

def check_player_crate_collision(player, crate):
    # If player lands on crate
    if player.rect.colliderect(crate.rect) and not crate.broken:
        if player.velocity_y > 0 and player.rect.bottom <= crate.rect.top + 10:
            player.rect.bottom = crate.rect.top  # Position player on top of the crate
            player.velocity_y = 0  # Stop downward velocity
            player.is_jumping = False  # Player has landed on the crate
            player.ground_level = crate.rect.top  # Temporarily update ground level to crate's top
            crate.player_on_crate = True  # Track that the player is on the crate

            # Start the timer when the player lands on the crate
            if crate.start_time_on_crate is None:
                crate.start_time_on_crate = pygame.time.get_ticks()
                print("Player landed on crate, timer started.")  # Debugging print statement

            # Check if the player has stood on the crate long enough
            elapsed_time = pygame.time.get_ticks() - crate.start_time_on_crate
            if elapsed_time >= STAND_TIME_BEFORE_ANIMATING and not crate.broken:
                print(f"Crate breaking after {elapsed_time/1000} seconds.")  # Debugging print statement
                crate.arming = True  # Start crate breaking process
                crate.broken = True  # Set crate to broken

    # If player jumps off the crate
    elif crate.player_on_crate and not player.rect.colliderect(crate.rect):
        crate.player_on_crate = False  # Player is no longer on crate
        crate.start_time_on_crate = None  # Reset standing time
        player.ground_level = ORIGINAL_GROUND_LEVEL  # Reset ground level to original value after jumping off
        print("Player jumped off crate, timer reset.")  # Debugging print statement

# Initialize the game loop
run = True

# Creating sprite group and player
moving_sprites = pygame.sprite.Group()
player = Player(200, 380)
moving_sprites.add(player)

# Create a crate and add it to a sprite group
crate = Crate(450, 525)  # Crate at position 
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(crate)

# Main game loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Handle jumping with space or up arrow
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player.jump()

    # Handle key movement
    keys = pygame.key.get_pressed()
    moving = False  # Reset moving status each frame
    if keys[pygame.K_LEFT]:
        player.rect.x -= sprite_speed
        moving = True
    if keys[pygame.K_RIGHT]:
        player.rect.x += sprite_speed
        moving = True

    # Apply gravity if the player is not on the ground or crate
    if player.rect.bottom < player.ground_level:
        player.rect.y += player.velocity_y
        player.velocity_y += player.gravity

    # Check collision with crate and update crate state
    check_player_crate_collision(player, crate)

    # Update and draw everything
    all_sprites.update()  # Update the crate and player
    screen.blit(background_image, (0, 0))  # Draw the background

    # Draw all sprites (player, crate, explosion)
    all_sprites.draw(screen)

    # Remove crate if broken animation is done
    if crate.broke_done:
        all_sprites.remove(crate)

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit the frame rate to 60 FPS

# Quit Pygame
pygame.quit()
