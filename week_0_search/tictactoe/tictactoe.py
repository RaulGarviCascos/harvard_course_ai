"""
Tic Tac Toe Player
"""

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
    num_x = 0
    num_o = 0

    for row in board:
        for cell in row:
            if cell == X:
                num_x += 1
            elif cell == O:
                num_o += 1

    if num_x == 0 or num_x == num_o:
        return X
    else:
        return O
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not (0 <= action[0] <= 2 and 0 <= action[1] <= 2):
        raise Exception("Action out of bounds")

    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid action")

    new_board = initial_state()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if i == action[0] and j == action[1]:
                new_board[i][j] = player(board)
            else:
                new_board[i][j] = board[i][j]

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    rows = check_row_or_col(board, row=True)
    if rows: 
        return rows

    cols = check_row_or_col(board, row=False)
    if cols: 
        return cols

    diagonal = check_diagonal(board)
    if diagonal: 
        return diagonal

    
def check_diagonal(board):
    central_cell = board[1][1]
    if central_cell is not None:
        if board[0][0] == central_cell and board[2][2] == central_cell:
            return central_cell
        elif board[0][2] == central_cell and board[2][0] == central_cell:
            return central_cell
    return None


def check_row_or_col(board, row):
    num_x = 0
    num_o = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            cell = board[i][j] if row else board[j][i]
            if cell == X and num_o == 0:
                num_x += 1
            elif cell == O and num_x == 0:
                num_o += 1
            elif num_o > 0 or num_x > 0:
                break
        if num_o == 3: 
            return O
        elif num_x == 3: 
            return X
        else:
            num_o = 0
            num_x = 0

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    finished = is_full(board)
    if not finished:
        finished = True if winner(board) else False
    return finished

    
def is_full(board):
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    finalWinner = winner(board)

    if finalWinner == X:
        return 1
    elif finalWinner == O:
        return -1
    else:
        return 0


def max_value(board, action=None):
    if terminal(board): 
        result_utility = utility(board)
        return result_utility, action

    v = float('-inf')
    
    for current_action in actions(board):
        current_result = result(board, current_action)
        min_v = min_value(current_result, current_action)[0]
        if min_v > v:
            v = min_v
            action = current_action

    return v, action


def min_value(board, action=None):
    if terminal(board): 
        result_utility = utility(board)
        return result_utility, action

    v = float('inf')

    for current_action in actions(board):
        current_result = result(board, current_action)
        max_v = max_value(current_result, current_action)[0]
        if max_v < v:
            v = max_v
            action = current_action

    return v, action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    final_action = None
    if player(board) == X:
        final_action = max_value(board)[1]

    elif player(board) == O:
        final_action = min_value(board)[1]

    return final_action

