import pygame
import sys

#---------------------------------------------------------------------------------------------------------
# Game setup 
#---------------------------------------------------------------------------------------------------------
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

#BG pic test
background_image = pygame.image.load("E:/chuditchwerkroom/2024_Werkroom/0000_CDU/2024_CDU/2024 SEM 2/HIT137/Assignment 3/Pygame_working files/Lemon Guy/background2.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale it to fit the screen

#----------------------------------------------------------------------------------------------------------------
# Game audio
#----------------------------------------------------------------------------------------------------------------

# Load audio mp3
footstep_sound = pygame.mixer.Sound("E:/chuditchwerkroom/2024_Werkroom/0000_CDU/2024_CDU/2024 SEM 2/HIT137/Assignment 3/Pygame_working files/Lemon Guy/Lemonsquash.mp3")
footstep_sound.set_volume(0.05)  # Set to % volume

#----------------------------------------------------------------------------------------------------------------
# Font
#----------------------------------------------------------------------------------------------------------------

# Font for the warning message
font = pygame.font.SysFont(None, 30)

#----------------------------------------------------------------------------------------------------------------
# Game Sprite_The Hero_Lemon Guy
#----------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('E:/chuditchwerkroom/2024_Werkroom/0000_CDU/2024_CDU/2024 SEM 2/HIT137/Assignment 3/Pygame_working files/Lemon Guy/LG_walk_side0.png'))
        self.sprites.append(pygame.image.load('E:/chuditchwerkroom/2024_Werkroom/0000_CDU/2024_CDU/2024 SEM 2/HIT137/Assignment 3/Pygame_working files/Lemon Guy/LG_walk_side1.png'))
        self.sprites.append(pygame.image.load('E:/chuditchwerkroom/2024_Werkroom/0000_CDU/2024_CDU/2024 SEM 2/HIT137/Assignment 3/Pygame_working files/Lemon Guy/LG_walk_side2.png'))

        # Load the idle sprite image (replace the path with your actual image path)
        self.idle_sprite = pygame.image.load('E:/chuditchwerkroom/2024_Werkroom/0000_CDU/2024_CDU/2024 SEM 2/HIT137/Assignment 3/Pygame_working files/Lemon Guy/LG_walk_side2.png')
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        if moving:
            # Handle animation here
            self.current_sprite += 0.1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
        #Stop walking 
        else:
            self.image = self.idle_sprite  # Set to idle sprite when not moving

# Creating sprite group and player
moving_sprites = pygame.sprite.Group()
player = Player(400, 200)
moving_sprites.add(player)

# Define footstep sound
sprite_speed = 8
footstep_delay = 500  # milliseconds (time between footstep sounds)
last_footstep_time = 0  # Initialize last footstep sound time

# Initialize the moving variable globally
moving = False

#----------------------------------------------------------------------------------------------------------------
# Main game loop
#----------------------------------------------------------------------------------------------------------------

run = True
facing_right = True  # Initialize the facing direction

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Check for key press events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Pause the game on Esc
                # Define this function or remove it
                pass

                # Check for key release events (added section)
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                moving = False  # Stop moving when any direction key is released
      

    # Handle key movement
    keys = pygame.key.get_pressed()
    moving = False  # Reset moving status each frame
    if keys[pygame.K_LEFT]:
        player.rect.x -= sprite_speed
        moving = True
        facing_right = False  # Face left
    if keys[pygame.K_RIGHT]:
        player.rect.x += sprite_speed
        moving = True
        facing_right = True  # Face right
    if keys[pygame.K_UP]:
        player.rect.y -= sprite_speed
        moving = True
    if keys[pygame.K_DOWN]:
        player.rect.y += sprite_speed
        moving = True

    # Play footstep sound if moving and enough time has passed
    if moving:
        current_time = pygame.time.get_ticks()
        if current_time - last_footstep_time > footstep_delay:
            footstep_sound.play()
            last_footstep_time = current_time

    # Game logic and drawing code here
    screen.fill((0, 0, 0))  # Clear the screen during normal game operation

    # Draw the background image
    screen.blit(background_image, (0, 0))  # Draw the background at (0, 0)

    # Update the player's state (animation)
    player.update()

    # Draw the flipped or original sprite based on the facing direction
    if facing_right:
        screen.blit(player.image, player.rect)  # Draw normal sprite
    else:
        flipped_image = pygame.transform.flip(player.image, True, False)
        screen.blit(flipped_image, player.rect)  # Draw flipped sprite

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit the frame rate to 60 FPS

# Quit Pygame
pygame.quit()
