import pygame
from Enemy import Enemy

class Enemy3(Enemy):
    GUN_WIDTH, GUN_HEIGHT = 35, 35
    GUN_OFFSET_X, GUN_OFFSET_Y = 17, 17

    BULLET_WIDTH, BULLET_HEIGHT = 10, 10
    BULLET_SPEED = 7

    USER_EVENT = pygame.USEREVENT + 3

    gun_fire_rate = 0.1
    time_before_shoot = 2

    speed = 0.5
    previous_pos_x = 0
    previous_pos_y = 0

    health = 20

    index = 2