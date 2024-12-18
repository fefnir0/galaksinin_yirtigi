import pygame
import random
import math

pygame.init()

# Set up the display
win = pygame.display.set_mode((750, 750))
pygame.display.set_caption("First Game")

# Load images
background_img = pygame.image.load('background.jpg')  # Background image
background_img = pygame.transform.scale(background_img, (750, 750))  # Resize to fit screen size

player_img = pygame.image.load('player.png')  # Player image
player_img = pygame.transform.scale(player_img, (30, 30))  # Resize the player image (adjust as needed)

enemy_img = pygame.image.load('enemy.png')  # Enemy image
enemy_img = pygame.transform.scale(enemy_img, (30, 30))  # Resize the enemy image (adjust as needed)

player_bullet_img = pygame.image.load('player_bullet.png')  # Replace with your player bullet image path
player_bullet_img = pygame.transform.scale(player_bullet_img, (15, 25))  # Resize as needed

enemy_bullet_img = pygame.image.load('enemy_bullet.png')  # Replace with your enemy bullet image path
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (20, 20))  # Resize as needed


playershoot = pygame.mixer.Sound('playershoot.wav')
playershoot.set_volume(0.07)
enemyshoot = pygame.mixer.Sound('enemyshoot.ogg')
enemysuccshoot = pygame.mixer.Sound('enemysuccshoot.wav')
playersuccshoot = pygame.mixer.Sound('playersuccshoot.ogg')

# Load and play background music
pygame.mixer.music.load('musictheme.ogg')  # Replace with your background music file path
pygame.mixer.music.set_volume(0.1)  # Adjust volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play music in a loop

enemysuccshoot.set_volume(0.07)

# Player settings
x = 375  # Centered in the 750x750 window
y = 375
radius = 12
vel = 1  # Slow movement speed

# Bullet settings
bullet_vel = 3  # Slow bullet speed
bullet = None  # No bullet at the start
last_shot_time = 0
cooldown_time = 500  # Cooldown time in milliseconds (0.5 seconds)

# Enemy settings
enemy_size = 30
enemy_x = random.randint(0, 750 - enemy_size)
enemy_y = random.randint(0, 750 - enemy_size)
enemy_vel_x = 0.6  # Horizontal velocity of enemy
enemy_vel_y = 0.6  # Vertical velocity of enemy
enemy_bullet_vel = 2  # Enemy bullet speed
enemy_bullet = None  # No enemy bullet at the start
last_enemy_shot_time = 0
enemy_shoot_cooldown = 2000  # Enemy shoots every 2 seconds

# Game over flag
game_over = False

# Score variable
score = 0


