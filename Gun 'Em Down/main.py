from cProfile import run
from pickle import FALSE
import pygame 
import os
import math
import random
from Bullet import Bullet
from Enemy import Enemy
from Enemy2 import Enemy2
from Enemy3 import Enemy3
from Enemy4 import Enemy4
from Powerup import Powerup
from Button import Button


pygame.font.init()
MIXER = pygame.mixer
MIXER.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Constants
FPS = 60
DELTA_TIME = 0.017

FONT = pygame.font.SysFont("roboto", 40)

BULLET_VEL = 7
MAX_BULLETS = 20

shoot_particle_colors = [(255, 0, 0), (255, 215,0), (255, 69, 0)]

OBSTACLE_COLOR = (110, 230, 140)

PLAYER_WIDTH, PLAYER_HEIGHT = 30, 30

# ENEMYWIDTH, HEIGHT
ENEMY1_WIDTH, ENEMY1_HEIGHT = 30, 30
ENEMY2_WIDTH, ENEMY2_HEIGHT = 20, 20
ENEMY3_WIDTH, ENEMY3_HEIGHT = 35, 35
ENEMY4_WIDTH, ENEMY4_HEIGHT = 70, 70

GUN_WIDTH, GUN_HEIGHT = 30, 30
GUN_OFFSET_X, GUN_OFFSET_Y = 15, 15

POWERUP_WIDTH, POWERUP_HEIGHT = 25, 25

PLAYER_IMAGE = pygame.image.load(os.path.join("PygameProject", "Assets", "Player.png"))
PLAYER = pygame.transform.rotate(pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), -90) # SCALED AND ROTATED

GUN_IMAGE = pygame.image.load(os.path.join("PygameProject", "Assets", "gun.png"))

PLAYER_GUN = pygame.transform.rotate(pygame.transform.scale(GUN_IMAGE, (GUN_WIDTH, GUN_HEIGHT)), -90) # SCALED AND ROTATED


# ENEMIES
ENEMY1_IMAGE = pygame.image.load(os.path.join("PygameProject", "Assets", "Enemy.png"))
ENEMY1 = pygame.transform.scale(ENEMY1_IMAGE, (ENEMY1_WIDTH, ENEMY1_HEIGHT)) # SCALED AND ROTATED

ENEMY2_IMAGE = pygame.image.load(os.path.join("PygameProject", "Assets", "Enemy2.png"))
ENEMY2 = pygame.transform.scale(ENEMY2_IMAGE, (ENEMY2_WIDTH, ENEMY2_HEIGHT)) # SCALED AND ROTATED

ENEMY3_IMAGE = pygame.image.load(os.path.join("PygameProject", "Assets", "Enemy3.png"))
ENEMY3 = pygame.transform.scale(ENEMY3_IMAGE, (ENEMY3_WIDTH, ENEMY3_HEIGHT)) # SCALED AND ROTATED

ENEMY4_IMAGE = pygame.image.load(os.path.join("PygameProject", "Assets", "Enemy4.png"))
ENEMY4 = pygame.transform.scale(ENEMY4_IMAGE, (ENEMY4_WIDTH, ENEMY4_HEIGHT)) # SCALED AND ROTATED




LIFE_POWERUP_IMAGE = pygame.image.load(os.path.join("PygameProject", "Assets", "LifePowerUp.png"))
LIFE_POWERUP = pygame.transform.scale(LIFE_POWERUP_IMAGE, (POWERUP_WIDTH + 5, POWERUP_HEIGHT + 5))
LIFE_POWERUP_INCREASE = 10

FIRE_RATE_POWERUP_IMAGE = pygame.image.load(os.path.join("PygameProject", "Assets", "FireRatePowerUp.png"))
FIRE_RATE_POWERUP = pygame.transform.scale(FIRE_RATE_POWERUP_IMAGE, (POWERUP_WIDTH, POWERUP_HEIGHT))
FIRE_RATE_INCREASE = 0.1

SPEED_POWERUP_IMAGE = pygame.image.load(os.path.join("PygameProject", "Assets", "SpeedPowerUp.png"))
SPEED_POWERUP = pygame.transform.scale(SPEED_POWERUP_IMAGE, (POWERUP_WIDTH, POWERUP_HEIGHT))
SPEED_POWERUP_INCREASE = 0.3

