import pygame, sys

#---------------------------------------------------------------------------------------------------------
#Game setup 
#---------------------------------------------------------------------------------------------------------
pygame.init()
clock = pygame.time.Clock()

#----------------------------------------------------------------------------------------------------------------
#Game Screen load
#----------------------------------------------------------------------------------------------------------------

# Screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Greatest Game that Three Heroic Learners Ever Imagined with a lemon headed friend...")

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
#Game Sprite_The Hero_Lemon Guy
#----------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('LG_walk_side0.png'))
        self.sprites.append(pygame.image.load('LG_walk_side1.png'))
        self.sprites.append(pygame.image.load('LG_walk_side2.png'))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # Corrected: get_rect() instead of get_rec()
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        # Handle animation here (optional)
        self.current_sprite += 0.1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

# Creating sprite group and player
moving_sprites = pygame.sprite.Group()
player = Player(400, 200)
moving_sprites.add(player)

#----------------------------------------------------------------------------------------------------------------
# Main game loop
#----------------------------------------------------------------------------------------------------------------
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

    # Update and draw the sprite group
    moving_sprites.update()  # Update the state of the sprites (if necessary)
    moving_sprites.draw(screen)  # Draw the sprites onto the screen

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit the frame rate to 60 FPS
