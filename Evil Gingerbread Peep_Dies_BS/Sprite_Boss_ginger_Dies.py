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
pygame.display.set_caption("The Greatest Game that Three Heroic Learners Ever Imagined with a lemon-headed friend...")

# BG pic test
background_image = pygame.image.load("background4.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale it to fit the screen

#----------------------------------------------------------------------------------------------------------------
# Game audio
#----------------------------------------------------------------------------------------------------------------

# Load audio mp3
footstep_sound = pygame.mixer.Sound('Boohoo.mp3')
footstep_sound.set_volume(2)  # Set to % volume

#----------------------------------------------------------------------------------------------------------------
# Font
#----------------------------------------------------------------------------------------------------------------

# Font for the warning message
font = pygame.font.SysFont(None, 30)

#----------------------------------------------------------------------------------------------------------------
# Game Sprite_Final Boss_Ginger Peep
#----------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 0.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 1.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 2.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 3.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 4.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 5.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 6.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 8.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 8.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 8.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 8.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))   
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 8.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 7.png'))   
        self.sprites.append(pygame.image.load('B_ging_Sprite Die 8.png'))

        # Load the idle sprite image (replace the path with your actual image path)
        self.idle_sprite = pygame.image.load('B_ging_Sprite Die 0.png')
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        self.animation_speed = 20  # The number of frames between sprite updates
        self.frame_count = 0  # Counter to control animation speed
        self.animation_done = False  # To track if the animation is completed
        self.animation_active = False  # To control when the animation plays

    def update(self):
        if self.animation_active and not self.animation_done:  # Only update if animation is active
            self.frame_count += 1
            if self.frame_count >= self.animation_speed:
                self.frame_count = 0
                self.current_sprite += 1

                # If the animation reaches the end, stop updating
                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = len(self.sprites) - 1  # Set to last frame
                    self.animation_done = True  # Mark the animation as done
                    self.animation_active = False  # Stop the animation after playing once

                self.image = self.sprites[self.current_sprite]

    def start_animation(self):
        self.animation_active = True  # Start the animation
        self.animation_done = False  # Reset the animation state
        self.current_sprite = 0  # Reset to the first frame
        footstep_sound.play()  # Play sound when animation starts

#----------------------------------------------------------------------------------------------------------------
# Initialize the player sprite
#----------------------------------------------------------------------------------------------------------------

player = Player(400, 170)

#----------------------------------------------------------------------------------------------------------------
# Main game loop
#----------------------------------------------------------------------------------------------------------------

run = True  # Initialize the 'run' variable

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Check for key press to start animation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Start animation when the spacebar is pressed
                player.start_animation()  # Start the animation

    # Game logic and drawing code here
    screen.fill((0, 0, 0))  # Clear the screen during normal game operation

    # Draw the background image
    screen.blit(background_image, (0, 0))  # Draw the background at (0, 0)

    # Update the player's state (animation)
    player.update()

    # Draw the player sprite
    screen.blit(player.image, player.rect)

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit the frame rate to 60 FPS

# Quit Pygame
pygame.quit()