SHIELD_POWERUP_IMAGE = pygame.image.load(os.path.join("PygameProject", "Assets", "ShieldPowerUp.png"))
SHIELD_POWERUP = pygame.transform.scale(SHIELD_POWERUP_IMAGE, (POWERUP_WIDTH, POWERUP_HEIGHT))
SHIELD_POWERUP_INCREASE = 40

POWERUP_DROP_RATE = 3

MAX_ENEMIES = 20

SPAWNPOSX, SPAWNPOSY = 450, 250 # PLAYER SPAWN POS
ENEMY_SPAWNPOSES = [(20, 40), (690, 400), (450, 320), (120, 440), (860, 60), (840, 430)]

ENEMY_1_HIT_PLAYER = pygame.USEREVENT + 1
ENEMY_2_HIT_PLAYER = pygame.USEREVENT + 2
ENEMY_3_HIT_PLAYER = pygame.USEREVENT + 3
ENEMY_4_HIT_PLAYER = pygame.USEREVENT + 4

ENEMY_1_DAMAGE = 20
ENEMY_2_DAMAGE = 20
ENEMY_3_DAMAGE = 30
ENEMY_4_DAMAGE = 50


# SOUNDS
PLAYER_HIT_SOUND = MIXER.Sound(os.path.join("PygameProject", "Assets", "Player_Hit.wav"))
PLAYER_SHOOT_SOUND = MIXER.Sound(os.path.join("PygameProject", "Assets", "Player_Shoot.wav"))
PLAYER_DIE_SOUND = MIXER.Sound(os.path.join("PygameProject", "Assets", "Die.wav"))
CLICK_BUTTON_SOUND = MIXER.Sound(os.path.join("PygameProject", "Assets", "Click_Button.wav"))
ENEMY_DIE_SOUND = MIXER.Sound(os.path.join("PygameProject", "Assets", "Enemy_Die.wav"))
WAVE_UP_SOUND = MIXER.Sound(os.path.join("PygameProject", "Assets", "Wave_Up.wav"))
PICK_UP_POWERUP_SOUND = MIXER.Sound(os.path.join("PygameProject", "Assets", "Pick_Up_Powerup.wav"))



# Obstacles
obstacles = []
obstacles.append(pygame.Rect(365, 400, 170, 20))
obstacles.append(pygame.Rect(365, 70, 170, 20))
obstacles.append(pygame.Rect(700, 280, 70, 70))
obstacles.append(pygame.Rect(100, 70, 70, 70))
obstacles.append(pygame.Rect(740, 120, 40, 40))
obstacles.append(pygame.Rect(80, 400, 40, 40))
obstacles.append(pygame.Rect(330, 250, 40, 40))

