import pygame
import os
import random
import time
import subprocess

pygame.init()

# Configuration
PROGRAM_1 = ['python', 'ia-random.py']
PROGRAM_2 = ['python', 'ia-dummy.py']
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 5
POS_PLAYER_1 = 6
POS_PLAYER_2 = 18
POS_GUN = 20
POS_HEART = 4
AMMO = 5

# State
# 0 empty
# 1 player 1
# 2 player 2
# 3 gun
# 4 heart
# life 1, life 2, gun 1, gun 2
board = [0 for _ in range(GRID_SIZE*GRID_SIZE)]
pos_player1 = POS_PLAYER_1
pos_player2 = POS_PLAYER_2
pos_gun = POS_GUN
pos_heart = POS_HEART
board[pos_player1] = 1
board[pos_player2] = 2
board[pos_gun] = 3
board[pos_heart] = 4
lifes = [9, 9]
bullets = [0, 0]
block = [0, 0]

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT+50))
pygame.display.set_caption("AI turn-based battle")
background = pygame.image.load(os.path.join("images", "background.png")).convert()
player1 = pygame.image.load(os.path.join("images", "palA100.png")).convert_alpha()
player2 = pygame.image.load(os.path.join("images", "palB100.png")).convert_alpha()
gun = pygame.image.load(os.path.join("images", "gun.png")).convert_alpha()
heart = pygame.image.load(os.path.join("images", "heart.png")).convert_alpha()
attack = pygame.image.load(os.path.join("images", "attack.png")).convert_alpha()
defense = pygame.image.load(os.path.join("images", "block.png")).convert_alpha()
player1_turn = random.randint(0, 1)

font = pygame.font.SysFont("comicsans", 20, True)


