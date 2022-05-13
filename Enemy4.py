import pygame
from Enemy import Enemy

class Enemy4(Enemy):
    GUN_WIDTH, GUN_HEIGHT = 40, 40
    GUN_OFFSET_X, GUN_OFFSET_Y = 25, 25

    BULLET_WIDTH, BULLET_HEIGHT = 6, 6
    BULLET_SPEED = 7

    USER_EVENT = pygame.USEREVENT + 4

    gun_fire_rate = 2.5
    time_before_shoot = 2

    speed = 0.8
    previous_pos_x = 0
    previous_pos_y = 0

    health = 200

    index = 3