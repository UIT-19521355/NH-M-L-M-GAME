import pygame
from Enemy import Enemy

class Enemy2(Enemy):
    '''This class inherited from Enemy class'''
    GUN_WIDTH, GUN_HEIGHT = 25, 25
    GUN_OFFSET_X, GUN_OFFSET_Y = 12, 12

    BULLET_WIDTH, BULLET_HEIGHT = 5, 5
    BULLET_SPEED = 5

    USER_EVENT = pygame.USEREVENT + 2

    gun_fire_rate = 2
    time_before_shoot = 1

    speed = 2
    previous_pos_x = 0
    previous_pos_y = 0

    health = 8

    index = 1