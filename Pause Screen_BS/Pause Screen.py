import pygame
import math

pygame.init()

#keys needed
from pygame.locals import (
    K_ESCAPE,
    K_RETURN,
    QUIT,
    KEYDOWN,
)

#----------------------------------------------------------------------------------------------------------------
#Game Screen load
#----------------------------------------------------------------------------------------------------------------

#Screen size_RGB_PNG8
#For alpha transparency, like in . png images, use the pygame. Surface. convert_alpha() change the pixel format of an image including per pixel alphas method after loading so that the image has per pixel transparency.

#Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Greatest Game that Three Heroic Learners Ever Imagined with a lemon headed friend...")

#----------------------------------------------------------------------------------------------------------------
#Game graphics
#----------------------------------------------------------------------------------------------------------------
# Load the background image
pause_image = pygame.image.load('BGpause.png')
pause_image = pygame.transform.scale(pause_image, (1000,700))  # Scale image to screen size

# Load the transparenvy for alert text
transparency_image = pygame.image.load('Transparency_alpha.png')
transparency_image = pygame.transform.scale(transparency_image, (800,500))  # Scale image to screen size
transparency_image.set_alpha(230)  # Set the alpha for transparency (0-255; 255 is fully opaque)

#----------------------------------------------------------------------------------------------------------------
#Game audio
#----------------------------------------------------------------------------------------------------------------

# Load audio mp3
pause_sound = pygame.mixer.Sound("pause.WAV") 

#----------------------------------------------------------------------------------------------------------------
#Font
#----------------------------------------------------------------------------------------------------------------

# Font for the warning message
font = pygame.font.SysFont(None, 30)

#----------------------------------------------------------------------------------------------------------------
#Game functons
#----------------------------------------------------------------------------------------------------------------

#Pause Screen Layout
def display_pause_message():
    screen.fill((0, 0, 0))  # Clear the screen
    screen.blit(pause_image, (0, 0))  # Blit it at the top-left corner
    screen.blit(transparency_image, (100, 100))  # Blit it at the top-left corner

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
    base_y = screen_rect.centery - 200  # Adjust the starting height here

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

            elif event.key == pygame.K_RETURN:  # Press Enter to resume the game
                    paused = False

        display_pause_message()

# Game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Check for key press events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Pause the game on Esc
                pause_game()

    # Game logic and drawing code here
    screen.fill((0, 0, 0))  # Clear the screen during normal game operation
    pygame.display.flip()