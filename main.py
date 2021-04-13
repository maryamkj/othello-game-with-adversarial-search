import copy
import time
EMPTY, BLACK, WHITE = 0, 1, 2
CUTOFF = 50
DIRECTIONS = ('up', 'down', 'right', 'left', 'upleft', 'upright', 'downleft', 'downright')
DISCCOUNTWEIGHT = 0.01
MOBILITYWEIGHT = 1
CORNERWEIGHT = 10

def initializeBoard(size):
    'returns an initialized othello board with the given size'
    board = [[EMPTY for i in range(size)] for j in range(size)]
    if size % 2 != 0:
        raise("board can not be initialized. size is odd")
    half = int(size/2) - 1
    board[half][half] = BLACK
    board[half][half+1] = WHITE
    board[half+1][half] = WHITE
    board[half+1][half+1] = BLACK
    return board


def showBoard(board):
    'prints the board'
    size = len(board)
    for i in range(size):
        for j in range(size):
            print(board[i][j], "  ", end="")
        print("")


def noOfEmptySquares(board):
    'returns the number of empty brackets in the board'
    number = 0
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == EMPTY:
                number += 1
    return number


def isEmpty(board, bracket):
    'returns true if the given bracket is empty else returns false'
    (i, j) = bracket
    return True if board[i][j] == EMPTY else False


def isValid(board, bracket):
    'returns true if the given bracket is in the board else returns false'
    (i, j) = bracket
    size = len(board)
    return True if 0 <= i < size and 0 <= j < size else False


def getOpponent(player):
    'returns the opponent of a player'
    return BLACK if player is WHITE else WHITE


def makeMove(move, board, player):
    'changes the board and return it after a player chooses a move'
    (i, j) = move
    board[i][j] = player
    for direction in DIRECTIONS:
        makeFlips(move, player, board, direction)
    return board


def makeFlips(move, player, board, direction):
    'changes the board and makes flips in a given direction when player chooses a move'
    bracket = findBracket(move, player, board, direction)
    if not bracket:
        return
    flip = getCell(move, direction)
    while flip != bracket:
        (i, j) = flip
        board[i][j] = player
        flip = getCell(flip, direction)


def getCell(current, direction):
    'returns a bracket generated from moving in a given direction from some current bracket'
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
    'returns the bracket b(if available), in a given direction from square,'
    'such that the player should flip all the brackets in between square and'
    'b when making a move.'
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
    'returns the player that should take a turn after player. returns None if game is over'
    opponent = getOpponent(player)
    if hasLegalMoves(opponent, board):
        return opponent
    if hasLegalMoves(player, board):
        return player
    return None


def isLegal(board, player, move):
    'returns true if a given move for a given player on the board is legal(results in flips)'
    'returns false otherwise'
    hasBracket = lambda direction: findBracket(move, player, board, direction)
    (i, j) = move
    return board[i][j] == EMPTY and any(map(hasBracket, DIRECTIONS))


def hasLegalMoves(player, board):
    'returns true if a player has any legal moves on the board'
    'returns false otherwise'
    size = len(board)
    for i in range(size):
        for j in range(size):
            if isLegal(board, player, (i, j)):
                return True
    return False


def legalMoves(board, player):
    'returns the list of all legal moves (brackets) for player on the board'
    moves = []
    size = len(board)
    for i in range(size):
        for j in range(size):
            if isLegal(board, player, (i, j)):
                moves.append((i, j))
    return moves


def showPlayer(player):
    'prints the player name'
    return "White" if player == WHITE else "Black"


def score(board, player):
    'returns the score of player on the board'
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


def playOthello(counter, size=8):
    'plays othello using min max algorithm with alpha beta pruning. returns the final board'
    board = initializeBoard(size)
    print("initial board:")
    showBoard(board)
    player = BLACK
    while player is not None:
        print("turn = ", showPlayer(player))
        move = minmaxDecisionWithPruning(board, player, counter)
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
    print(counter)
    return board


def result (board, action, player):
    'returns a board after a player makes an action (action is a legal move/ bracket for a player)'
    'this method does not change the given board'
    newBoard = copy.deepcopy(board)
    (i, j) = action
    newBoard[i][j] = player
    return newBoard


def isTerminalState(board):
    'returns True if no legal moves can be made on the board'
    return True if hasLegalMoves(WHITE, board) is False and hasLegalMoves(BLACK, board) is False else True


def minmaxDecisionWithPruning(board, player, counter):
    'returns an action for the player based on min max algorithm with pruning'
    count = counter[0]
    counter[0] = count + 1
    temp = -float("inf")
    alphabeta = [-float("inf"), float("inf")]
    for action in legalMoves(board, player):
        if minValueWithPruning(result(board, action, player), player, alphabeta, counter) > temp:
            selectedAction = action
            temp = minValueWithPruning(result(board, action, player), player, alphabeta, counter)
            if temp >= alphabeta[1]:
                break;
            if temp > alphabeta[0]:
                alphabeta[0] = temp
    print("the decision is made. to a node with min value : ", temp)
    return selectedAction


def maxValueWithPruning(board, player, alphabeta, counter):
    'returns the value of max nodes based on min max algorithm with pruning'
    count = counter[0]
    counter[0] = count + 1
    # if isTerminalState(board):
    if noOfEmptySquares(board) <= CUTOFF:
        return heuristicEval(board, player)
        # return score(board, player)
    temp = -float("inf")
    for action in legalMoves(board, player):
        if minValueWithPruning(result(board, action, player), player, alphabeta, counter) > temp:
            temp = minValueWithPruning(result(board, action, player), player, alphabeta, counter)
        if temp >= alphabeta[1]:
            return temp
        if temp > alphabeta[0]:
            alphabeta[0] = temp
    return temp


def minValueWithPruning(board, player, alphabeta, counter):
    'returns the value of min nodes based on min max algorithm with pruning'
    count = counter[0]
    counter[0] = count + 1
    # if isTerminalState(board):
    if noOfEmptySquares(board) <= CUTOFF:
        return heuristicEval(board, player)
        # return score(board, player)
    temp = float("inf")
    opponent = getOpponent(player)
    for action in legalMoves(board, opponent):
        if maxValueWithPruning(result(board, action, opponent), player, alphabeta, counter) < temp:
            temp = maxValueWithPruning(result(board, action, opponent), player, alphabeta, counter)
        if temp <= alphabeta[0]:
            return temp
        if temp < alphabeta[1]:
            alphabeta[1] = temp
    return temp


def heuristicEval(board, player):
    'returns evaluation of the board based on number of discs of the player,'
    'mobility of the player and the number of corner discs of the player'
    return DISCCOUNTWEIGHT * noOfDiscs(board, player) + MOBILITYWEIGHT * len(legalMoves(board, player)) + CORNERWEIGHT * noOfCorners(board, player)


def noOfDiscs(board, player):
    'returns number of discs of a player on the board'
    number = 0
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == player:
                number += 1
    return number


def noOfCorners(board, player):
    'returns number of discs of a player in the corner of the board'
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


start = time.clock()
playOthello([0], 8)
end = time.clock()
print("run time :", str(end - start))
