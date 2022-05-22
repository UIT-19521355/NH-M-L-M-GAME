import pygame
import math

class Bullet:
    '''This class is used to hold Bullets data and also is used to create the bullet and update to the screen'''
    def __init__(self, pos, angle, size, speed):
        '''This function creates fundamental infomations
        
        Input
        -----
        pos:
            position of the bullet before shooting
        angle:
            angle when shooting the bullet depend on axis of coordinate X and Y
        size:
            the size of bullets
        speed:
            the speed of bullets
        Attributes:
            self.speed : apply speed
            self.directionx : calculated the way of bullets move with x axis 
            self.directiony : calculated the way of bullets move with y axis
            self.rect : create the bullet 

        Output
        ------
        the bullet after shooted fly with correct calculated shooting's way
        '''
        self.speed = speed
        self.directionx = math.cos(math.radians(angle))
        self.directiony = math.sin(math.radians(angle))
        self.rect = pygame.Rect(pos, size)
    
    def update(self):
        '''Update calculated coordinate before displaying on the screen
        
        Input:
        -----
        None

        Output:
        ------
        New coordinate for each frame make bullet like moving
        '''
        self.rect.x += self.directionx * self.speed
        self.rect.y -= self.directiony * self.speed