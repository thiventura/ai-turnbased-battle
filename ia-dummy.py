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
            pos_player = [j,i]
        elif board[i][j] == enemy:
            pos_enemy = [j,i]

# If enemy is close, attack
if abs(pos_player[0] - pos_enemy[0]) <= 1 and abs(pos_player[1] - pos_enemy[1]) <= 1:
    print("attack")

# If not, move to the enemy
else:
    if pos_player[0] < pos_enemy[0]:
        print("right")
    elif pos_player[0] > pos_enemy[0]:
        print("left")
    elif pos_player[1] < pos_enemy[1]:
        print("down")
    else:
        print("up")
