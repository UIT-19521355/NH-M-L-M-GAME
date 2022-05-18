import math
import pygame
import random



class Powerup:
    '''This class is used to hold the fundamental Powerup infos'''
    def __init__(self, pos, width, height, surface, index):
        '''Fundamental infos'''
        self.index = index
        self.pos = pos
        self.width = width
        self.height = height
        self.sin = 0
        self.sin_amplitude = 0.3
        self.sin_frequency = 5
        self.surface = surface
        self.rect = pygame.Rect(pos.x, pos.y, width, height)
        self.y = self.rect.y

    def update(self):
        self.sin += 0.017
        self.y += math.sin(self.sin * self.sin_frequency) * self.sin_amplitude
        self.rect.y = self.y

        