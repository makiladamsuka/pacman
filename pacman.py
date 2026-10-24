import pygame
from board import boards    
import math

pygame.init()

WIDTH = 600
HIGHT = 650
PI = math.pi

screen = pygame.display.set_mode((WIDTH, HIGHT))
timer = pygame.time.Clock()

fps = 60
font = pygame.font.SysFont("freesanbold", 75)
run = True
level = boards

player = []
turns_allowed = [True, True, True, True]  # right, left, up, down

for i in range(1, 5):
    player.append(pygame.transform.scale(pygame.image.load(f"assets/player_images/{i}.png").convert_alpha(), (30, 30)))
    
player_x = 300
player_y = 115
direction = 0
count = 0
flicker = False

def draw_board(level):
    num1 = (HIGHT - 50) // 30 
    num2 = (WIDTH // 30)
    
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, (255, 255, 255), (j * num1 + (0.5* num1), i * num1 + (0.5* num1)), 3)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, (255, 255, 255), (j * num1 + (0.5* num1), i * num1 + (0.5* num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, (0, 0, 255), (j * num1 + (0.5* num1), i * num1), (j * num1 + (0.5* num1), i * num1 + num1), 3)
                
            if level[i][j] == 4:
                pygame.draw.line(screen, (0, 0, 255), (j * num2 , (0.5* num1) + i * num1), ( j * num2 + num2 , i * num1 + (0.5* num1)), 3)
                
            if level[i][j] == 9:
                pygame.draw.line(screen, (255, 255, 255), (j * num2 , (0.5* num1) + i * num1), ( j * num2 + num2 , i * num1 + (0.5* num1)), 3)
            
            if level[i][j] == 5:
                pygame.draw.arc(screen, (0, 0, 255), ((j * num2 - (num2 * 0.4)-2), (i * num1 + (num1 * 0.5)), num2, num1), 0, PI/2, 3)
                
            if level[i][j] == 6:
                pygame.draw.arc(screen, (0, 0, 255), ((j * num2 + (num2 * 0.5)), (i * num1 + (num1 * 0.5)), num2, num1), PI/2, PI, 3)
                
            if level[i][j] == 7:
                pygame.draw.arc(screen, (0, 0, 255), ((j * num2 + (num2 * 0.5)), (i * num1 - (num1 * 0.4)), num2, num1), PI, 3*PI/2, 3)
                
            if level[i][j] == 8:
                pygame.draw.arc(screen, (0, 0, 255), ((j * num2 - (num2 * 0.4)-2), (i * num1 - (num1 * 0.4)), num2, num1), 3*PI/2, 2*PI, 3)



def check_position(x, y):
    turns = [False, False, False, False]  # right, left, up, down
    num1 = (HIGHT - 50) // 30
    num2 = (WIDTH // 30)
    num3 = 15  # half of player size
    
    if x//30  < 29:
        if direction == 0:
            if level[center_y//num1][center_x//num2 + num3] < 3:
                turns[1] = True
                
                
        if direction == 1:
            if level[center_y//num1][center_x//num2 - num3] < 3:
                turns[0] = True
                
        if direction == 2:
            if level[(center_y + num3)//num1 - num3][center_x//num2] < 3:
                turns[3] = True
                
        if direction == 3:
            if level[(center_y - num3)//num1 + num3][center_x//num2] < 3:
                turns[2] = True
                
                
    else:
        turns[0] = True
        turns[1] = True

    return turns

def draw_player():
    #0 RIGHT 1 LEFT 2 UP 3 DOWN
    
    frame = (count // 5) % len(player)
    
    if direction == 0:
        screen.blit(player[frame], (player_x, player_y))
        
    if direction == 1:
            screen.blit(pygame.transform.flip(player[frame], True, False), (player_x, player_y))
            
    if direction == 2:
            screen.blit(pygame.transform.rotate(player[frame], 90), (player_x, player_y))
            
        
    if direction == 3:
            screen.blit(pygame.transform.rotate(player[frame], 270), (player_x, player_y))
        
                                             
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0
                
            if event.key == pygame.K_LEFT:
                direction = 1
                
            if event.key == pygame.K_UP:
                direction = 2
                
            if event.key == pygame.K_DOWN:
                direction = 3 
            
            
    if (count < 20):
        count += 1
        
        if count > 10:
            flicker = True
        
        
    else:
        count = 0
        flicker = False

    screen.fill((0, 0, 0))
    draw_board(level)
    
    draw_player()
    
    center_x = player_x + 15
    center_y = player_y + 15
    
    pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), 3)
    turns_allowed = check_position(center_x, center_y)
    pygame.display.update()
    timer.tick(fps)
    
pygame.quit()