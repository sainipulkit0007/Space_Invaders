import pygame
import math
import random
from pygame import mixer

pygame.init()   

# Creating Screen
screen = pygame.display.set_mode((800, 600))  
# Background Img
background = pygame.image.load('background.png') 
# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Icon and Title
pygame.display.set_caption("Space Ship")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 500
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6    # For Multiple Enemies, No. of enemies can be changed as per requirement

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(10,100))
    enemyX_change.append(8)
    enemyY_change.append(30)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf',40)
textX=10
textY=10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf',100)

# Functions 
def show_score(x,y):
    game_score = font.render("Score : " + str(score),True,(255,255,255))
    screen.blit(game_score, (x,y))
def game_over_text():
    game_over = over_font.render("GAME OVER" ,True,(255,255,255))
    screen.blit(game_over, (100,220))    
def player(x,y):
    screen.blit(playerImg, (x,y))
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))    
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10))    
def collision(enemyX,enemyY,bulletX,bulletY):
    dis = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))  
    if dis < 27:
        return True  

# Game Loop "anything we want to display continously we write it in this loop"
r= True
while r:
    screen.fill((0,0,0))   
    screen.blit(background, (0,0))     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10 
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready": 
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    #G  et the current x Coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)    

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0           

    playerX += playerX_change   
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736 

    # Enemy Movement
    for i in range(no_of_enemies):
        # Game Over
        if enemyY[i] > 480:
            for j in range(no_of_enemies):
                enemyY[j] = 1000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]   
        if enemyX[i] <= 0:
            enemyX_change[i] = 8
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -8   
            enemyY[i] += enemyY_change[i]

        # Collision 
        col = collision(enemyX[i],enemyY[i],bulletX,bulletY)
        if col:
            col_sound = mixer.Sound('explosion.wav')
            col_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score += 1 
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(10,100)

        enemy(enemyX[i],enemyY[i],i)
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"
        
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change    

    player(playerX,playerY)  
    show_score(textX,textY)
    pygame.display.update()    
