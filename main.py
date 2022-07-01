import copy
import time
import constants as key


def initialize_board():
    'returns an initialized othello board with size of 8*8'
    board = [[key.EMPTY for i in range(8)] for j in range(8)]
    board[3][3] = key.BLACK
    board[3][4] = key.WHITE
    board[4][3] = key.WHITE
    board[4][4] = key.BLACK
    return board


def show_board(board):
    'prints the board'
    for i in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'):
        print(" ", i, end="")
    print("")
    for i in range(8):
        for j in range(8):
            if j == 0:
                print(i+1, end="")
            print(board[i][j], "", end="")
        print("")


def no_of_empty_cells(board):
    'returns the number of empty brackets in the board'
    counter = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == key.EMPTY:
                counter = counter + 1
    return counter


def is_empty(board, bracket):
    'returns true if the given bracket is empty else returns false'
    (i, j) = bracket
    if board[i][j] == key.EMPTY:
        return True
    else:
        return False


def is_valid(bracket):
    'returns true if the given bracket is in the board else returns false'
    (i, j) = bracket
    if i in range(8) and j in range(8):
        return True
    else:
        return False


def get_opponent(player):
    'returns the opponent of a player'
    if player is key.WHITE:
        return key.BLACK
    else:
        return key.WHITE


def make_move(move, board, player):
    'changes the board and return it after a player chooses a move'
    (i, j) = move
    board[i][j] = player
    for direction in key.DIRECTIONS:
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


def find_bracket(cell, player, board, direction):
    'returns the bracket b(if available), in a given direction from cell,'
    'such that the player should flip all the brackets in between cell and'
    'b when making a move.'
    bracket = get_cell(cell, direction)
    (i, j) = bracket
    if is_valid(bracket) is False or board[i][j] == player:
        return None
    opponent = get_opponent(player)
    while is_valid(bracket) and board[i][j] == opponent:
        bracket = get_cell(bracket, direction)
        (i, j) = bracket
    if is_valid(bracket) is False or is_empty(board, bracket):
        return None
    else:
        return bracket


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
    return board[i][j] == key.EMPTY and any(map(has_bracket, key.DIRECTIONS))


def has_legal_moves(player, board):
    'returns true if a player has any legal moves on the board'
    'returns false otherwise'
    for i in range(8):
        for j in range(8):
            if is_legal(board, player, (i, j)):
                return True
    return False


def legal_moves(board, player):
    'returns the list of all legal moves for player on the board'
    moves = []
    for i in range(8):
        for j in range(8):
            if is_legal(board, player, (i, j)):
                moves.append((i, j))
    return moves


def no_of_legal_moves(board, player):
    'returns number of all legal moves for player on the board'
    counter = 0
    for i in range(8):
        for j in range(8):
            if is_legal(board, player, (i, j)):
                counter = counter + 1
    return counter


def score(board):
    'returns the score of player on the board'
    score, oppscore = 0, 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == key.WHITE:
                score += 1
            if board[i][j] == key.BLACK:
                oppscore += 1
    return score, oppscore


def print_move_converter(move):
    'converts the real elements location to name of the boards elements '
    (i, j) = move
    j = chr(ord("A") + j)
    i = i+1
    return(i, j)


def input_move_converter(move):
    'converts  name of the boards elements to the real elements location'
    (i, j) = move
    j = int(ord(j) - ord("A"))
    i = i-1
    return(i, j)


def play_othello():
    'plays othello using min max algorithm with alpha beta pruning. returns the final board'

    difficulty_level = int(
        input("please choose a difficulty level\n0 for easy level\n1 for meduim level\n2 for hard level\n"))
    if difficulty_level == 0:
        depth = 3
    elif difficulty_level == 1:
        depth = 7
    elif difficulty_level == 2:
        depth = 11
    else:
        print("please make a wiser decision next time.\n")
        return
    board = initialize_board()
    print("initial board:")
    show_board(board)
    player = key.BLACK
    while player is not None:
        if player == key.WHITE:
            print("\n\nit's your turn please make a valid move. ")
            while True:
                move = (int(input()), input())
                move = input_move_converter(move)
                if is_valid(move) and is_legal(board, player, move):
                    break
                print("you cannot make this move please try again.\n")
        else:
            print("\n\nplease wait for " + str(player) + "  to make a move. ")
            move = min_max_decision_with_pruning(board, depth)
        print("the selected move is = ", print_move_converter(move))
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
    'returns a board after a player makes an action (action is a legal move for a player)'
    'this method does not change the given board'
    new_board = copy.deepcopy(board)
    (i, j) = action
    new_board[i][j] = player
    return new_board


def is_terminal_state(board):
    'returns True if no legal moves can be made on the board'
    return True if has_legal_moves(key.WHITE, board) is False and has_legal_moves(key.BLACK, board) is False else False


def min_max_decision_with_pruning(board, depth):
    'returns an action for the black player (the agent) based on min max algorithm with pruning'

    temp = -float("inf")
    alphabeta = [-float("inf"), float("inf")]
    for action in legal_moves(board, key.BLACK):
        current = min_value_with_pruning(
            result(board, action, key.BLACK), key.BLACK, alphabeta, depth)
        if current > temp:
            selected_action = action
            temp = current
            if temp >= alphabeta[1]:
                break
            if temp > alphabeta[0]:
                alphabeta[0] = temp
    print("the decision is made. to a node with value : ", temp)
    return selected_action


def max_value_with_pruning(board, player, alphabeta, depth):
    'returns the value of max nodes based on min max algorithm with pruning'
    if depth == 0 or is_terminal_state(board) == True:
        return heuristic_evaluation(board, player)

    temp = -float("inf")
    for action in legal_moves(board, player):
        current = min_value_with_pruning(
            result(board, action, player), player, alphabeta, depth - 1)
        if current > temp:
            temp = current
        if temp >= alphabeta[1]:
            return temp
        if temp > alphabeta[0]:
            alphabeta[0] = temp
    return temp


def min_value_with_pruning(board, player, alphabeta, depth):
    'returns the value of min nodes based on min max algorithm with pruning'
    if depth == 0 or is_terminal_state(board) == True:
        return heuristic_evaluation(board, player)

    temp = float("inf")
    opponent = get_opponent(player)
    for action in legal_moves(board, opponent):
        current = max_value_with_pruning(
            result(board, action, opponent), player, alphabeta, depth - 1)
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
    return (key.DISCCOUNTWEIGHT * no_of_discs(board, player)) + (key.MOBILITYWEIGHT * no_of_legal_moves(board, player)) + (key.CORNERWEIGHT * no_of_corners(board, player))


def no_of_discs(board, player):
    'returns number of discs of a player on the board'
    number = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                number += 1
    return number


def no_of_corners(board, player):
    'returns number of discs of a player in the corner of the board'
    number = 0
    if board[0][7] == player:
        number += 1
    if board[7][7] == player:
        number += 1
    if board[7][0] == player:
        number += 1
    if board[0][0] == player:
        number += 1
    return number


start = time.time()
play_othello()
end = time.time()
print("run time :", str(end - start))
