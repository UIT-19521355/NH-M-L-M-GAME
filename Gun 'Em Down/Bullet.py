import pygame
import math

class Bullet:
    '''This class is used to hold Bullet data.
    Two function below is used to create the fundamental of bullet and update to screen'''
    def __init__(self, pos, angle, size, speed):
        '''Fundamental infomations'''
        self.speed = speed
        self.directionx = math.cos(math.radians(angle))
        self.directiony = math.sin(math.radians(angle))

        self.rect = pygame.Rect(pos, size)
    
    def update(self):
        '''Update to screen'''
        self.rect.x += self.directionx * self.speed
        self.rect.y -= self.directiony * self.speed