def draw_window(color, player_sprite, player_rot, bullets, gun_sprite, gun_rot, enemies, wave, health_rect, current_health_rect, powerups, shield_rect, current_shield_rect):
    global play_again_button
    global game_over_panel
    global game_over_text
    global player_damage
    global player_armor
    global next_wave
    global Damage_Buff_button
    global Armor_Buff_button
    global rand
    global rand_buff
    
    WIN.fill(color)

    for obstacle in obstacles:
        pygame.draw.rect(WIN, OBSTACLE_COLOR, obstacle, 5)

    wave_text = FONT.render("WAVE " + str(wave), 1, (255, 255, 255))
    WIN.blit(wave_text, (WIDTH/2 - wave_text.get_width()/2, 10))

    atk_text = FONT.render("ATK:" + str(player_damage), 1, (255, 255, 255))
    WIN.blit(atk_text, (WIDTH*0.8 , 10))

    armor_text = FONT.render("ARMOR:" + str(player_armor), 1, (255, 255, 255))
    WIN.blit(armor_text, (WIDTH*0.8 , 50))

    pygame.draw.rect(WIN, (255, 255, 255), health_rect, 100)
    pygame.draw.rect(WIN, (255, 0, 0), current_health_rect, 100)

    pygame.draw.rect(WIN, (255, 255, 255), shield_rect, 100)
    pygame.draw.rect(WIN, (0, 0, 255), current_shield_rect, 100)
    
    for powerup in powerups:
        WIN.blit(powerup.surface, powerup.rect)

    for bullet in bullets:
        pygame.draw.rect(WIN, (255, 255, 255), bullet.rect, 5)

    for enemy in enemies:
        for bullet in enemy.bullets:
            pygame.draw.rect(WIN, (255, 0, 0), bullet.rect, 20)
        WIN.blit(enemy.surface, enemy.rotated_rect)
        WIN.blit(enemy.gun_rotated, enemy.gun_rotated_rect)
    
    WIN.blit(player_sprite, player_rot)
    WIN.blit(gun_sprite, gun_rot)

    if game_is_over:
        pygame.draw.rect(WIN, (110, 230, 140), game_over_panel, 1000)
        play_again_button.draw(WIN, True)
        WIN.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width()/2, 70))
        WIN.blit(score_text, (WIDTH / 2 - score_text.get_width()/2, 160))
        WIN.blit(enemies_killed_text, (WIDTH / 2 - enemies_killed_text.get_width()/2, 235))

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[pygame.BUTTON_LEFT - 1] and play_again_button.isOver(pygame.mouse.get_pos()):
            CLICK_BUTTON_SOUND.play()
            main()
           
    if next_wave:
        Damage_Buff_button.draw(WIN,True)
        Armor_Buff_button.draw(WIN,True)
        
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[pygame.BUTTON_LEFT - 1] and Damage_Buff_button.isOver(pygame.mouse.get_pos()):
            CLICK_BUTTON_SOUND.play()
            player_damage+=1
            next_wave = False
        if mouse_pressed[pygame.BUTTON_LEFT - 1] and Armor_Buff_button.isOver(pygame.mouse.get_pos()):
            CLICK_BUTTON_SOUND.play()
            player_armor+=3
            next_wave = False
    
    # if rand:
    #     if random.choice(rand_buff)==1:
    #         Buff_font = pygame.font.SysFont('roboto', 80)
    #         Buff_text = Buff_font.render("+ bullet type 2", 1, (255, 0, 0))
    #         WIN.blit(Buff_text, (WIDTH / 2 - Buff_text.get_width()/2, 70))
    #         player_bullets.append(bullet2)
    #     if random.choice(rand_buff)==2:
    #         Buff_font = pygame.font.SysFont('roboto', 80)
    #         Buff_text = Buff_font.render("+ bullet type 3", 1, (255, 0, 0))
    #         WIN.blit(Buff_text, (WIDTH / 2 - Buff_text.get_width()/2, 70))
    #         player_bullets.append(bullet3)
    #     if random.choice(rand_buff)==3:
    #         Buff_font = pygame.font.SysFont('roboto', 80)
    #         Buff_text = Buff_font.render("+ bullet type 4", 1, (255, 0, 0))
    #         WIN.blit(Buff_text, (WIDTH / 2 - Buff_text.get_width()/2, 70))
    #         player_bullets.append(bullet4)
    #     rand=False
    
        
    pygame.display.update()



def handle_player_movement(keys_pressed, player, x, y):
    previous_pos_x = x
    previous_pos_y = y

    if keys_pressed[pygame.K_w] and y - run_speed > 0 - 0.1:
        y -= run_speed
    if keys_pressed[pygame.K_s] and y + run_speed < HEIGHT - PLAYER_HEIGHT:
        y += run_speed
    if keys_pressed[pygame.K_a] and x - run_speed > 0 - 0.1:
        x -= run_speed
    if keys_pressed[pygame.K_d] and x + run_speed < WIDTH - PLAYER_WIDTH:
        x += run_speed

    player.x = x
    player.y = y
    
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            if math.isclose(obstacle.right, player.left, abs_tol=3) or math.isclose(obstacle.left, player.right, abs_tol=3):
                x = previous_pos_x
            elif math.isclose(obstacle.top, player.bottom, abs_tol=3) or math.isclose(obstacle.bottom, player.top, abs_tol=3):
                y = previous_pos_y
            else:
                x = previous_pos_x
                y = previous_pos_y
    return [x, y]  

def take_damage(damage, player_health):
    global player_shield
    global player_armor
    player_shield -=damage
    if player_shield> 100:
        player_shield = 100
    elif player_shield <=0:
        player_shield = 0
    if player_shield==0:
        player_health -= damage-player_armor
    if player_health > 100:
        player_health = 100
    elif player_health <= 0:
        player_health = 0
        game_over()
    
    current_health_rect.width = player_health * 1.5
    current_shield_rect.width = player_shield * 1.5
    return player_health


