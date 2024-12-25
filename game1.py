import pygame
import random
import math

pygame.init()

win = pygame.display.set_mode((750, 750))
pygame.display.set_caption("First Game")

background_img = pygame.image.load('background.jpg')  
background_img = pygame.transform.scale(background_img, (750, 750))  #

player_img = pygame.image.load('player.png')  
player_img = pygame.transform.scale(player_img, (30, 30)) 

enemy_img = pygame.image.load('enemy.png')  
enemy_img = pygame.transform.scale(enemy_img, (30, 30))  

player_bullet_img = pygame.image.load('player_bullet.png')  
player_bullet_img = pygame.transform.scale(player_bullet_img, (15, 25))  

enemy_bullet_img = pygame.image.load('enemy_bullet.png') 
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (20, 20)) 


playershoot = pygame.mixer.Sound('playershoot.wav')
playershoot.set_volume(0.07)
enemyshoot = pygame.mixer.Sound('enemyshoot.ogg')
enemysuccshoot = pygame.mixer.Sound('enemysuccshoot.wav')
playersuccshoot = pygame.mixer.Sound('playersuccshoot.ogg')


pygame.mixer.music.load('musictheme.ogg')  
pygame.mixer.music.set_volume(0.1) 
pygame.mixer.music.play(-1)  

enemysuccshoot.set_volume(0.07)


x = 375 
y = 375
radius = 12
vel = 1


bullet_vel = 3  
bullet = None 
last_shot_time = 0
cooldown_time = 500  


enemy_size = 30
enemy_x = random.randint(0, 750 - enemy_size)
enemy_y = random.randint(0, 750 - enemy_size)
enemy_vel_x = 0.6  
enemy_vel_y = 0.6 
enemy_bullet_vel = 2  
enemy_bullet = None 
last_enemy_shot_time = 0
enemy_shoot_cooldown = 2000 


game_over = False


score = 0



def reset_game():
    global x, y, bullet, enemy_x, enemy_y, enemy_bullet, score, game_over, last_shot_time, last_enemy_shot_time
   
    x = 375
    y = 375
    bullet = None
    enemy_x = random.randint(0, 750 - enemy_size)
    enemy_y = random.randint(0, 750 - enemy_size)
    enemy_bullet = None
    score = 0
    game_over = False
    last_shot_time = 0
    last_enemy_shot_time = 0


run = True
while run:
    if game_over:
        font = pygame.font.SysFont(None, 55)
        text = font.render(f"GAME OVER! Score: {score}", True, (255, 0, 0))
        win.blit(text, (160, 375))
        enemysuccshoot.play()
     
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        win.blit(restart_text, (250, 425))

        pygame.display.update()

   
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    waiting_for_restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  
                        reset_game()  
                        waiting_for_restart = False
                        enemy_vel_x = 0.8 
                        enemy_vel_y = 0.8

        continue  

    win.fill((0, 0, 0))  #


    win.blit(background_img, (0, 0))  


    win.blit(player_img, (x - player_img.get_width() // 2, y - player_img.get_height() // 2))
    player_img = pygame.transform.scale(player_img, (50, 50))


    if bullet is not None:
        bullet[1] -= bullet_vel  
        win.blit(player_bullet_img, (bullet[0], bullet[1])) 



        if bullet[0] > enemy_x and bullet[0] < enemy_x + enemy_size and bullet[1] > enemy_y and bullet[1] < enemy_y + enemy_size:
         
            playersuccshoot.play()
            enemy_x = random.randint(0, 750 - enemy_size) 
            enemy_y = random.randint(0, 750 - enemy_size)


            score += 1
            enemy_vel_x += 0.3
            enemy_vel_y += 0.3


        if bullet[1] < 0:
            bullet = None

  
    enemy_x += enemy_vel_x
    enemy_y += enemy_vel_y


    if enemy_x <= 0 or enemy_x >= 750 - enemy_size:
        enemy_vel_x = -enemy_vel_x 
    if enemy_y <= 0 or enemy_y >= 750 - enemy_size:
        enemy_vel_y = -enemy_vel_y 

 
    win.blit(enemy_img, (enemy_x, enemy_y))
    enemy_img = pygame.transform.scale(enemy_img, (60, 60))

    
    current_time = pygame.time.get_ticks()  
    if current_time - last_enemy_shot_time > enemy_shoot_cooldown:

        enemyshoot.play()

     
        dx = x - (enemy_x + enemy_size // 2)
        dy = y - (enemy_y + enemy_size // 2)
        angle = math.atan2(dy, dx) 
        enemy_bullet_vel_x = enemy_bullet_vel * math.cos(angle) 
        enemy_bullet_vel_y = enemy_bullet_vel * math.sin(angle) 

        enemy_bullet = [enemy_x + enemy_size // 2 - 2.5, enemy_y + enemy_size] 
        last_enemy_shot_time = current_time  

  
    if enemy_bullet is not None:
        enemy_bullet[0] += enemy_bullet_vel_x  
        enemy_bullet[1] += enemy_bullet_vel_y 
        win.blit(enemy_bullet_img, (enemy_bullet[0], enemy_bullet[1])) 

        
        if enemy_bullet[0] > x - radius and enemy_bullet[0] < x + radius and enemy_bullet[1] > y - radius and \
                enemy_bullet[1] < y + radius:
            game_over = True 

        if enemy_bullet[1] > 750 or enemy_bullet[0] < 0 or enemy_bullet[0] > 750:
            enemy_bullet = None

 
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))

  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    userinput = pygame.key.get_pressed()

 
    if userinput[pygame.K_LEFT] and x - radius > 0:
        x -= vel
    if userinput[pygame.K_RIGHT] and x + radius < 750:
        x += vel
    if userinput[pygame.K_UP] and y - radius > 0:
        y -= vel
    if userinput[pygame.K_DOWN] and y + radius < 750:
        y += vel


    if userinput[pygame.K_SPACE] and bullet is None and current_time - last_shot_time > cooldown_time:
        bullet = [x - 2.5, y - radius]  
        last_shot_time = current_time  
        playershoot.play()

    pygame.display.update() 
