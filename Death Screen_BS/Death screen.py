import pygame
import os

pygame.init()

# ----------------------------------------------------------------------------------------------------------------
# Game Screen load
# ----------------------------------------------------------------------------------------------------------------

# Set working directory to where the script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Greatest Game that Three Heroic Learners Ever Imagined with a lemon headed friend...")

# ----------------------------------------------------------------------------------------------------------------
# Game graphics
# ----------------------------------------------------------------------------------------------------------------
# Load the death sequence for animation
you_died = [pygame.transform.scale(pygame.image.load(f"LG_die_{i}.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)) for i in range(0, 15)]
you_died_options = pygame.transform.scale(pygame.image.load("LG_die_15.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))


# ----------------------------------------------------------------------------------------------------------------
# Game audio
# ----------------------------------------------------------------------------------------------------------------

# Load audio mp3
Lastwords = pygame.mixer.Sound("LGQuote_End Game.mp3")
Lastwords.set_volume(5)  # Set to % volume

# ----------------------------------------------------------------------------------------------------------------
# Font
# ----------------------------------------------------------------------------------------------------------------

# Font for the warning message
font = pygame.font.SysFont(None, 30)

# ----------------------------------------------------------------------------------------------------------------
# Game functions
# ----------------------------------------------------------------------------------------------------------------

# You Died Screen Layout
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
                    return False  # Resume the game and restart

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


# Main Game loop
def main_game():
    death = False  # Player starts alive

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not death:  # Trigger death only if alive
                    death = True  # Set death to True when player dies
                    death = your_dead()  # Run death sequence

                elif event.key == pygame.K_RETURN and not death:  # Restart Game
                    death = False  # Reset death state and restart

                elif event.key == pygame.K_ESCAPE:  # Quit exit game window
                    run = False

        # Game logic and drawing code here
        if not death:
            screen.fill((0, 0, 0))  # Clear the screen during normal game operation

        pygame.display.flip()

    pygame.quit()


# Start the game
if __name__ == "__main__":
    main_game()
