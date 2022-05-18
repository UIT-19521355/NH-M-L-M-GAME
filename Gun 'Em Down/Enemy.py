import pygame
import math
import random
from EnemyBullet import EnemyBullet

class Enemy:
    "This class is used to hold the enemies infos and create enemies"
    GUN_WIDTH, GUN_HEIGHT = 30, 30
    GUN_OFFSET_X, GUN_OFFSET_Y = 15, 15

    BULLET_WIDTH, BULLET_HEIGHT = 5, 5
    BULLET_SPEED = 5

    USER_EVENT = pygame.USEREVENT + 1

    gun_fire_rate = 0.2
    time_before_shoot = 1

    speed = 1
    previous_pos_x = 0
    previous_pos_y = 0

    health = 10

    index = 0



    def __init__(self, pos, size, surface, obstacles, gun_image):
        '''Fundamental infos
        
        Input:
        -----
        pos:
            position of the enemy
        size:
            size of the enemy
        surface:
            the Pygame's window which is the place will display enemies
        obstacles:
            the obstacles display on surface
        gun_image:
            the gun image
        
        Output:
        ------
        The enemy with gun attach to it

        '''
        self.main_surface = surface
        self.surface = surface
        self.rect = pygame.Rect(pos, size)
        self.obstacles = obstacles

        self.gun = pygame.transform.rotate(pygame.transform.scale(gun_image, (self.GUN_WIDTH, self.GUN_HEIGHT)), -90) # SCALED AND ROTATED
        self.gun_rotated = 0
        self.gun_rotated_rect = 0

        self.bullets = []

        self.x = pos[0]
        self.y = pos[1]
        self.gun_x = 0
        self.gun_y = 0

        self.shoot_particles = []
        self.shoot_particle_colors = [(255, 0, 0), (255, 215,0), (255, 69, 0)]

    def handle_collisions(self, player_rect):
        '''Use this function to handle the collision
        
        Input:
        -----
        player_rect:
            the player
        
        Output:
        ------
        the bullet will disappear after touching the obstacle 
        '''
        # COLLISIONS ON OBSTACLES
        for obstacle in self.obstacles:
            if self.rect.colliderect(obstacle):
                if math.isclose(obstacle.right, self.rect.left, abs_tol=3) or math.isclose(obstacle.left, self.rect.right, abs_tol=3):
                    self.x = self.previous_pos_x
                elif math.isclose(obstacle.top, self.rect.bottom, abs_tol=3) or math.isclose(obstacle.bottom, self.rect.top, abs_tol=3):
                    self.y = self.previous_pos_y
                else:
                    self.x = self.previous_pos_x
                    self.y = self.previous_pos_y


    def update_move_rot(self, player_rect):
        '''This function is used to make Player's shoot direction follow mouse's direction
        And also calculated the movement of the player
        
        Input:
        player_rect:
            the player

        Output:
        The player will be attached with a gun. The gun moving , rotate same as player
        '''
        self.previous_pos_x = self.x
        self.previous_pos_y = self.y

        dir = pygame.Vector2(player_rect.x - self.rect.x, self.rect.y - player_rect.y)

        if dir != pygame.Vector2(0, 0):        
            angle = math.degrees(math.atan2(dir.y, dir.x))

            # GUN ROT
            self.gun_rotated = pygame.transform.rotate(self.gun, angle)
            self.gun_rotated_rect = self.gun_rotated.get_rect(center = self.rect.center)

            self.gun_x = pygame.Vector2.dot(pygame.Vector2(0, 1), pygame.Vector2(dir.x, dir.y).normalize())
            self.gun_y = pygame.Vector2.dot(pygame.Vector2(1, 0), pygame.Vector2(dir.x, dir.y).normalize())
            self.gun_rotated_rect.x += self.GUN_OFFSET_X * self.gun_x
            self.gun_rotated_rect.y += self.GUN_OFFSET_Y * self.gun_y


            # MOVE PLAYER
            self.move_dirx = math.cos(math.radians(angle))
            self.move_diry = math.sin(math.radians(angle))

            self.x += self.move_dirx * self.speed
            self.y -= self.move_diry * self.speed
            self.rect.x = self.x
            self.rect.y = self.y


            # ROTATING PLAYER
            rot_angle = angle - 90

            self.surface = pygame.transform.rotate(self.main_surface, rot_angle)
            self.rotated_rect = self.surface.get_rect(center = self.rect.center)

    def update_gun(self, player_rect):
        '''This function is used to update the shooting
        
        Input:
        player_rect:
            The player
        
        Output:
        the bullet will come out at the coordinate of the gun and also it has deplay for each shoot
        '''
        if self.time_before_shoot <= 0:
            # SHOOT
            shoot_dir_x, shoot_dir_y = player_rect.centerx - self.gun_rotated_rect.x, self.gun_rotated_rect.y - player_rect.centery
            shoot_angle = math.degrees(math.atan2(shoot_dir_y, shoot_dir_x))

            self.bullets.append(EnemyBullet((self.gun_rotated_rect.centerx, self.gun_rotated_rect.centery), shoot_angle, (self.BULLET_WIDTH, self.BULLET_HEIGHT), self.BULLET_SPEED))

            self.time_before_shoot = 1 / self.gun_fire_rate
        else:
            self.time_before_shoot -= 0.017
    
    def update_bullets(self, obstacles, WIDTH, HEIGHT, player_rect):
        '''This function is used to make the bullet disappear after a collision
        
        Input:
        -----
        obstacles:
            the obstacle display on the pygame's screen
        WIDTH:
            the width of the pygame's screen
        HEIGHT:
            the height of the Pygame's screen
        player_rect:
            the player
        
        Output:
        ------
        After a collision with obstacle , it disappear
        '''
        bullet_to_remove = 0

        for bullet in self.bullets:
            bullet.update()
            for obstacle in obstacles:
                if bullet.rect.x >= WIDTH or bullet.rect.x <= 0 or bullet.rect.y >= HEIGHT or bullet.rect.y <= 0:
                    bullet_to_remove = bullet
                elif bullet.rect.colliderect(obstacle):
                    bullet_to_remove = bullet
            
            if bullet.rect.colliderect(player_rect):
                pygame.event.post(pygame.event.Event(self.USER_EVENT))
                bullet_to_remove = bullet

        if bullet_to_remove != 0:
            self.bullets.remove(bullet_to_remove)
    
    
    def take_damage(self, damage):
        '''This function is used to calculated the damage
        
        Input:
        -----
        damage:
            the damage receive from player or player receive damage from enemy
        
        Output:
        ------
        Player's Health decrease or enemies's health decrease
        '''
        self.health -= damage
        return self.health

    