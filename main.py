import copy

EMPTY, BLACK, WHITE = 0, 1, 2
CUTOFF = 14
DIRECTIONS = ('up', 'down', 'right', 'left', 'upleft', 'upright', 'downleft', 'downright')
DISCCOUNTWEIGHT = 0.01
MOBILITYWEIGHT = 1
CORNERWEIGHT = 10


def initializeBoard(size):
    board = [[EMPTY for i in range(size)] for j in range(size)]
    if size % 2 != 0:
        print("board can not be initialized. size is odd")
        return
    half = int(size/2) - 1
    board[half][half] = BLACK
    board[half][half+1] = WHITE
    board[half+1][half] = WHITE
    board[half+1][half+1] = BLACK
    return board


def showBoard(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            print(board[i][j], "  ", end="")
        print("")


def noOfEmptySquares(board):
    number = 0
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == EMPTY:
                number += 1
    return number


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
    'finds a bracket for the player on the board on a given direction from a square(ke vasatesho por kone)'
    bracket = getCell(square, direction)
    (i, j) = bracket
    if isValid(board, bracket) is False or board[i][j] == player:
        return None
    opponent = getOpponent(player)
    while isValid(board, bracket) and board[i][j] == opponent:
        bracket = getCell(bracket, direction)
        (i, j) = bracket
    return None if isValid(board, bracket) is False or isEmpty(board, bracket) else bracket


def nextPlayer(board, player):
    opponent = getOpponent(player)
    if hasLegalMoves(opponent, board):
        return opponent
    if hasLegalMoves(player, board):
        return player
    return None


def isLegal(board, player, move):
    hasBracket = lambda direction: findBracket(move, player, board, direction)
    (i, j) = move
    return board[i][j] == EMPTY and any(map(hasBracket, DIRECTIONS))


def hasLegalMoves(player, board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if isLegal(board, player, (i, j)):
                return True
    return False


def legalMoves(board, player):
    moves = []
    size = len(board)
    for i in range(size):
        for j in range(size):
            if isLegal(board, player, (i, j)):
                moves.append((i, j))
    'liste zoje morateb haaE ke player mitune unja bere'
    return moves


def showPlayer(player):
    return "White" if player == WHITE else "Black"


def score(board, player):
    score, oppscore = 0, 0
    opponent = getOpponent(player)
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == player:
                score += 1
            if board[i][j] == opponent:
                oppscore += 1
    score = score - oppscore
    return score


def playOthello():
    board = initializeBoard(8)
    print("initial board:")
    showBoard(board)
    player = BLACK
    while player is not None:
        print("turn = ", showPlayer(player))
        move = minmaxDecision(board, player)
        print("the selected move is = ", move)
        'pas minmax bayad khuneE ke mikhaym berim behesh ro bargardune'
        makeMove(move, board, player)
        print("board after the selected move")
        showBoard(board)
        player = nextPlayer(board, player)
    print("no legal moves available.")
    showBoard(board)
    print("white's score =", score(board, WHITE))
    print("black's score =", score(board, BLACK))
    return board


def result (board, action, player):
    'action is a legal move. legal moves are zoje moratab haaE ke mishe be unja raft'
    'mikhaym bebinim result esh chi mishe'
    'board ro taghir nade'
    newBoard = copy.deepcopy(board)
    (i, j) = action
    newBoard[i][j] = player
    return newBoard


def minmaxDecision(board, player):
    temp = -float("inf")
    for action in legalMoves(board, player):
        if minValue(result(board, action, player), player) > temp:
            selectedAction = action
            temp = minValue(result(board, action, player), player)
    return selectedAction


def isTerminalState(board):
    return True if hasLegalMoves(WHITE, board) is False and hasLegalMoves(BLACK, board) is False else True


def maxValue(board, player):
    # if isTerminalState(board):
    if noOfEmptySquares(board) <= CUTOFF or  isTerminalState(board):
        return heuristicEval(board, player)
        # return score(board, player)
    temp = -float("inf")
    for action in legalMoves(board, player):
        if minValue(result(board, action), player) > temp:
            temp = minValue(result(board, action), player)
    return temp


def minValue(board, player):
    # if isTerminalState(board):
    if noOfEmptySquares(board) <= CUTOFF or  isTerminalState(board):
        return heuristicEval(board, player)
        # return score(board, player)
    temp = float("inf")
    for action in legalMoves(board, getOpponent(player)):
        if maxValue((result(board, action), player)) < temp:
            temp = maxValue(result(board, action), player)
    return temp


def heuristicEval(board, player):
    return DISCCOUNTWEIGHT * noOfDiscs(board, player) + MOBILITYWEIGHT * len(legalMoves(board, player)) + CORNERWEIGHT * noOfCorners(board, player)


def noOfDiscs(board, player):
    number = 0
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == player:
                number += 1
    return number


def noOfCorners(board, player):
    max = len(board) - 1
    number = 0
    if board[0][max] == player:
        number += 1
    if board[max][max] == player:
        number += 1
    if board[max][0] == player:
        number += 1
    if board[0][0] == player:
        number += 1
    return number





playOthello()

