import pygame
import random

class Collectable(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, points):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.points = points

    def collect(self):
        """Returns the points when the collectable is collected."""
        return self.points

    @staticmethod
    def create_collectables(collectable_info, image_width, ground_level, max_jump_height):
        collectable_group = pygame.sprite.Group()
        
        # Loop through the collectable_info to create collectables
        for info in collectable_info:
            num_collectables = info['count']
            image_path = info['image']
            points = info['points']
            
            for _ in range(num_collectables):
                # Random x position across the entire image width
                x = random.randint(0, image_width - 50)  # Offset to avoid out-of-bound placement
                
                # Random y position in the jumpable range (above the ground but below max_jump_height)
                y = random.randint(ground_level - max_jump_height, ground_level - 50)  # Offset to place it above the ground
                
                # Create and add collectable to the group
                collectable = Collectable(x, y, image_path, points)
                collectable_group.add(collectable)
        
        return collectable_group
