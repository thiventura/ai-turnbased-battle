import pygame
import os
import random
from random import choice, SystemRandom
import time
import subprocess

pygame.init()

# === Configurações ===
PROGRAM_1 = ['python', 'ia-dummy.py']
PROGRAM_2 = ['python', 'ia-random.py']
WIDTH, HEIGHT = 433, 650
GRID_SIZE = 5
AMMO = 5
CELL_WIDTH, CELL_HEIGHT = 65, 65
GRID_OFFSET_X = 56
GRID_OFFSET_Y = 130

# === Estado Inicial ===
valid_moves = list(range(25))
random_gen = SystemRandom()
ARR = []
wins = [0, 0]
running = True
last_status = ""

font = pygame.font.Font("pixel_font.ttf", 12)
bold_font = pygame.font.Font("pixel_font.ttf", 16)

board = [0 for _ in range(GRID_SIZE * GRID_SIZE)]
bullets = [0, 0]
lifes = [9, 9]
block = [0, 0]

def random_pos():
    pos = choice([i for i in valid_moves if i not in ARR])
    ARR.append(pos)
    return pos

def reset_game():
    global pos_player1, pos_player2, pos_gun, pos_heart, bullets, lifes, block, board, player1_turn, running, ARR, last_status
    ARR.clear()
    board[:] = [0 for _ in range(GRID_SIZE * GRID_SIZE)]
    pos_player1 = random_pos()
    pos_player2 = random_pos()
    pos_gun = random_pos()
    pos_heart = random_pos()
    board[pos_player1] = 1
    board[pos_player2] = 2
    board[pos_gun] = 3
    board[pos_heart] = 4
    bullets[:] = [0, 0]
    lifes[:] = [9, 9]
    block[:] = [0, 0]
    player1_turn = random_gen.randint(0, 1)
    last_status = ""
    running = True

reset_game()

# === Carrega Imagens ===
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI turn-based battle")
background = pygame.image.load(os.path.join("images", "background.png")).convert()
player1 = pygame.image.load(os.path.join("images", "naruto.png")).convert_alpha()
player2 = pygame.image.load(os.path.join("images", "sasuke.png")).convert_alpha()
gun = pygame.image.load(os.path.join("images", "chakra.png")).convert_alpha()
heart = pygame.image.load(os.path.join("images", "heart.png")).convert_alpha()
attack_chidori = pygame.image.load(os.path.join("images", "chidori.png")).convert_alpha()
attack_rasengan = pygame.image.load(os.path.join("images", "rasengan.png")).convert_alpha()
defense = pygame.image.load(os.path.join("images", "block.png")).convert_alpha()

# === Funções ===
def draw_life_bar(x, y, life, max_life=9):
    bar_width = 50
    bar_height = 10
    fill = int((life / max_life) * bar_width)
    pygame.draw.rect(screen, (40, 40, 40), (x, y, bar_width, bar_height), border_radius=8)
    pygame.draw.rect(screen, (0, 220, 0) if life > 3 else (220, 0, 0), (x, y, fill, bar_height), border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2, border_radius=8)

def grid_to_pixel(index):
    x = index % GRID_SIZE
    y = index // GRID_SIZE
    return GRID_OFFSET_X + x * CELL_WIDTH, GRID_OFFSET_Y + y * CELL_HEIGHT

