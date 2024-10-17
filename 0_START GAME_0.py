import pygame
import os
import sys
import subprocess

pygame.init()
clock = pygame.time.Clock()

# Set working directory to where the script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ----------------------------------------------------------------------------------------------------------------
#Initialise game screen
# ----------------------------------------------------------------------------------------------------------------

# Screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Greatest Game...")

# ----------------------------------------------------------------------------------------------------------------
# Load Lemon Guy
# ----------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('LG_walk_side0.png'))
        self.sprites.append(pygame.image.load('LG_walk_side1.png'))
        self.sprites.append(pygame.image.load('LG_walk_side2.png'))
        self.idle_sprite = pygame.image.load('LG_FrontStanding.png')
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self):
        global moving
        if moving:
            self.current_sprite += 0.1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
        else:
            self.image = self.idle_sprite  # Set to idle sprite when not moving

# Creating sprite group and player
moving_sprites = pygame.sprite.Group()
player = Player(400, 500)
moving_sprites.add(player)

# Define footstep sound
sprite_speed = 8
footstep_delay = 1000  # milliseconds (time between footstep sounds)
last_footstep_time = 0  # Initialize last footstep sound time

moving = False
movement_frame_limit = 37

# Load the sequence for animations
Game_opening_sequence = [pygame.transform.scale(pygame.image.load(f"BG_{i}.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)) for i in range(1, 49)]
BG_userinput = pygame.transform.scale(pygame.image.load("BG_47.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load audio
Themesong = pygame.mixer.Sound("Theme.WAV")
Themesong.set_volume(1.0)

footstep_sound = pygame.mixer.Sound('Lemonsquash.mp3')
footstep_sound.set_volume(0.4)

# Font and colors
font = pygame.font.SysFont(None, 30)
input_font = pygame.font.Font(None, 100)
Lemon_Blue = (41, 148, 214)
Lemon_Yellow = (244, 208, 12)
BLACK = (0, 0, 0)

user_name = ''

# ----------------------------------------------------------------------------------------------------------------
# Game functions
# ----------------------------------------------------------------------------------------------------------------
    
def Game_Opening():
    global moving, last_footstep_time, facing_right
    animation_done = False
    facing_right = True
    
    frame_background = 0
    Themesong.play()
    
    background_delay = 1000  # Background frame change delay
    player_delay = 10       # Delay between player sprite updates (in ms)
    footstep_delay = 1000     # Delay for footstep sound in ms
    hide_frame = 37          # Frame where Lemon Guy disappears
    start_ticks_background = pygame.time.get_ticks()
    start_ticks_player = pygame.time.get_ticks()

    while not animation_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update the screen with the current background frame
        screen.blit(Game_opening_sequence[frame_background], (0, 0))

        # Update background frame based on time
        if pygame.time.get_ticks() - start_ticks_background > background_delay:
            frame_background += 1
            start_ticks_background = pygame.time.get_ticks()

        # Handle player movement and animation
        if frame_background < movement_frame_limit and frame_background < hide_frame:
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_a]:
                player.rect.x -= sprite_speed
                moving = True
                facing_right = False
            elif keys[pygame.K_d]:
                player.rect.x += sprite_speed
                moving = True
                facing_right = True
            else:
                moving = False

            # Ensure player stays within screen bounds
            player.rect.x = max(0, min(player.rect.x, SCREEN_WIDTH - player.image.get_width()))

            # Update player sprite animation and footstep sound
            if moving:
                # Animate player sprite if enough time has passed
                if pygame.time.get_ticks() - start_ticks_player > player_delay:
                    player.update()  # Call player sprite's update method for animation
                    start_ticks_player = pygame.time.get_ticks()
                
                # Play footstep sound with delay
                if pygame.time.get_ticks() - last_footstep_time > footstep_delay:
                    footstep_sound.play()
                    last_footstep_time = pygame.time.get_ticks()

        # Draw player sprite based on movement state
        if frame_background < hide_frame:
            if moving:
                if facing_right:
                    screen.blit(player.image, player.rect)
                else:
                    flipped_image = pygame.transform.flip(player.image, True, False)
                    screen.blit(flipped_image, player.rect)
            else:
                screen.blit(player.idle_sprite, player.rect)

        pygame.display.update()
        clock.tick(60)  # Control the frame rate

        if frame_background >= len(Game_opening_sequence):
            animation_done = True

    return True

def get_name_input():
    global user_name
    input_active = True
    while input_active:
        screen.blit(BG_userinput, (0, 0))
        prompt_text = font.render("You can type your name right?", True, Lemon_Yellow)
        screen.blit(prompt_text, (400, 320))
        user_input_text = input_font.render(user_name, True, Lemon_Blue)
        screen.blit(user_input_text, (350, 400))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                    with open("player_name.txt", "w") as f:
                        f.write(user_name)  
                    print(f"Player name saved: {user_name}")  # Debug print              
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    user_name += event.unicode

    # Launch the Tkinter script using subprocess
    try:
        pygame_script = os.path.join(os.getcwd(), "0_TKINTER COLLECTABLE GENERATOR_0.py")
        print(f"Launching Tkinter script: {pygame_script}")  # Debug print
        subprocess.Popen(["python", pygame_script])  # Use Popen instead of run
        print("Tkinter script launched successfully!")  # Debug print
    except Exception as e:
        print(f"Error launching Tkinter script: {e}")  # Debug print

# Main Game loop
def main_game():
    running = True
    current_state = 'animation'

    while running:
        if current_state == "animation":
            animation_completed = Game_Opening()
            if animation_completed:
                current_state = "input"

        elif current_state == "input":
            get_name_input()
            running = False  # Stop the game loop after running Tkinter

    pygame.quit()

# Start the game
main_game()
