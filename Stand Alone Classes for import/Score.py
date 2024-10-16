import pygame

class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points):
        self.points += points

    def display_score(self, screen, font):
        score_text = font.render(f'Score: {self.points}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