# Function to reset the game
def reset_game():
    global x, y, bullet, enemy_x, enemy_y, enemy_bullet, score, game_over, last_shot_time, last_enemy_shot_time
    # Reset player and game state
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
        # Show "Press R to Restart" message
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        win.blit(restart_text, (250, 425))

        pygame.display.update()

        # Wait for player to press 'R' to restart
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    waiting_for_restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Press R to restart
                        reset_game()  # Reset the game
                        waiting_for_restart = False
                        enemy_vel_x = 0.8  # Horizontal velocity of enemy
                        enemy_vel_y = 0.8

        continue  # Continue to the next iteration of the game loop after restarting

    win.fill((0, 0, 0))  # Clear the screen

    # Draw the background image
    win.blit(background_img, (0, 0))  # Display background at the top-left corner

    # Draw the player image
    win.blit(player_img, (x - player_img.get_width() // 2, y - player_img.get_height() // 2))
    player_img = pygame.transform.scale(player_img, (50, 50))

    # If there is an active bullet, move and display it
    if bullet is not None:
        bullet[1] -= bullet_vel  # Move the bullet upwards
        win.blit(player_bullet_img, (bullet[0], bullet[1]))  # Use player bullet image


        # Check if the bullet hits the enemy (collision detection)
        if bullet[0] > enemy_x and bullet[0] < enemy_x + enemy_size and bullet[1] > enemy_y and bullet[1] < enemy_y + enemy_size:
            # Bullet hit the enemy, destroy the enemy and respawn it
            playersuccshoot.play()
            enemy_x = random.randint(0, 750 - enemy_size)  # Respawn enemy at a new position
            enemy_y = random.randint(0, 750 - enemy_size)

            # Increase the score
            score += 1
            enemy_vel_x += 0.3
            enemy_vel_y += 0.3


            # Remove the bullet if it goes off the screen (top)
        if bullet[1] < 0:
            bullet = None

    # Move the enemy: Bounce off walls
    enemy_x += enemy_vel_x
    enemy_y += enemy_vel_y

    # Check for bouncing off the edges
    if enemy_x <= 0 or enemy_x >= 750 - enemy_size:
        enemy_vel_x = -enemy_vel_x  # Reverse horizontal direction
    if enemy_y <= 0 or enemy_y >= 750 - enemy_size:
        enemy_vel_y = -enemy_vel_y  # Reverse vertical direction

    # Draw the enemy image
    win.blit(enemy_img, (enemy_x, enemy_y))
    enemy_img = pygame.transform.scale(enemy_img, (60, 60))

    # Enemy shooting towards player
    current_time = pygame.time.get_ticks()  # Get current time in milliseconds
    if current_time - last_enemy_shot_time > enemy_shoot_cooldown:

        enemyshoot.play()

        # Calculate direction from enemy to player
        dx = x - (enemy_x + enemy_size // 2)
        dy = y - (enemy_y + enemy_size // 2)
        angle = math.atan2(dy, dx)  # Get angle of the player relative to the enemy
        enemy_bullet_vel_x = enemy_bullet_vel * math.cos(angle)  # Horizontal velocity of enemy bullet
        enemy_bullet_vel_y = enemy_bullet_vel * math.sin(angle)  # Vertical velocity of enemy bullet

        enemy_bullet = [enemy_x + enemy_size // 2 - 2.5, enemy_y + enemy_size]  # Fire bullet from the enemy's position
        last_enemy_shot_time = current_time  # Update the time of the last shot

    # If there is an active enemy bullet, move and display it
    if enemy_bullet is not None:
        enemy_bullet[0] += enemy_bullet_vel_x  # Move the enemy bullet towards the player horizontally
        enemy_bullet[1] += enemy_bullet_vel_y  # Move the enemy bullet towards the player vertically
        win.blit(enemy_bullet_img, (enemy_bullet[0], enemy_bullet[1]))  # Use enemy bullet image

        # Check if the enemy bullet hits the player (collision detection)
        if enemy_bullet[0] > x - radius and enemy_bullet[0] < x + radius and enemy_bullet[1] > y - radius and \
                enemy_bullet[1] < y + radius:
            game_over = True  # Player hit by enemy bullet, game over

        # Remove the enemy bullet if it goes off the screen (bottom or sides)
        if enemy_bullet[1] > 750 or enemy_bullet[0] < 0 or enemy_bullet[0] > 750:
            enemy_bullet = None

    # Display the score
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Key input handling
    userinput = pygame.key.get_pressed()

    # Movement controls for the triangle
    if userinput[pygame.K_LEFT] and x - radius > 0:
        x -= vel
    if userinput[pygame.K_RIGHT] and x + radius < 750:
        x += vel
    if userinput[pygame.K_UP] and y - radius > 0:
        y -= vel
    if userinput[pygame.K_DOWN] and y + radius < 750:
        y += vel

    # Shooting
    if userinput[pygame.K_SPACE] and bullet is None and current_time - last_shot_time > cooldown_time:
        bullet = [x - 2.5, y - radius]  # Create a new bullet at the top of the triangle
        last_shot_time = current_time  # Update the time of the last shot
        playershoot.play()

    pygame.display.update()  # Update the display