def new_wave():
    global amount_of_enemies
    global enemy_spawn_rate_min
    global enemy_spawn_rate_max
    global wave
    global enemies_killed_wave
    global enemies_spawned_wave
    global enemy_rarity_chance
    global next_wave
    global Damage_Buff_button
    global Armor_Buff_button
    global enemies
    global rand_buff
    global rand
    WAVE_UP_SOUND.play()
    wave += 1
    next_wave=True
    enemy_rarity_chance.append(0)
    if wave > 3:
        enemy_rarity_chance.append(1)
    if wave > 5:
        enemy_rarity_chance.append(2)
        enemy_rarity_chance.append(2)
    if wave > 8:
        enemy_rarity_chance.append(3)
    if wave  % 10 == 0:
        for enemy in enemies:
            enemy.health+=150
            enemy.speed+=0.5
        #rand=True


    enemies_killed_wave = 0
    enemies_spawned_wave = 0
    amount_of_enemies += enemy_spawn_increase
    enemy_spawn_rate_min += enemy_spawn_rate_increase
    enemy_spawn_rate_max += enemy_spawn_rate_increase
    if next_wave == False:
        del Damage_Buff_button
        del Armor_Buff_button
    

def handle_player_bullets(player_bullets):    
    # Update Bullets
    bullet_to_remove = 0
    global enemies_killed_wave
    global enemies_killed
    global next_wave
    for bullet in player_bullets:
        bullet.update()
        for obstacle in obstacles:
            if bullet.rect.x >= WIDTH or bullet.rect.x <= 0 or bullet.rect.y >= HEIGHT or bullet.rect.y <= 0:
                bullet_to_remove = bullet
            elif bullet.rect.colliderect(obstacle):
                bullet_to_remove = bullet
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                if enemy.take_damage(player_damage) <= 0:
                    enemies_killed += 1
                    ENEMY_DIE_SOUND.play()

                    if random.randrange(0, 11) < POWERUP_DROP_RATE:
                        rand = random.randrange(0, 4)
                        surface = 0
                        if rand == 0:
                            surface = LIFE_POWERUP
                        elif rand == 1:
                            surface = SPEED_POWERUP
                        elif rand == 2:
                            surface = FIRE_RATE_POWERUP
                        elif rand == 3:
                            surface = SHIELD_POWERUP
                        powerups.append(Powerup(enemy.rect, POWERUP_WIDTH, POWERUP_HEIGHT, surface, rand))

                    enemies.remove(enemy)
                    enemies_killed_wave += 1
                    if enemies_killed_wave == amount_of_enemies:
                        new_wave()
                    
                    color = 0
                    if enemy.index == 0:
                        color = (255, 67, 67)
                    elif enemy.index == 1:
                        color = (237, 225, 32)
                    elif enemy.index == 2:
                        color = (169, 32, 237)
                    elif enemy.index == 3:
                        color = (237, 105, 32)

                bullet_to_remove = bullet

    if bullet_to_remove != 0:
        player_bullets.remove(bullet_to_remove)



def handle_powerups(powerups, player):
    global player_health
    global run_speed
    global bullet_fire_rate
    global player_shield
    global current_shield_rect
    global current_health_rect
    powerup_to_remove = 0
    for powerup in powerups:
        if player.colliderect(powerup.rect):
            PICK_UP_POWERUP_SOUND.play()
            if powerup.index == 0:
                powerup_to_remove = powerup
                player_health += LIFE_POWERUP_INCREASE
                if player_health>100:
                    player_health=100
                current_health_rect.width = player_health * 1.5
            elif powerup.index == 1:
                powerup_to_remove = powerup
                run_speed += SPEED_POWERUP_INCREASE
            elif powerup.index == 2:
                powerup_to_remove = powerup
                bullet_fire_rate += FIRE_RATE_INCREASE
            elif powerup.index ==3:
                powerup_to_remove = powerup
                player_shield += SHIELD_POWERUP_INCREASE
                if player_shield>100:
                    player_shield=100
                current_shield_rect.width = player_shield * 1.5

            
    if powerup_to_remove != 0:
        powerups.remove(powerup_to_remove)


def game_over():
    pygame.display.set_caption("YOU ARE DEAD")
    PLAYER_DIE_SOUND.play()
    MIXER.music.stop()
    global game_is_over
    global wave
    game_is_over = True
    global score_text
    global enemies_killed_text
    score_font = pygame.font.SysFont("roboto", 50)
    score_text = score_font.render("You got to wave " + str(wave) + "!", 1, (50, 50, 50))
    enemies_killed_text = score_font.render("Enemies killed: " + str(enemies_killed), 1, (255, 0, 0))




