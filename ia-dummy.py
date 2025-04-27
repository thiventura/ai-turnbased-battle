import sys

GRID_SIZE = 5

# State from parameters
player = int(sys.argv[1])
enemy = 1 if player == 2 else 2
board = sys.argv[2]
life1 = int(sys.argv[3])
life2 = int(sys.argv[4])
bullet1 = int(sys.argv[5])
bullet2 = int(sys.argv[6])

# Mounting matrix board
board = list(board)
res = []
for idx in range(0, len(board) // GRID_SIZE):
    res.append(board[idx * GRID_SIZE : (idx + 1) * GRID_SIZE])
board = [list(map(int, x)) for x in res]

# Getting player and enemy positions
pos_player = []
pos_enemy = []
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        if board[i][j] == player:
            pos_player = [j, i]
        elif board[i][j] == enemy:
            pos_enemy = [j, i]

def pode_mover(x, y):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and board[y][x] in [0, 3, 4]

def esta_cercado(x, y):
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if pode_mover(nx, ny):
            return False
    return True

# If enemy is close, attack
if abs(pos_player[0] - pos_enemy[0]) + abs(pos_player[1] - pos_enemy[1]) == 1:
    print("attack")
else:
    x, y = pos_player
    directions = [
        ("right", x+1, y),
        ("left",  x-1, y),
        ("down",  x, y+1),
        ("up",    x, y-1)
    ]

    # Ordena as direções pela proximidade com o inimigo
    directions.sort(key=lambda d: abs(d[1] - pos_enemy[0]) + abs(d[2] - pos_enemy[1]))

    for dir, nx, ny in directions:
        if pode_mover(nx, ny):
            print(dir)
            break
    else:
        print("block")
