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
    # 評估所有空格的威脅與機會
    best_move = None
    best_score = -1

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != 0:
                continue

            # 優先評估玩家的威脅
            board[r][c] = 2  # 假裝玩家下這裡
            if checkWin(r, c, 2):
                board[r][c] = 0
                board[r][c] = 1  # 搶先一步阻止玩家贏
                return r, c
            block_score = evaluate_potential(r, c, 2)  # 玩家潛力（越高越危險）
            board[r][c] = 0

            # 評估自己進攻潛力
            board[r][c] = 1  # 假裝 CPU 自己下
            win_score = evaluate_potential(r, c, 1)
            board[r][c] = 0

            # 給分邏輯：阻擋分比進攻分略高，避免防不住
            total_score = block_score * 1.2 + win_score

            if total_score > best_score:
                best_score = total_score
                best_move = (r, c)

    if best_move:
        r, c = best_move
        down(r, c, is_player=False)
        return r, c

    # fallback：亂下
    while True:
        r = random.randint(0, BOARD_SIZE - 1)
        c = random.randint(0, BOARD_SIZE - 1)
        if down(r, c, is_player=False):
            return r, c
        
def evaluate_potential(row, col, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    score = 0

    for dr, dc in directions:
        count = 1  # 該點自己也算一子
        for i in range(1, 5):
            nr, nc = row + dr*i, col + dc*i
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            nr, nc = row - dr*i, col - dc*i
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == player:
                count += 1
            else:
                break

        # 加權得分機制（可依需求微調）
        if count == 2:
            score += 5
        elif count == 3:
            score += 15
        elif count == 4:
            score += 100
        elif count >= 5:
            score += 999
    return score


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