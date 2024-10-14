import pygame
import math

class Enemy_bird(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, damage):
        super().__init__()
        self.frames = [
            pygame.image.load('bird_0.png').convert_alpha(),
            pygame.image.load('bird_1.png').convert_alpha()
        ]
        self.frames = [pygame.transform.scale(frame, (width, height)) for frame in self.frames]
        self.current_frame = 0
        self.animation_counter = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.damage = damage
        self.health = 100  # Health of the enemy
        self.start_x = x
        self.start_y = y
        self.movement_speed = 2
        self.movement_counter = 0
        self.falling = False
        self.fall_distance = 0

    def update(self):
        if self.health > 0:
            # Animate the bird
            self.animation_counter += 1
            if self.animation_counter >= 10:  # Change frame every 10 updates
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                self.animation_counter = 0

            # Move the enemy in a W shape
            self.movement_counter += 1
            self.rect.x = self.start_x + math.sin(self.movement_counter * 0.05) * 100
            self.rect.y = self.start_y + math.sin(self.movement_counter * 0.1) * 50
        elif self.falling:
            # Make the bird fall when deadibones
            self.rect.y += 5
            self.fall_distance += 5
            if self.fall_distance >= 300:
                self.kill()

    def deal_damage(self, player):
        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.image = pygame.image.load('bird_dead.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            self.falling = True
