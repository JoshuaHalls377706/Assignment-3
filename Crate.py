import pygame
import os

# File Management and Initialization
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Game Thingy mabob')

# Constants
GL = 600  # Ground level
MAP_WIDTH = 1200
MAP_HEIGHT = 800
GRAVITY = 0.5

class Crate(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, crate_break_sound, score):
        super().__init__()
        self.idle_sprite = pygame.image.load('crate_idle.png')
        self.broke_sprites = [
            pygame.image.load(f'crate_{i}.png') for i in range(2)  # Assuming 2 frames of broken crate
        ]
        self.current_sprite = 0
        self.image = self.idle_sprite  # Initial idle state
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.crate_break_sound = crate_break_sound
        self.sound_played = False  # Ensure sound plays only once
        self.score = score

        # State variables
        self.broken = False
        self.animating = False
        self.animation_finished = False  # Track when the animation finishes
        self.last_update_time = pygame.time.get_ticks()
        self.stand_start_time = None  # When the player started standing on the crate

    def update(self):
        current_time = pygame.time.get_ticks()

        # Handle starting the break animation after stand time is reached
        if self.stand_start_time and not self.broken:
            if current_time - self.stand_start_time >= 3000:  # how ever many seconds
                self.broken = True
                self.animating = True

        # Handle broken animation if animating (i.e., crate is breaking)
        if self.animating and not self.animation_finished:
            if current_time - self.last_update_time > 100:  # 100ms between frames
                self.current_sprite += 1  # Move to the next frame
                self.last_update_time = current_time

                if self.current_sprite >= len(self.broke_sprites):
                    self.animation_finished = True  # Mark animation as finished
                    self.image = pygame.Surface((0, 0))  # Make crate invisible
                    self.kill()  # Remove crate from the game
                else:
                    # Update the sprite to the current frame
                    self.image = self.broke_sprites[self.current_sprite]

            if not self.sound_played:
                self.crate_break_sound.play()
                self.sound_played = True

    def interact(self, player):
        # Check collision and start timer on first collision
        if player.rect.colliderect(self.rect) and not self.broken and not self.animating:
            player.rect.bottom = self.rect.top  # Sit the player on top of the crate
            player.velocity_y = 0
            player.is_jumping = False
            player.on_crate = True  # Set player state to on crate

            # Start the timer if the player first lands on the crate
            if self.stand_start_time is None:
                self.stand_start_time = pygame.time.get_ticks()
        else:
            # Reset player state if they are not on the crate anymore
            player.on_crate = False
