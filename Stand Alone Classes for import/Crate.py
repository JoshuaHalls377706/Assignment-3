import pygame

crate_animation_speed = 0.1
STAND_TIME_BEFORE_ANIMATING = 1000  # Time before the crate breaks after standing on it

class Crate(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.idle_sprite = pygame.image.load('crate_idle.png')  # Crate before broken
        self.broke_sprites = [
            pygame.image.load(f'crate_{i}.png') for i in range(2)  # Load broken frames
        ]
        self.current_sprite = 0
        self.image = self.idle_sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        # Crate state variables
        self.player_on_crate = False
        self.arming = False
        self.broken = False
        self.broke_done = False
        self.start_time_on_crate = None  # Timer for breaking

    def update(self):
        # Handle broken animation
        if self.broken and not self.broke_done:
            print(f"Breaking crate... Current sprite: {self.current_sprite}")
            self.current_sprite += crate_animation_speed  # Advance through the broken frames
            if int(self.current_sprite) >= len(self.broke_sprites):
                self.broke_done = True  # Animation is complete
                print("Crate has fully broken.")
            else:
                self.image = self.broke_sprites[int(self.current_sprite)]

        # If the crate is armed but not yet broken, keep idle sprite
        elif self.arming:
            print("Crate armed and waiting to break.")
            self.image = self.idle_sprite  # Crate looks idle but is "armed"


def check_player_crate_collision(player, crate):
    print(f"Player rect: {player.rect}, Crate rect: {crate.rect}")

    if player.rect.colliderect(crate.rect) and not crate.broken:
        print("Player collided with crate.")

        # Ensure the player is falling and colliding with the crate from above
        if player.velocity_y > 0:
            print("Player is landing on the crate.")
            
            # Adjust player's position to be on top of the crate
            player.rect.bottom = crate.rect.top
            player.velocity_y = 0  # Stop the downward velocity
            player.is_jumping = False  # Stop the jumping state
            player.ground_level = crate.rect.top  # Set the ground level to the top of the crate
            crate.player_on_crate = True

            # Start the timer for breaking the crate
            if crate.start_time_on_crate is None:
                crate.start_time_on_crate = pygame.time.get_ticks()
                print("Crate timer started.")  # Debugging print

            # Check if the player has stood long enough to break the crate
            elapsed_time = pygame.time.get_ticks() - crate.start_time_on_crate
            if elapsed_time >= STAND_TIME_BEFORE_ANIMATING and not crate.broken:
                print(f"Crate breaking after {elapsed_time / 1000} seconds.")
                crate.arming = True
                crate.broken = True  # Trigger breaking animation

    # If the player jumps off the crate, reset the ground level
    elif crate.player_on_crate and not player.rect.colliderect(crate.rect):
        print("Player jumped off crate.")
        crate.player_on_crate = False  # Player is no longer on the crate
        player.ground_level = player.original_ground_level  # Reset ground level after jumping off

class SolidCrate(Crate):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        # Override the image with a static crate image
        self.idle_sprite = pygame.image.load('static_crate.png')  # Static crate image
        self.image = self.idle_sprite  # Set the image to the static crate image
        self.broken = False  # Ensure it never breaks

    # No need to handle breaking logic, as the crate won't break
    def update(self):
        # Just keep the static image
        self.image = self.idle_sprite




