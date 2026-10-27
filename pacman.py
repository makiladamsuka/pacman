import pygame
from board import boards    
import math

pygame.init()

WIDTH = 600
HIEGHT = 650
PI = math.pi

screen = pygame.display.set_mode((WIDTH, HIEGHT))
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

powerups = False
eaten_ghosts = [False, False, False, False]
power_counter = 0
moving = False
startup_counter = 0

for i in range(1, 5):
    player.append(pygame.transform.scale(pygame.image.load(f"assets/player_images/{i}.png").convert_alpha(), (30, 30)))
    


player_x = 300
player_y = 115
direction = 0
count = 0
flicker = False
lives = 3

import pygame

blinky_img = pygame.transform.scale(pygame.image.load("assets/ghost_images/red.png").convert_alpha(), (30, 30))
pinky_img = pygame.transform.scale(pygame.image.load("assets/ghost_images/pink.png").convert_alpha(), (30, 30))
inky_img = pygame.transform.scale(pygame.image.load("assets/ghost_images/blue.png").convert_alpha(), (30, 30))
clyde_img = pygame.transform.scale(pygame.image.load("assets/ghost_images/orange.png").convert_alpha(), (30, 30))
spooked_img = pygame.transform.scale(pygame.image.load("assets/ghost_images/powerup.png").convert_alpha(), (30, 30))
dead_img = pygame.transform.scale(pygame.image.load("assets/ghost_images/dead.png").convert_alpha(), (30, 30))

blinky_x = 490
blinky_y = 300
blinky_direction = 0
blinky_dead = False
pinky_x = 300
pinky_y = 360
pinky_direction = 2
pinky_dead = False
inky_x = 300
inky_y = 300
inky_direction = 2
inky_dead = False
clyde_x = 300
clyde_y = 300
clyde_direction = 0
clyde_dead = False


eaten_ghosts = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]

class Ghost:
    def __init__(self, x_cood, y_cood, img, target, speed, direction, dead, box, id):
        self.x_cood = x_cood
        self.y_cood = y_cood
        self.img = img
        self.target = target
        self.speed = speed
        self.direction = direction
        self.dead = dead
        self.box = box
        self.id = id
        self.center_x = self.x_cood + 15
        self.center_y = self.y_cood + 15
        self.turns, self.in_box = self.check_collision()
        self.rect = self.draw()
        if self.id == 3:
            self.move_clyde()   
    def draw(self):
        
        if (not self.dead and not powerups) or (eaten_ghosts[self.id] and not self.dead):
            screen.blit(self.img, (self.x_cood, self.y_cood))
            
        elif powerups and not self.dead and not eaten_ghosts[self.id]:
            screen.blit(spooked_img, (self.x_cood, self.y_cood))
            
        else:
            screen.blit(dead_img, (self.x_cood, self.y_cood))
            
        ghost_rect = pygame.rect.Rect(self.center_x - 18, self.y_cood -18 , 30, 30)
        
        return ghost_rect
    
    
    def check_collision(self):
        self.turns = [False, False, False, False]
        self.in_box = False
        # R, L, U, D
        num1 = ((HIEGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_cood < 550 and 370 < self.y_cood < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
        self.center_x = self.x_cood + 15
        self.center_y = self.y_cood + 15

        if not self.turns[self.direction]:
            horizontal_direction = 0 if self.target[0] > self.center_x else 1
            vertical_direction = 3 if self.target[1] > self.center_y else 2
            for direction in (
                horizontal_direction,
                vertical_direction,
                1 - horizontal_direction,
                5 - vertical_direction,
            ):
                if self.turns[direction]:
                    self.direction = direction
                    break

        if self.turns[self.direction]:
            if self.direction == 0:
                self.x_cood += self.speed
            elif self.direction == 1:
                self.x_cood -= self.speed
            elif self.direction == 2:
                self.y_cood -= self.speed
            else:
                self.y_cood += self.speed

        self.center_x = self.x_cood + 15
        self.center_y = self.y_cood + 15
def draw_board(level):
    cell_height = (HIEGHT - 50) // 30 
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

def check_collision(score, powerups, power_counter, eaten_ghosts):
    cell_height = (HIEGHT - 50) // 30  # 20
    cell_width = WIDTH // 30           # 20
    if 0 < player_x < WIDTH:
        if 0 < player_y < HIEGHT - 50:
            if level[center_y//cell_width][center_x//cell_height] == 1:
                level[center_y//cell_width][center_x//cell_height] = 0
                score += 10

        if level[center_y//cell_width][center_x//cell_height] == 2:
            level[center_y//cell_width][center_x//cell_height] = 0
            score += 50
            powerups = True
            power_counter = 0
        
    return score, powerups, power_counter, eaten_ghosts      
    
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
    cell_height = (HIEGHT - 50) // 30  # 20
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
    score_rect.midleft = (10, HIEGHT - 25)
    screen.blit(score_text, score_rect)
    
    
    if powerups:
        pygame.draw.circle(screen, (0, 0, 255), (150, HIEGHT - 25), 10)
        
        
    for i in range(lives):
        screen.blit(pygame.transform.scale(player[0], (20, 20)), ((200 + (i * 30)), (HIEGHT - 35)))
while run:
             
    if (count < 20):
        count += 1
        
        if count > 10:
            flicker = True
        
        
    else:
        count = 0
        flicker = False
        
        
    if powerups and power_counter < 600:
        power_counter += 1
        
    elif power_counter >= 600 and powerups:
        powerups = False
        power_counter = 0
        eaten_ghosts = [False, False, False, False]
        
        
    if startup_counter < 180:
        moving = False
        startup_counter += 1
        
    else:
        moving = True

    screen.fill((0, 0, 0))
    draw_board(level)
    
    draw_player()
    
    targets[3] = (player_x, player_y)
    blinky = Ghost(blinky_x, blinky_y, blinky_img, targets[0], 2, blinky_direction, blinky_dead, False, 0)
    pinky = Ghost(pinky_x, pinky_y, pinky_img, targets[1], 2, pinky_direction, pinky_dead, False, 1)
    inky = Ghost(inky_x, inky_y, inky_img, targets[2], 2, inky_direction, inky_dead, False, 2)
    clyde = Ghost(clyde_x, clyde_y, clyde_img, targets[3], 2, clyde_direction, clyde_dead, False, 3)
    if moving:
        clyde_x = clyde.x_cood
        clyde_y = clyde.y_cood
        clyde_direction = clyde.direction
    
    
    center_x = player_x + 15
    center_y = player_y + 15
    if moving:
        player_x, player_y = move_player(player_x, player_y)
    turns_allowed = check_position(center_x, center_y)
    score, powerups, power_counter, eaten_ghosts = check_collision(score, powerups, power_counter, eaten_ghosts)
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