def draw_box_with_text(y, text, title="", color=(255, 255, 255), show_icons=False):
    box_width = 320
    box_height = 50
    x = (WIDTH - box_width) // 2
    pygame.draw.rect(screen, (20, 20, 20, 180), (x, y, box_width, box_height), border_radius=10)
    pygame.draw.rect(screen, (255, 120, 0), (x, y, box_width, box_height), width=3, border_radius=10)

    if title:
        title_surface = bold_font.render(title, True, (255, 120, 0))
        screen.blit(title_surface, (x + box_width // 2 - title_surface.get_width() // 2, y + 5))

    if show_icons:
        icon1 = pygame.transform.scale(player1, (25, 25))
        icon2 = pygame.transform.scale(player2, (25, 25))
        screen.blit(icon1, (x + 20, y + 22))
        screen.blit(icon2, (x + box_width - 45, y + 22))

    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x + box_width // 2 - text_surface.get_width() // 2, y + 28))

def updateScreen(status, player1_attack, player2_attack, show_restart=False):
    screen.blit(background, (0, 0))
    p1_xy = grid_to_pixel(pos_player1)
    p2_xy = grid_to_pixel(pos_player2)
    screen.blit(player1, p1_xy)
    screen.blit(player2, p2_xy)

    if pos_gun >= 0:
        g_xy = grid_to_pixel(pos_gun)
        screen.blit(gun, (g_xy[0] + 10, g_xy[1] + 10))
    if pos_heart >= 0:
        h_xy = grid_to_pixel(pos_heart)
        screen.blit(heart, (h_xy[0] + 15, h_xy[1] + 15))

    draw_life_bar(p1_xy[0] + 5, p1_xy[1] - 18, lifes[0])
    draw_life_bar(p2_xy[0] + 5, p2_xy[1] - 18, lifes[1])

    for i in range(bullets[0]):
        pygame.draw.circle(screen, (50, 50, 50), [p1_xy[0] + 25 + i * 8, p1_xy[1] - 5], 3)
    for i in range(bullets[1]):
        pygame.draw.circle(screen, (50, 50, 50), [p2_xy[0] + 25 + i * 8, p2_xy[1] - 5], 3)

    if player1_attack:
        screen.blit(attack_rasengan, p1_xy)
    elif player2_attack:
        screen.blit(attack_chidori, p2_xy)

    if block[0]:
        screen.blit(defense, p1_xy)
    elif block[1]:
        screen.blit(defense, p2_xy)

    draw_box_with_text(510, f"{wins[0]}   VS   {wins[1]}", "PLACAR", show_icons=True)
    draw_box_with_text(570, last_status)

    if show_restart:
        tip = font.render("(ESPAÇO) Reiniciar", True, (255, 255, 255))
        screen.blit(tip, (10, 10))

    pygame.display.flip()

def updateState(command):
    global pos_player1, pos_player2, pos_gun, pos_heart, bullets, lifes
    idx = 0
    p_xy = [pos_player1 % GRID_SIZE, pos_player1 // GRID_SIZE]
    e_xy = [pos_player2 % GRID_SIZE, pos_player2 // GRID_SIZE]
    g_xy = [pos_gun % GRID_SIZE, pos_gun // GRID_SIZE]
    h_xy = [pos_heart % GRID_SIZE, pos_heart // GRID_SIZE]
    status = "J1"
    atk1, atk2 = False, False
    if not player1_turn:
        idx = 1
        p_xy = e_xy
        e_xy = [pos_player1 % GRID_SIZE, pos_player1 // GRID_SIZE]
        status = "J2"
    block[idx] = 0
    dx, dy = 0, 0
    if command == "up": dy = -1
    elif command == "down": dy = 1
    elif command == "left": dx = -1
    elif command == "right": dx = 1
    if dx or dy:
        nx, ny = p_xy[0] + dx, p_xy[1] + dy
        ni = ny * GRID_SIZE + nx
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and ni != (e_xy[1] * GRID_SIZE + e_xy[0]):
            status += f" moveu {command}"
            if [nx, ny] == g_xy:
                bullets[idx] += AMMO
                pos_gun = -1
                status += " +arma"
            if [nx, ny] == h_xy:
                lifes[idx] = 9
                pos_heart = -1
                status += " +vida"
            if player1_turn:
                board[pos_player1] = 0
                pos_player1 = ni
                board[pos_player1] = 1
            else:
                board[pos_player2] = 0
                pos_player2 = ni
                board[pos_player2] = 2
        else:
            status += " mov. inválido"
    elif command == "attack":
        dmg = 1
        if player1_turn: atk1 = True
        else: atk2 = True
        if bullets[idx] > 0:
            dmg = 2
            bullets[idx] -= 1
        if block[not idx]:
            dmg -= 1
        if abs(p_xy[0] - e_xy[0]) <= 1 and abs(p_xy[1] - e_xy[1]) <= 1:
            lifes[not idx] -= dmg
            status += f" atacou (-{dmg})"
        else:
            status += " atacou (errou)"
    elif command == "block":
        block[idx] = 1
        status += " defendeu"
    return status, atk1, atk2

def is_surrounded(pos, enemy_pos):
    x, y = pos % GRID_SIZE, pos // GRID_SIZE
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        idx = ny * GRID_SIZE + nx
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and idx != enemy_pos:
            return False
    return True

# === Loop Principal ===
updateScreen("Jogo iniciado", False, False)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and not running:
                reset_game()
                updateScreen("Novo jogo", False, False)

    if running:
        param = (PROGRAM_1 if player1_turn else PROGRAM_2) + [str(1 if player1_turn else 2)] + ["".join(str(i) for i in board)] + [str(lifes[0]), str(lifes[1]), str(bullets[0]), str(bullets[1])]
        cmd = subprocess.getoutput(param)
        player_pos = pos_player1 if player1_turn else pos_player2
        enemy_pos = pos_player2 if player1_turn else pos_player1
        if is_surrounded(player_pos, enemy_pos) and cmd in ["up", "down", "left", "right"]:
            cmd = "block"
        last_status, a1, a2 = updateState(cmd)
        print(last_status)
        updateScreen(last_status, a1, a2)
        if lifes[0] <= 0:
            wins[1] += 1
            last_status = "J2 VENCEU!"
            print(last_status)
            updateScreen(last_status, False, False, show_restart=True)
            running = False
        elif lifes[1] <= 0:
            wins[0] += 1
            last_status = "J1 VENCEU!"
            print(last_status)
            updateScreen(last_status, False, False, show_restart=True)
            running = False
        player1_turn = not player1_turn
        time.sleep(0.1)
