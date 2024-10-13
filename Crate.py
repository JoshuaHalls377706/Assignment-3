import pygame

crate_animation_speed = 0.8
STAND_TIME_BEFORE_ANIMATING = 1000  # Time before the crate breaks after standing on it
GL = 600

class Crate(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, crate_break_sound, score):
        super().__init__()
        self.idle_sprite = pygame.image.load('crate_idle.png')  # Crate before broken
        self.broke_sprites = [
            pygame.image.load(f'crate_{i}.png') for i in range(2)  # Load broken frames
        ]
        self.current_sprite = 0
        self.image = self.idle_sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.crate_break_sound = crate_break_sound
        self.score = score

        # Crate state variables
        self.player_on_crate = False
        self.arming = False
        self.broken = False
        self.broke_done = False
        self.start_time_on_crate = None  # Timer for breaking
        self.last_update_time = pygame.time.get_ticks()  # To manage animation timing

    def update(self):
        current_time = pygame.time.get_ticks()

        # Handle broken animation
        if self.broken and not self.broke_done:
            # Only update animation if enough time has passed
            if current_time - self.last_update_time > 100:  # Update every 100ms
                self.current_sprite += crate_animation_speed  # Advance through the broken frames
                self.last_update_time = current_time  # Reset last update time
                if int(self.current_sprite) >= len(self.broke_sprites):
                    self.broke_done = True  # Animation is complete
                    self.crate_break_sound.play()
                    print("Crate has fully broken.")
                    self.score.increment(50)  # Increment the score linked to the main game

                    # Set the crate's image to a transparent or broken state
                    self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                    self.image.fill((0, 0, 0, 0))  # Fully transparent surface
                    # Remove the collision rectangle to avoid player standing on it
                    self.rect.height = 0
                    self.rect.width = 0
                else:
                    self.image = self.broke_sprites[int(self.current_sprite)]

    def interact(self, player):
        # Only check for collision if the crate is not broken
        if player.rect.colliderect(self.rect) and not self.broken and not self.broke_done and player.velocity_y > 0:
            # Player lands on crate
            player.rect.bottom = self.rect.top
            player.velocity_y = 0
            player.is_jumping = False
            player.ground_level = self.rect.top
            self.player_on_crate = True

            # Start timer if not started and break crate if elapsed time exceeds threshold
            if self.start_time_on_crate is None:
                self.start_time_on_crate = pygame.time.get_ticks()

            if pygame.time.get_ticks() - self.start_time_on_crate >= STAND_TIME_BEFORE_ANIMATING:
                self.arming = True
                self.broken = True


class SolidCrate(Crate):
    def __init__(self, pos_x, pos_y, crate_break_sound, score):
        super().__init__(pos_x, pos_y, crate_break_sound, score)
        self.idle_sprite = pygame.image.load('static_crate.png')
        self.image = self.idle_sprite 
        self.broken = False  # Solid crate does not break

    def update(self):
        self.image = self.idle_sprite
        self.broken = False  # This crate does not break

def check_player_crate_collision(player, crate):
    # Only check for collision if the crate is not broken
    if player.rect.colliderect(crate.rect) and not crate.broken and not crate.broke_done and player.velocity_y > 0:
        # Player lands on crate
        player.rect.bottom = crate.rect.top
        player.velocity_y = 0
        player.is_jumping = False
        player.ground_level = crate.rect.top
        crate.player_on_crate = True

        # Start timer if not started and break crate if elapsed time exceeds threshold
        if crate.start_time_on_crate is None:
            crate.start_time_on_crate = pygame.time.get_ticks()

        if pygame.time.get_ticks() - crate.start_time_on_crate >= STAND_TIME_BEFORE_ANIMATING:
            crate.arming = True
            crate.broken = True

        return True

    return False


class SolidCrate(Crate):
    def __init__(self, pos_x, pos_y, crate_break_sound, score):
        super().__init__(pos_x, pos_y, crate_break_sound, score)
        self.idle_sprite = pygame.image.load('static_crate.png')
        self.image = self.idle_sprite 
        self.broken = False  # Solid crate does not break

    def update(self):
        self.image = self.idle_sprite
        self.broken = False  # This crate does not break
 