def main():
    pygame.display.set_caption("DUNGEON")

    clock = pygame.time.Clock()
    run = True
    
    global wave
    wave = 1
    global enemies_killed
    enemies_killed = 0
    global pause
    pause = False
    global game_is_over
    global game_over_panel
    global play_again_button
    global Damage_Buff_button
    global Armor_Buff_button
    global game_over_text
    global next_wave
    global rand_buff
    global rand
    rand=False
    rand_buff=[1,2,3]
    next_wave = False
    game_is_over = False
    game_over_panel = pygame.Rect(450 - 200, 250 - 250, 400, 500)
    play_again_button = Button((255, 255, 255), 450 - 100, 350, 200, 80, "Play Again")
    Damage_Buff_button = Button((255, 255, 255), 450 - 100, 200, 200, 80, "Atttack Up!")
    Armor_Buff_button = Button((255, 255, 255), 450 - 100, 300, 200, 80, "Armor Up!")
    game_over_font = pygame.font.SysFont('roboto', 80)
    game_over_text = game_over_font.render("GAME OVER", 1, (255, 0, 0))


    # WAVE VARIABLES
    global amount_of_enemies
    global enemy_rarity_chance
    global enemies_spawned_wave
    global enemies_killed_wave
    global enemy_spawn_increase
    global enemy_spawn_rate_increase

    amount_of_enemies = 2
    enemy_rarity_chance = [0]

    enemies_spawned_wave = 0
    enemies_killed_wave = 0

    enemy_spawn_increase = 2
    enemy_spawn_rate_increase = 0.07

    # PLAYER VARIABLES
    global player
    global x, y
    global player_bullets
    global player_damage
    global player_health
    global run_speed
    global health_rect
    global current_health_rect
    global player_shield
    global shield_rect
    global current_shield_rect 
    global player_armor
    player = pygame.Rect(SPAWNPOSX, SPAWNPOSY, PLAYER_WIDTH, PLAYER_HEIGHT) # MAKE PLAYER RECT FOR MOVEMENT
    x, y = player.x, player.y
    player_bullets = []
    player_shield=100
    player_armor = 0
    player_damage = 5
    player_health = 100
    run_speed = 2

    health_rect = pygame.Rect(WIDTH - player_health * 1.5 - 10, HEIGHT - 30, player_health * 1.5, 20)
    current_health_rect = pygame.Rect(WIDTH - player_health * 1.5 - 10, HEIGHT - 30, player_health * 1.5, 20)

    shield_rect = pygame.Rect(WIDTH - player_shield * 1.5 - 10, HEIGHT - 60, player_shield * 1.5, 20)
    current_shield_rect = pygame.Rect(WIDTH - player_shield * 1.5 - 10, HEIGHT - 60, player_shield * 1.5, 20)

    # BULLET VARIABLES
    global bullet_fire_rate
    global time_before_shoot
    bullet_fire_rate = 1
    time_before_shoot = 0
    global bullet2
    global bullet3
    global bullet4
    # ENEMY VARIABLES
    global enemies
    global enemy_spawn_rate_min
    global enemy_spawn_rate_max
    global time_before_enemy_spawn

    enemies = []
    enemy_spawn_rate_min = 0.2
    enemy_spawn_rate_max = 0.3
    time_before_enemy_spawn = 1 / random.uniform(enemy_spawn_rate_min, enemy_spawn_rate_max)

    # POWERUP VARIABLES
    global powerups
    powerups = []



    while run:
        if not game_is_over:
            mousex, mousey = pygame.mouse.get_pos() # GET MOUSE POS

            # HANDLE PLAYER MOVEMENT
            keys_pressed = pygame.key.get_pressed()
            xylist = handle_player_movement(keys_pressed, player, x, y)    
            x = xylist[0]
            y = xylist[1]

            # POWERUPS
            handle_powerups(powerups, player)

            # PLAYER ROTATION
            dirx = mousex - player.centerx
            diry = player.centery - mousey
            angle = math.degrees(math.atan2(diry, dirx))
            player_rotated = pygame.transform.rotate(PLAYER, angle)
            gun_rotated = pygame.transform.rotate(PLAYER_GUN, angle)
            player_rotated_rect = player_rotated.get_rect(center = player.center)
            gun_rotated_rect = gun_rotated.get_rect(center = player.center)

            # GUN ROTATION
            if not pygame.Vector2(dirx, diry).length() == 0:
                gun_x = pygame.Vector2.dot(pygame.Vector2(0, 1), pygame.Vector2(dirx, diry).normalize())
                gun_y = pygame.Vector2.dot(pygame.Vector2(1, 0), pygame.Vector2(dirx, diry).normalize())
                gun_rotated_rect.x += GUN_OFFSET_X * gun_x
                gun_rotated_rect.y += GUN_OFFSET_Y * gun_y




            # BULLETS
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[pygame.BUTTON_LEFT - 1] and time_before_shoot <= 0 and len(player_bullets) < MAX_BULLETS:
                
                
                PLAYER_SHOOT_SOUND.play()

                # BULLET ROTATION
                bullet_angle = math.degrees(math.atan2(diry, dirx))

                
                bullet = Bullet((gun_rotated_rect.centerx, gun_rotated_rect.centery), bullet_angle, (4, 4), 7)

                #bullet2 = Bullet((gun_rotated_rect.centerx, gun_rotated_rect.centery), bullet_angle, (4, 4), 3.5)
                
                #bullet3 = Bullet((gun_rotated_rect.centerx, gun_rotated_rect.centery), bullet_angle, (4, 4), 5)
                
                #bullet4 = Bullet((gun_rotated_rect.centerx, gun_rotated_rect.centery), bullet_angle, (4, 4), 8)

                player_bullets.append(bullet)
                
                
                time_before_shoot = 1 / bullet_fire_rate

            if time_before_shoot > 0:
                time_before_shoot -= DELTA_TIME

            handle_player_bullets(player_bullets)


            # ENEMIES
            if time_before_enemy_spawn <= 0 and enemies_spawned_wave < amount_of_enemies:
                pos_index = random.randrange(0, len(ENEMY_SPAWNPOSES))

                enemy_index = random.randrange(0, len(enemy_rarity_chance))
                if enemy_rarity_chance[enemy_index] == 0:
                    enemies.append(Enemy(ENEMY_SPAWNPOSES[pos_index], (ENEMY1_WIDTH, ENEMY1_HEIGHT), ENEMY1, obstacles, GUN_IMAGE))
                elif enemy_rarity_chance[enemy_index] == 1:
                    enemies.append(Enemy2(ENEMY_SPAWNPOSES[pos_index], (ENEMY2_WIDTH, ENEMY2_HEIGHT), ENEMY2, obstacles, GUN_IMAGE))
                elif enemy_rarity_chance[enemy_index] == 2:
                    enemies.append(Enemy3(ENEMY_SPAWNPOSES[pos_index], (ENEMY3_WIDTH, ENEMY3_HEIGHT), ENEMY3, obstacles, GUN_IMAGE))
                elif enemy_rarity_chance[enemy_index] == 3:
                    enemies.append(Enemy4(ENEMY_SPAWNPOSES[pos_index], (ENEMY4_WIDTH, ENEMY4_HEIGHT), ENEMY4, obstacles, GUN_IMAGE))


                time_before_enemy_spawn = 1 / random.uniform(enemy_spawn_rate_min, enemy_spawn_rate_max)
                enemies_spawned_wave += 1
            
            time_before_enemy_spawn -= DELTA_TIME

            for enemy in enemies:
                enemy.update_move_rot(player_rotated_rect)
                enemy.handle_collisions(player_rotated_rect)
                enemy.update_gun(player)
                enemy.update_bullets(obstacles, WIDTH, HEIGHT, player_rotated_rect)
            
            for powerup in powerups:
                powerup.update()

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == ENEMY_1_HIT_PLAYER:
                player_health = take_damage(ENEMY_1_DAMAGE, player_health)
                PLAYER_HIT_SOUND.play()
            elif event.type == ENEMY_2_HIT_PLAYER:
                player_health = take_damage(ENEMY_2_DAMAGE, player_health)
                PLAYER_HIT_SOUND.play()
            elif event.type == ENEMY_3_HIT_PLAYER:
                player_health = take_damage(ENEMY_3_DAMAGE, player_health)
                PLAYER_HIT_SOUND.play()
            elif event.type == ENEMY_4_HIT_PLAYER:
                player_health = take_damage(ENEMY_4_DAMAGE, player_health)
                PLAYER_HIT_SOUND.play()
        
        draw_window((50, 50, 50), player_rotated, player_rotated_rect, player_bullets, gun_rotated, gun_rotated_rect, enemies, wave, health_rect, current_health_rect, powerups, shield_rect, current_shield_rect)

    pygame.quit()

if __name__ == "__main__":
    main()
