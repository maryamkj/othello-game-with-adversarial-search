EMPTY, BLACK, WHITE = 0, 1, 2
DIRECTIONS = ('up', 'down', 'right', 'left', 'upleft', 'upright', 'downleft', 'downright')

def initializeBoard(size):
    board = [[EMPTY for i in range(size)] for j in range(size)]
    if size % 2 != 0:
        print("board can not be initialized. size is odd")
        return
    half = int(size/2)
    board[half][half] = WHITE
    board[half][half+1] = BLACK
    board[half+1][half] = BLACK
    board[half+1][half+1] = WHITE
    return board


def showBoard(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            print(board[i][j], "  ", end="")
        print("")


def isEmpty(board, bracket):
    (i, j) = bracket
    return True if board[i][j] == EMPTY else False


def isValid(board, bracket):
    (i, j) = bracket
    size = len(board)
    return True if 0 <= i < size and 0 <= j < size else False


def getOpponent(player):
    return BLACK if player is WHITE else WHITE


def makeMove(move, board, player):
    (i, j) = move
    board[i][j] = player
    for direction in DIRECTIONS:
        makeFlips(move, player, board, direction)
    return board


def makeFlips(move, player, board, direction):
    bracket = findBracket(move, player, board, direction)
    if not bracket:
        return
    flip = getCell(move, direction)
    while flip != bracket:
        (i, j) = flip
        board[i][j] = player
        flip = getCell(flip, direction)


def getCell(current, direction):
    (i, j) = current
    if direction == 'up':
        return i-1, j
    if direction == 'down':
        return i+1, j
    if direction == 'left':
        return i, j-1
    if direction == 'right':
        return i, j+1
    if direction == 'upright':
        return i-1, j+1
    if direction == 'upleft':
        return i-1, j-1
    if direction == 'downright':
        return i+1, j+1
    if direction == 'downleft':
        return i+1, j-1
    print("invalid direction")
    return None


def findBracket(square, player, board, direction):
    bracket = getCell(square, direction)
    (i, j) = bracket
    if board[i][j] == player:
        return None
    opponent = getOpponent(player)
    while board[i][j] == opponent:
        bracket = getCell(bracket, direction)
        (i, j) = bracket
    return None if isValid(board, bracket) is False or isEmpty(board, bracket) else bracket




# def playOthello():
#     board = initializeBoard(8)
#     player = BLACK
#     while player is not None:
#         move = minmaxDecision(board, player)
#         makeMove(move, board, player)
#         player = nextPlayer(boad, player)
#     return board, score(black, board)
#
#
# def minmaxDecision(board, player):
#     temp = -float("inf")
#     for action in actions(board):
#         if minValue(result(board, action), player) > temp:
#             selectedAction = action
#             temp = minValue(result(board, action), player)
#     return selectedAction
#
#
# def maxValue(board, player):
#     if isTerminalState(board):
#         return utility(board, player)
#     temp = -float("inf")
#     for action in actions(board):
#         if minValue(result(board, action), player) > temp:
#             temp = minValue(result(board, action), player)
#     return temp
#
# def minValue(board, player):
#     if isTerminalState(board):
#         return utility(board, player)
#     temp = float("inf")
#     for action in actions(board):
#         if maxValue((result(board, action), player) < temp:
#             temp = maxValue(result(board, action), player)
#     return temp

showBoard(initializeBoard(8))
move = (0,1)
board = initializeBoard(8)

