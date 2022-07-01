import copy
import time
EMPTY, WHITE, BLACK = '🟩', '⬜', '⬛'
CUTOFF = 50
DIRECTIONS = ('up', 'down', 'right', 'left', 'upleft',
              'upright', 'downleft', 'downright')
DISCCOUNTWEIGHT = 0.01
MOBILITYWEIGHT = 1
CORNERWEIGHT = 10


def initialize_board(size):
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


def show_board(board):
    'prints the board'
    size = len(board)
    for i in range(size):
        for j in range(size):
            print(board[i][j], "", end="")
        print("")


def no_of_empty_squares(board):
    'returns the number of empty brackets in the board'
    number = 0
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == EMPTY:
                number += 1
    return number


def is_empty(board, bracket):
    'returns true if the given bracket is empty else returns false'
    (i, j) = bracket
    if board[i][j] == EMPTY:
        return True
    else:
        return False


def is_valid(board, bracket):
    'returns true if the given bracket is in the board else returns false'
    (i, j) = bracket
    size = len(board)
    if i in range(0, size) and j in range(0, size):
        return True
    else:
        return False


def get_opponent(player):
    'returns the opponent of a player'
    if player is WHITE:
        return BLACK
    else:
        return WHITE


def make_move(move, board, player):
    'changes the board and return it after a player chooses a move'
    (i, j) = move
    board[i][j] = player
    for direction in DIRECTIONS:
        make_flips(move, player, board, direction)
    return board


def make_flips(move, player, board, direction):
    'changes the board and makes flips in a given direction when player chooses a move'
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    flip = get_cell(move, direction)
    while flip != bracket:
        (i, j) = flip
        board[i][j] = player
        flip = get_cell(flip, direction)


def get_cell(current, direction):
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


def find_bracket(square, player, board, direction):
    'returns the bracket b(if available), in a given direction from square,'
    'such that the player should flip all the brackets in between square and'
    'b when making a move.'
    bracket = get_cell(square, direction)
    (i, j) = bracket
    if is_valid(board, bracket) is False or board[i][j] == player:
        return None
    opponent = get_opponent(player)
    while is_valid(board, bracket) and board[i][j] == opponent:
        bracket = get_cell(bracket, direction)
        (i, j) = bracket
    return None if is_valid(board, bracket) is False or is_empty(board, bracket) else bracket


def next_player(board, player):
    'returns the player that should take a turn after player. returns None if game is over'
    opponent = get_opponent(player)
    if has_legal_moves(opponent, board):
        return opponent
    if has_legal_moves(player, board):
        return player
    return None


def is_legal(board, player, move):
    'returns true if a given move for a given player on the board is legal(results in flips)'
    'returns false otherwise'
    def has_bracket(direction):
        return find_bracket(move, player, board, direction)
    (i, j) = move
    return board[i][j] == EMPTY and any(map(has_bracket, DIRECTIONS))


def has_legal_moves(player, board):
    'returns true if a player has any legal moves on the board'
    'returns false otherwise'
    size = len(board)
    for i in range(size):
        for j in range(size):
            if is_legal(board, player, (i, j)):
                return True
    return False


def legal_moves(board, player):
    'returns the list of all legal moves (brackets) for player on the board'
    moves = []
    size = len(board)
    for i in range(size):
        for j in range(size):
            if is_legal(board, player, (i, j)):
                moves.append((i, j))
    return moves


def score(board):
    'returns the score of player on the board'
    score, oppscore = 0, 0
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == WHITE:
                score += 1
            if board[i][j] == BLACK:
                oppscore += 1
    return score, oppscore


def play_othello(size=8):
    'plays othello using min max algorithm with alpha beta pruning. returns the final board'
    board = initialize_board(size)
    print("initial board:")
    show_board(board)
    player = BLACK
    while player is not None:
        print("\n\nplease wait for " + str(player) + "  to make a move ")
        move = min_max_decision_with_pruning(board, player)
        print("the selected move is = ", move)
        'minmax returns the location of the place we want to move in'
        make_move(move, board, player)
        print("board after the selected move:")
        show_board(board)
        player = next_player(board, player)
    print("no legal moves available.")
    show_board(board)
    white_score, black_score = score(board)
    print("white's score =", white_score)
    print("black's score =", black_score)
    return board


def result(board, action, player):
    'returns a board after a player makes an action (action is a legal move/ bracket for a player)'
    'this method does not change the given board'
    newBoard = copy.deepcopy(board)
    (i, j) = action
    newBoard[i][j] = player
    return newBoard


def is_terminal_state(board):
    'returns True if no legal moves can be made on the board'
    return True if has_legal_moves(WHITE, board) is False and has_legal_moves(BLACK, board) is False else True


def min_max_decision_with_pruning(board, player):
    'returns an action for the player based on min max algorithm with pruning'
    temp = -float("inf")
    alphabeta = [-float("inf"), float("inf")]
    for action in legal_moves(board, player):
        current = min_value_with_pruning(
            result(board, action, player), player, alphabeta)
        if current > temp:
            selected_action = action
            temp = current
            if temp >= alphabeta[1]:
                break
            if temp > alphabeta[0]:
                alphabeta[0] = temp
    print("the decision is made. to a node with value : ", temp)
    return selected_action


def max_value_with_pruning(board, player, alphabeta):
    'returns the value of max nodes based on min max algorithm with pruning'
    if no_of_empty_squares(board) <= CUTOFF:
        return heuristic_evaluation(board, player)
    temp = -float("inf")
    for action in legal_moves(board, player):
        current = min_value_with_pruning(
            result(board, action, player), player, alphabeta)
        if current > temp:
            temp = current
        if temp >= alphabeta[1]:
            return temp
        if temp > alphabeta[0]:
            alphabeta[0] = temp
    return temp


def min_value_with_pruning(board, player, alphabeta):
    'returns the value of min nodes based on min max algorithm with pruning'
    if no_of_empty_squares(board) <= CUTOFF:
        return heuristic_evaluation(board, player)

    temp = float("inf")
    opponent = get_opponent(player)
    for action in legal_moves(board, opponent):
        current = max_value_with_pruning(
            result(board, action, opponent), player, alphabeta)
        if current < temp:
            temp = current
        if temp <= alphabeta[0]:
            return temp
        if temp < alphabeta[1]:
            alphabeta[1] = temp
    return temp


def heuristic_evaluation(board, player):
    'returns evaluation of the board based on number of discs of the player,'
    'mobility of the player and the number of corner discs of the player'
    return DISCCOUNTWEIGHT * no_of_discs(board, player) + MOBILITYWEIGHT * len(legal_moves(board, player)) + CORNERWEIGHT * no_of_corners(board, player)


def no_of_discs(board, player):
    'returns number of discs of a player on the board'
    number = 0
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == player:
                number += 1
    return number


def no_of_corners(board, player):
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


start = time.time()
play_othello(8)
end = time.time()
print("run time :", str(end - start))
