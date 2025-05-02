import pygame
import random
import math

# Initialize pygame
pygame.init()

# Create the screen (height increased to 800)
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Space Raiders")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# Load background
background = pygame.image.load('background.jpg')

# Load player
player_img = pygame.image.load('player.png')
player_x = 370
player_y = 700
player_x_change = 0

# Load bullet
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = player_y
bullet_y_change = 5
bullet_state = "ready"

# Load explosion image (collision effect)
explosion_img = pygame.image.load('x.gif')
explosions = []  # [(x, y, timer)]

# Load aliens (slower speed)
alien_img = []
alien_x = []
alien_y = []
alien_x_change = []
alien_y_change = []
num_of_aliens = 6

for i in range(num_of_aliens):
    alien_img.append(pygame.image.load('alien.png'))
    alien_x.append(random.randint(0, 735))
    alien_y.append(random.randint(50, 150))
    alien_x_change.append(0.8)  # slower speed
    alien_y_change.append(40)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Functions
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(player_img, (x, y))

def alien(x, y, i):
    screen.blit(alien_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(alien_x, alien_y, bullet_x, bullet_y):
    distance = math.hypot(bullet_x - alien_x, bullet_y - alien_y)
    return distance < 27

def show_explosions():
    for exp in explosions[:]:
        x, y, timer = exp
        screen.blit(explosion_img, (x, y))
        if timer > 0:
            explosions[explosions.index(exp)] = (x, y, timer - 1)
        else:
            explosions.remove(exp)

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -2
            if event.key == pygame.K_RIGHT:
                player_x_change = 2
            if event.key == pygame.K_s and bullet_state == "ready":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    player_x = max(0, min(player_x, 736))

    # Alien movement
    for i in range(num_of_aliens):
        alien_x[i] += alien_x_change[i]
        if alien_x[i] <= 0 or alien_x[i] >= 736:
            alien_x_change[i] *= -1
            alien_y[i] += alien_y_change[i]

        # Collision check
        if is_collision(alien_x[i], alien_y[i], bullet_x, bullet_y):
            bullet_y = player_y
            bullet_state = "ready"
            score_value += 1
            explosions.append((alien_x[i], alien_y[i], 15))  # explosion for 15 frames

            alien_x[i] = random.randint(0, 735)
            alien_y[i] = random.randint(50, 150)

        alien(alien_x[i], alien_y[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        if bullet_y <= 0:
            bullet_y = player_y
            bullet_state = "ready"

    show_explosions()
    player(player_x, player_y)
    show_score(text_x, text_y)

    pygame.display.update()
