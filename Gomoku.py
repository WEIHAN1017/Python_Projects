import os
import random

BOARD_SIZE = 15
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def showBoard():
    os.system("cls")
    print("  " + " ".join([str(i).rjust(2) for i in range(1, BOARD_SIZE + 1)]))
    for r in range(0, len(board)):
        data = str(r + 1).rjust(2)
        for c in range(0, len(board[r])):
            if board[r][c] == 0:
                data += " . "
            elif board[r][c] == 1:
                data += " X "
            else:
                data += " O "
        print(data)

def down(row, col, is_player):
    if board[row][col] != 0:
        return False  # 如果已有棋子，回傳 False
    board[row][col] = 2 if is_player else 1
    return True

def playerRound():
    while True:
        player_input = input("你是 O 子，請輸入列行來下子，例如: 18 表示第 1 列第 8 行：")
        if len(player_input) < 2 or not player_input.isdigit():
            print("❌ 輸入錯誤！請重新輸入兩位數字，例如 57。")
            continue
        row = int(player_input[0]) - 1
        col = int(player_input[1]) - 1
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            if down(row, col, is_player=True):
                return row, col
            else:
                print("⚠️ 此處已有棋子！請重新選擇位置。")
        else:
            print("⚠️ 座標超出棋盤範圍，請重新輸入！")

def checkWin(row, col, player):
    directions = [(1,0), (0,1), (1,1), (1,-1)]  # 四個方向：垂直、水平、兩個對角
    for dr, dc in directions:
        count = 1
        # 向正方向檢查
        for i in range(1, 5):
            nr, nc = row + dr*i, col + dc*i
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                count += 1
            else:
                break
        # 向反方向檢查
        for i in range(1, 5):
            nr, nc = row - dr*i, col - dc*i
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

def CPURound():
    while True:
        row = random.randint(0, BOARD_SIZE - 1)
        col = random.randint(0, BOARD_SIZE - 1)
        if down(row, col, is_player=False):
            return row, col

def playGame():
    while True:
        showBoard()
        prow, pcol = playerRound()
        if checkWin(prow, pcol, player=2):
            showBoard()
            print("🎉 恭喜，你贏了！")
            break
        crow, ccol = CPURound()
        if checkWin(crow, ccol, player=1):
            showBoard()
            print("😢 哎呀，你輸了。")
            break

# 啟動遊戲
playGame()