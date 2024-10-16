import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, ground_level):
        super().__init__()
        self.sprites = [
            pygame.image.load('LG_walk_side0.png'),
            pygame.image.load('LG_walk_side1.png'),
            pygame.image.load('LG_walk_side2.png')
        ]
        # Store pre-flipped sprites for left-facing direction
        self.flipped_sprites = [pygame.transform.flip(sprite, True, False) for sprite in self.sprites]

        self.idle_sprite = pygame.image.load('LG_walk_side2.png')
        self.flipped_idle_sprite = pygame.transform.flip(self.idle_sprite, True, False)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

        # Movement variables
        self.is_jumping = False
        self.jump_speed = -25  # Jump height
        self.gravity = 1
        self.velocity_y = 0

        # Ground level settings
        self.ground_level = ground_level  # Set dynamically
        self.original_ground_level = ground_level  # Store the original ground level
        self.rect.bottom = self.ground_level  # Start on the ground
        print(f"Initial player bottom: {self.rect.bottom}, Ground level: {self.ground_level}")

        self.sprite_speed = 4
        self.facing_right = True

    def update(self):
        keys = pygame.key.get_pressed()
        moving = False

        # Handle movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.sprite_speed
            moving = True
            if self.facing_right:  # If facing right, flip to left
                self.facing_right = False
                self.current_sprite = 0  # Reset sprite animation
            self.image = self.flipped_sprites[int(self.current_sprite)]  # Use left-facing sprites

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.sprite_speed
            moving = True
            if not self.facing_right:  # If facing left, flip to right
                self.facing_right = True
                self.current_sprite = 0  # Reset sprite animation
            self.image = self.sprites[int(self.current_sprite)]  # Use right-facing sprites

        # Animate the player if moving
        if moving:
            self.current_sprite += 0.1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            # Update the correct sprite depending on direction
            if self.facing_right:
                self.image = self.sprites[int(self.current_sprite)]
            else:
                self.image = self.flipped_sprites[int(self.current_sprite)]
        else:
            # Set the idle sprite depending on direction
            if self.facing_right:
                self.image = self.idle_sprite
            else:
                self.image = self.flipped_idle_sprite

        # Apply gravity
        if self.is_jumping or self.rect.bottom < self.ground_level:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            # Check if the player has landed
            if self.rect.bottom >= self.ground_level:
                self.rect.bottom = self.ground_level
                self.velocity_y = 0
                self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_speed
            print(f"Player jumps with velocity: {self.velocity_y}")
