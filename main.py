import random
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 50  # Set Duration To 1000 ms == 1 second
from os import listdir
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
pygame.init()
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,255,0
screen=width,height = 1024,768
main_surface = pygame.display.set_mode(screen)
bg = pygame.transform.scale(pygame.image.load('background.png').convert(),screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3
IMG_PATH = 'goose'
imgs = [pygame.image.load(IMG_PATH + '/' + file).convert_alpha() for file in listdir(IMG_PATH)]
img_index = 0
ball = imgs[img_index]
ball_rect = ball.get_rect()
ball_speed = 4
FPS = pygame.time.Clock()
def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(),(100,35))
    enemy_rect = pygame.Rect(width,random.randint(0,height),*enemy.get_size())
    enemy_speed = random.randint(2,5)
    return [enemy, enemy_rect, enemy_speed]
def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(),(100,200))
    bonus_rect = pygame.Rect(random.randint(100,width-100),0,*bonus.get_size())
    bonus_speed = random.randint(1,4)
    return [bonus, bonus_rect, bonus_speed]
CHANGE_IMG = pygame.USEREVENT+1
pygame.time.set_timer(CHANGE_IMG, 200)
CREATE_ENEMY = pygame.USEREVENT+2
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []
CREATE_BONUS = pygame.USEREVENT+3
pygame.time.set_timer(CREATE_BONUS, 4500)
bonuses = []
scores = 0
font = pygame.font.SysFont('Verdana', 20)
Is_working = True 
while Is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            Is_working = False
        if event.type == CREATE_ENEMY: 
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS: 
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG: 
            img_index += 1
            if img_index == len(imgs): 
                img_index = 0
            ball = imgs[img_index]
    main_surface.blit(bg, (bgX,0))
    main_surface.blit(bg, (bgX2,0))
    bgX -= bg_speed
    bgX2 -= bg_speed
    if bgX < -bg.get_width():
        bgX=0
        bgX2 = bg.get_width()
    main_surface.blit(ball,ball_rect)
    count_msg = font.render(str(scores), True, GREEN)
    main_surface.blit(count_msg,(width-10-count_msg.get_size()[0],0))
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2],0)
        main_surface.blit(enemy[0],enemy[1])
        if enemy[1].left<0:
            enemies.pop(enemies.index(enemy))
        if ball_rect.colliderect(enemy[1]):            
            Is_working = False
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0,bonus[2])
        main_surface.blit(bonus[0],bonus[1])
        if bonus[1].bottom>height:
            bonuses.pop(bonuses.index(bonus))
        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            winsound.Beep(frequency, duration)
            scores += 1
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_DOWN] and ball_rect.bottom < height:
        ball_rect = ball_rect.move(0,ball_speed)
    if pressed_keys[K_UP] and ball_rect.top > 0:
        ball_rect = ball_rect.move(0,-ball_speed)
    if pressed_keys[K_LEFT] and ball_rect.left>0:
        ball_rect = ball_rect.move(-ball_speed,0)
    if pressed_keys[K_RIGHT]and ball_rect.right<width:
        ball_rect = ball_rect.move(ball_speed,0)
    pygame.display.flip()
Is_working = True
font = pygame.font.SysFont('Verdana', 80)
MSG = font.render("GAME OVER", True, RED)
S_MSG = font.render("YOUR SCORE IS: " + str(scores), True, GREEN)
main_surface.fill(BLACK)
winsound.Beep(180, 1000)
while Is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            Is_working = False
    main_surface.blit(MSG,(width/2-MSG.get_size()[0]/2, height/2-(MSG.get_size()[1])))
    main_surface.blit(S_MSG,(width/2-S_MSG.get_size()[0]/2, height/2))
    pygame.display.flip()
    