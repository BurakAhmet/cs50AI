"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X

    total = 0
    for row in board:
        total += row.count(X) + row.count(O)
    if total % 2 == 1:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] is EMPTY:
                actions_set.add((row, col))
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row, col = action
    if board[row][col] != EMPTY:
        raise IndexError("Invalid index")
    new_board = copy.deepcopy(board)
    if player(board) == X:
        new_board[row][col] = X
    else:
        new_board[row][col] = O

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    board_length = len(board)

    # left diagonal
    all_same = True
    move = board[0][0]
    for i in range(board_length):
        if move != board[i][i]:
            all_same = False
            break
    if all_same:
        return move

    # right diagonal
    all_same = True
    move = board[0][board_length - 1]
    for i in range(board_length):
        if move != board[i][board_length - 1 - i]:
            all_same = False
            break
    if all_same:
        return move

    # horizontally
    for row in board:
        move = row[0]
        if row.count(move) == len(row):
            return move

    # vertically
    for col in range(board_length):
        all_same = True
        move = board[0][col]
        for row in range(board_length):
            if move != board[row][col]:
                all_same = False
                break
        if all_same:
            return move

    return None  # tie or the game is in progress


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    is_full = True
    for row in board:
        if EMPTY in row:
            is_full = False
            break
    if is_full:
        return True

    return winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    victor = winner(board)
    if victor == X:
        return 1
    elif victor == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        return maximize(board)[1]
    return minimize(board)[1]


def maximize(board):
    if terminal(board):
        return [utility(board), None]
    best_score = -math.inf
    best_move = None
    for move in actions(board):
        score = max(best_score, minimize(result(board, move))[0])
        if score > best_score:
            best_score = score
            best_move = move
    return [best_score, best_move]


def minimize(board):
    if terminal(board):
        return [utility(board), None]
    best_score = math.inf
    best_move = None
    for move in actions(board):
        score = min(best_score, maximize(result(board, move))[0])
        if score < best_score:
            best_score = score
            best_move = move
    return [best_score, best_move]
