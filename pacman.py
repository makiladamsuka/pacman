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
font = pygame.font.SysFont("freesanbold", 28)
run = True
level = boards
direction_command = 1
player = []
turns_allowed = [True, True, True, True]  # right, left, up, down
player_speed = 2
score = 0

for i in range(1, 5):
    player.append(pygame.transform.scale(pygame.image.load(f"assets/player_images/{i}.png").convert_alpha(), (30, 30)))
    
player_x = 300
player_y = 115
direction = 0
count = 0
flicker = False

def draw_board(level):
    cell_height = (HIGHT - 50) // 30 
    cell_width= (WIDTH // 30)
    
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, (255, 255, 255), (j * cell_height + (0.5* cell_height), i * cell_height + (0.5* cell_height)), 3)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, (255, 255, 255), (j * cell_height + (0.5* cell_height), i * cell_height + (0.5* cell_height)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, (0, 0, 255), (j * cell_height + (0.5* cell_height), i * cell_height), (j * cell_height + (0.5* cell_height), i * cell_height + cell_height), 3)
                
            if level[i][j] == 4:
                pygame.draw.line(screen, (0, 0, 255), (j * cell_width, (0.5* cell_height) + i * cell_height), ( j * cell_width+ cell_width, i * cell_height + (0.5* cell_height)), 3)
                
            if level[i][j] == 9:
                pygame.draw.line(screen, (255, 255, 255), (j * cell_width, (0.5* cell_height) + i * cell_height), ( j * cell_width+ cell_width, i * cell_height + (0.5* cell_height)), 3)
            
            if level[i][j] == 5:
                pygame.draw.arc(screen, (0, 0, 255), ((j * cell_width- (cell_width* 0.4)-2), (i * cell_height + (cell_height * 0.5)), cell_width, cell_height), 0, PI/2, 3)
                
            if level[i][j] == 6:
                pygame.draw.arc(screen, (0, 0, 255), ((j * cell_width+ (cell_width* 0.5)), (i * cell_height + (cell_height * 0.5)), cell_width, cell_height), PI/2, PI, 3)
                
            if level[i][j] == 7:
                pygame.draw.arc(screen, (0, 0, 255), ((j * cell_width+ (cell_width* 0.5)), (i * cell_height - (cell_height * 0.4)), cell_width, cell_height), PI, 3*PI/2, 3)
                
            if level[i][j] == 8:
                pygame.draw.arc(screen, (0, 0, 255), ((j * cell_width- (cell_width* 0.4)-2), (i * cell_height - (cell_height * 0.4)), cell_width, cell_height), 3*PI/2, 2*PI, 3)


def check_collision(score):
    cell_height = (HIGHT - 50) // 30  # 20
    cell_width = WIDTH // 30           # 20
    if 0 < player_x < WIDTH:
        if level[center_y//cell_width][center_x//cell_height] == 1:
            level[center_y//cell_width][center_x//cell_height] = 0
            score += 10

        if level[center_y//cell_width][center_x//cell_height] == 2:
            level[center_y//cell_width][center_x//cell_height] = 0
            score += 50
        
    return score
            
    

def move_player(player_x, player_y):
    if direction == 0 and turns_allowed[0]:
        player_x += player_speed
    if direction == 1 and turns_allowed[1]:
        player_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        player_y -= player_speed
    if direction == 3 and turns_allowed[3]:
        player_y += player_speed
    return player_x, player_y

def check_position(center_x, center_y):
    # turns = [right, left, up, down]
    turns = [False, False, False, False]
    cell_height = (HIGHT - 50) // 30  # 20
    cell_width = WIDTH // 30           # 20
    
    # 1. Edge tunnel safety: allow horizontal movement and prevent list crashes
    col = center_x // cell_width
    row = center_y // cell_height
    
    if col < 1 or col >= 29:
        # We are near or in the side tunnel: keep left/right open, stop vertical checks
        return [True, True, False, False]

    # Look ahead 12 pixels (just outside player's body radius)
    offset = 12

    # Check immediate path ahead
    # Right
    if level[row][(center_x + offset) // cell_width] < 3:
        turns[0] = True
    # Left
    if level[row][(center_x - offset) // cell_width] < 3:
        turns[1] = True
    # Up
    if level[(center_y - offset) // cell_height][col] < 3:
        turns[2] = True
    # Down
    if level[(center_y + offset) // cell_height][col] < 3:
        turns[3] = True

    # 2. Centering checks for clean turns:
    # Pac-Man can only turn 90 degrees if he is aligned with the grid lane
    x_in_cell = center_x % cell_width
    y_in_cell = center_y % cell_height

    # Moving UP/DOWN: you can only turn LEFT/RIGHT when vertically centered in the lane
    if direction in [2, 3]:
        if not (7 <= y_in_cell <= 13):
            turns[0] = False
            turns[1] = False

    # Moving LEFT/RIGHT: you can only turn UP/DOWN when horizontally centered in the lane
    if direction in [0, 1]:
        if not (7 <= x_in_cell <= 13):
            turns[2] = False
            turns[3] = False

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
        
def draw_misc():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.midleft = (10, HIGHT - 25)
    screen.blit(score_text, score_rect)
while run:
             
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
    
    player_x, player_y = move_player(player_x, player_y)
    turns_allowed = check_position(center_x, center_y)
    score = check_collision(score)
    draw_misc()
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
                
            if event.key == pygame.K_LEFT:
                direction_command = 1
                
            if event.key == pygame.K_UP:
                direction_command = 2
                
            if event.key == pygame.K_DOWN:
                direction_command = 3 
                
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction == 0:
                direction_command = direction
                
            if event.key == pygame.K_LEFT and direction == 1:
                direction_command = direction
                
            if event.key == pygame.K_UP and direction == 2:
                direction_command = direction
                
            if event.key == pygame.K_DOWN and direction == 3:
                direction_command = direction
                
    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = direction_command
            

    if player_x > WIDTH:
        player_x = -20
    elif player_x < -20:
        player_x = WIDTH
                        
    
    
    timer.tick(fps)
    
pygame.quit()