# Update screen
def updateScreen(status, player1_attack, player2_attack):
    # x,y positions
    player1_xy = [(pos_player1 % GRID_SIZE) * (WIDTH//(GRID_SIZE)), (pos_player1 // GRID_SIZE) * (HEIGHT//(GRID_SIZE))]
    player2_xy = [(pos_player2 % GRID_SIZE) * (WIDTH//(GRID_SIZE)), (pos_player2 // GRID_SIZE) * (HEIGHT//(GRID_SIZE))]
    
    screen.blit(background, (0, 0))
    screen.blit(player1, player1_xy)
    screen.blit(player2, player2_xy)

    # drawing gun if available
    if pos_gun >= 0:
        gun_xy = [(pos_gun % GRID_SIZE) * (WIDTH//(GRID_SIZE)) + 10, (pos_gun // GRID_SIZE) * (HEIGHT//(GRID_SIZE)) + 10]
        screen.blit(gun, gun_xy)

    # drawing heart if available
    if pos_heart >= 0:
        heart_xy = [(pos_heart % GRID_SIZE) * (WIDTH//(GRID_SIZE)) + 15, (pos_heart // GRID_SIZE) * (HEIGHT//(GRID_SIZE)) + 15]
        screen.blit(heart, heart_xy)

    # Health Bar
    healthBarOffset1 = 0
    healthBarOffset2 = 0
    if pos_player1 < GRID_SIZE:
        healthBarOffset1 = 80
    if pos_player2 < GRID_SIZE:
        healthBarOffset2 = 80
    pygame.draw.rect(screen, (255,0,0), (player1_xy[0] + 20, player1_xy[1] - 15 + healthBarOffset1, 45, 10))
    pygame.draw.rect(screen, (0,128,0), (player1_xy[0] + 20, player1_xy[1] - 15 + healthBarOffset1, 45 - (5 * (9 - lifes[0])), 10))
    pygame.draw.rect(screen, (255,0,0), (player2_xy[0] + 20, player2_xy[1] - 15 + healthBarOffset2, 45, 10))
    pygame.draw.rect(screen, (0,128,0), (player2_xy[0] + 20, player2_xy[1] - 15 + healthBarOffset2, 45 - (5 * (9 - lifes[1])), 10))

    # Bullets
    for i in range(bullets[0]):
        pygame.draw.circle(screen, (50,50,50), [player1_xy[0] + 25+i*8, player1_xy[1] - 10], 3, 0)
    for i in range(bullets[1]):
        pygame.draw.circle(screen, (50,50,50), [player2_xy[0] + 25+i*8, player2_xy[1] - 10], 3, 0)

    # Attack
    if player1_attack:
        screen.blit(attack, (player1_xy[0]-100,player1_xy[1]-100))
    elif player2_attack:
        screen.blit(attack, (player2_xy[0]-100,player2_xy[1]-100))

    # Block
    if block[0]:
        screen.blit(defense, (player1_xy[0]-100,player1_xy[1]-100))
    elif block[1]:
        screen.blit(defense, (player2_xy[0]-100,player2_xy[1]-100))

    # set status: text, anti-aliasing, color
    pygame.draw.rect(screen, (0,128,0), (0, 500, WIDTH, 50))
    status = font.render(status, 1, (255,255,255)) 
    screen.blit(status, (20, 500))
    
    pygame.display.flip()


# Update state after a command from a player
# Commands: up, down, left, right, attack, block
def updateState(command):

    global pos_player1, pos_player2, pos_gun, pos_heart, bullets, lifes

    player_index = 0 
    player_xy = [pos_player1 % GRID_SIZE, pos_player1 // GRID_SIZE]
    enemy_xy = [pos_player2 % GRID_SIZE, pos_player2 // GRID_SIZE]
    gun_xy = [pos_gun % GRID_SIZE, pos_gun // GRID_SIZE]
    heart_xy = [pos_heart % GRID_SIZE, pos_heart // GRID_SIZE]

    status = "Jogador 1"
    player1_attack = False
    player2_attack = False

    if not player1_turn:
        player_index = 1
        player_xy = enemy_xy
        enemy_xy = [pos_player1 % GRID_SIZE, pos_player1 // GRID_SIZE]
        status = "Jogador 2"

    block[player_index] = 0

    if command == "up":
        # Impossible to move (out of the bord or enemy in the same place)
        if player_xy[1] == 0 or (player_xy[0] == enemy_xy[0] and player_xy[1]-1 == enemy_xy[1]):
            status += " - Impossível mover"
        else:
            status += " - Moveu para cima"
            # Got a gun?
            if player_xy[0] == gun_xy[0] and player_xy[1]-1 == gun_xy[1]:
                bullets[player_index] += AMMO
                pos_gun = -1
                status += " - Pegou arma"
            # Got a heart?
            if player_xy[0] == heart_xy[0] and player_xy[1]-1 == heart_xy[1]:
                lifes[player_index] = 9
                pos_heart = -1
                status += " - Pegou vida"
            if player1_turn:
                board[pos_player1] = 0
                pos_player1 = pos_player1 - GRID_SIZE
                board[pos_player1] = 1
            else:
                board[pos_player2] = 0
                pos_player2 = pos_player2 - GRID_SIZE
                board[pos_player2] = 2

    if command == "down":
        # Impossible to move (out of the bord or enemy in the same place)
        if player_xy[1] == GRID_SIZE-1 or (player_xy[0] == enemy_xy[0] and player_xy[1]+1 == enemy_xy[1]):
            status += " - Impossível mover"
        else:
            status += " - Moveu para baixo"
            # Got a gun?
            if player_xy[0] == gun_xy[0] and player_xy[1]+1 == gun_xy[1]:
                bullets[player_index] += AMMO
                pos_gun = -1
                status += " - Pegou arma"
            # Got a heart?
            if player_xy[0] == heart_xy[0] and player_xy[1]+1 == heart_xy[1]:
                lifes[player_index] = 9
                pos_heart = -1
                status += " - Pegou vida"
            if player1_turn:
                board[pos_player1] = 0
                pos_player1 = pos_player1 + GRID_SIZE
                board[pos_player1] = 1
            else:
                board[pos_player2] = 0
                pos_player2 = pos_player2 + GRID_SIZE
                board[pos_player2] = 2

    if command == "left":
        # Impossible to move (out of the bord or enemy in the same place)
        if player_xy[0] == 0 or (player_xy[0]-1 == enemy_xy[0] and player_xy[1] == enemy_xy[1]):
            status += " - Impossível mover"
        else:
            status += " - Moveu para esquerda"
            # Got a gun?
            if player_xy[0]-1 == gun_xy[0] and player_xy[1] == gun_xy[1]:
                bullets[player_index] += AMMO
                pos_gun = -1
                status += " - Pegou arma"
            # Got a heart?
            if player_xy[0]-1 == heart_xy[0] and player_xy[1] == heart_xy[1]:
                lifes[player_index] = 9
                pos_heart = -1
                status += " - Pegou vida"
            if player1_turn:
                board[pos_player1] = 0
                pos_player1 = pos_player1 - 1
                board[pos_player1] = 1
            else:
                board[pos_player2] = 0
                pos_player2 = pos_player2 - 1
                board[pos_player2] = 2

    if command == "right":
        # Impossible to move (out of the bord or enemy in the same place)
        if player_xy[0] == GRID_SIZE-1 or (player_xy[0]+1 == enemy_xy[0] and player_xy[1] == enemy_xy[1]):
            status += " - Impossível mover"
        else:
            status += " - Moveu para direita"
            # Got a gun?
            if player_xy[0]+1 == gun_xy[0] and player_xy[1] == gun_xy[1]:
                bullets[player_index] += AMMO
                pos_gun = -1
                status += " - Pegou arma"
            # Got a heart?
            if player_xy[0]+1 == heart_xy[0] and player_xy[1] == heart_xy[1]:
                lifes[player_index] = 9
                pos_heart = -1
                status += " - Pegou vida"
            if player1_turn:
                board[pos_player1] = 0
                pos_player1 = pos_player1 + 1
                board[pos_player1] = 1
            else:
                board[pos_player2] = 0
                pos_player2 = pos_player2 + 1
                board[pos_player2] = 2
    
    elif command == "attack":
        damage = 1

        if player1_turn:
            player1_attack = True
        else:
            player2_attack = True

        # If the player has bullets
        if bullets[player_index] > 0:
            damage = 2
            bullets[player_index] = bullets[player_index] - 1
        
        # Enemy is blocking?
        if block[not player_index]:
            damage = damage - 1

        # Enemy is close?
        if abs(player_xy[0] - enemy_xy[0]) <= 1 and abs(player_xy[1] - enemy_xy[1]) <= 1:
            lifes[not player_index] -= damage
            status += " - Atacou e tirou " + str(damage) + " de vida"
        else:
            status += " - Atacou e errou"
            
    elif command == "block":
        block[player_index] = 1
        status += " - Defendeu"

    return status, player1_attack, player2_attack



updateScreen("Jogo iniciado", False, False)


# Game loop
running = True
while running:

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get command
    parameter = ""
    if player1_turn:
        parameter = PROGRAM_1 + ['1'] + [''.join(str(item) for item in board)] + [str(lifes[0]), str(lifes[1])] + [str(bullets[0]), str(bullets[1])]
    else:
        parameter = PROGRAM_2 + ['2'] + [''.join(str(item) for item in board)] + [str(lifes[0]), str(lifes[1])] + [str(bullets[0]), str(bullets[1])]
    command = subprocess.getoutput(parameter)
    time.sleep(0.3)

    # Updating
    status, player1_attack, player2_attack = updateState(command)
    updateScreen( status, player1_attack, player2_attack )

    # Game Over!
    if lifes[0] <= 0 or lifes[1] <= 0:
        running = False
        updateScreen("Fim de jogo!", False, False)
        time.sleep(5)
        
    player1_turn = not player1_turn


pygame.quit()