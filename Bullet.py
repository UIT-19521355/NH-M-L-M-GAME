import pygame
import math

class Bullet:
    def __init__(self, pos, angle, size, speed):
        self.speed = speed
        self.directionx = math.cos(math.radians(angle))
        self.directiony = math.sin(math.radians(angle))

        self.rect = pygame.Rect(pos, size)
    
    def update(self):
        self.rect.x += self.directionx * self.speed
        self.rect.y -= self.directiony * self.speed