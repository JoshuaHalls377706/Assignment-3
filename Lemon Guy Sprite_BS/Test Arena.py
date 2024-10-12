import pygame
from Player import Player
from Crate import Crate, check_player_crate_collision, SolidCrate
from Collectable import Collectable
from Score import Score

# Test Arena Section (Initialization)

# 1. Initialize Pygame and Clock
pygame.init()
clock = pygame.time.Clock()

# 2. Screen Setup
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The story of the nice Lemon Guy")

# 3. Background Setup
background_image = pygame.image.load("background2.png")
original_width, original_height = background_image.get_size()
new_width = int(original_width * (SCREEN_HEIGHT / original_height))
background_image = pygame.transform.scale(background_image, (new_width, SCREEN_HEIGHT))

# 4. Define Constants
ORIGINAL_GROUND_LEVEL = 680  # Adjust the ground level as needed
MAX_JUMP_HEIGHT = 200  # Maximum height a player can jump

# 5. Initialize Player
player = Player(200, ORIGINAL_GROUND_LEVEL, ORIGINAL_GROUND_LEVEL)

# 6. Initialize Crates (Both Breakable and Non-Breakable)
crates = pygame.sprite.Group()

# Create multiple breakable and non-breakable crates
breaking_crate1 = Crate(650, 525)
breaking_crate2 = Crate(750, 525)
solid_crate1 = SolidCrate(850, 525)
solid_crate2 = SolidCrate(950, 525)

# Add crates to the crates group
crates.add(breaking_crate1, breaking_crate2, solid_crate1, solid_crate2)

# 7. Initialize Collectables
collectable_info = [
    {"count": 5, "image": "lemonpoints.png", "points": 10},
    {"count": 3, "image": "head.png", "points": 15}
]
collectable_group = Collectable.create_collectables(collectable_info, new_width, ORIGINAL_GROUND_LEVEL, MAX_JUMP_HEIGHT)

# 8. Create Main Sprite Group and Add All Sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(crates)  # Add crate group to all_sprites
all_sprites.add(collectable_group)

# 9. Initialize Score System
game_score = Score()

# 10. Initialize Font for Displaying Score
font = pygame.font.SysFont('Arial', 30)

# 11. Additional Setup (Camera, etc.)
camera_x = 0  # Initial camera x-position
camera_speed = 5
#-----------------------------------------------------------------------------------------------------------------------------------
# Main game loop
# Main game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player.jump()

    # Update the player's position
    player.update()

    # Check for player collisions with each crate in the crates group
    for crate in crates:
        check_player_crate_collision(player, crate)

    # Check for collisions with collectables
    collected_items = pygame.sprite.spritecollide(player, collectable_group, False)
    for collectable in collected_items:
        points = collectable.collect()  # Get points from the collectable
        game_score.add_points(points)   # Add points to the score
        collectable_group.remove(collectable)  # Remove the collectable from the collectable group
        all_sprites.remove(collectable)  # Remove the collectable from the all_sprites group

    # Update all sprites (includes crate updates)
    all_sprites.update()

    # Check if any crates have completed their breaking animation and remove them
    for crate in crates:
        if crate.broke_done:
            all_sprites.remove(crate)  # Remove the crate from the game after it has fully broken
            crates.remove(crate)  # Remove it from the crates group

    # Calculate the camera offset based on the player's position
    player_x = player.rect.centerx  # Get the player's x position
    camera_x = min(max(0, player_x - SCREEN_WIDTH // 2), new_width - SCREEN_WIDTH)

    # Draw the background with camera offset
    screen.blit(background_image, (-camera_x, 0))

    # Draw all sprites (with camera offset)
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

    # Display the score on the screen
    game_score.display_score(screen, font)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

