"""
Tic Tac Toe Player
"""

import math
import copy

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
    # We check the state of the board, if there are more Xs, we know its Os turn 
    # and vice versa
    numX, numO = 0, 0
    for row in board:
        for entry in row:
            if entry == X:
                numX += 1
            elif entry == O:
                numO += 1
    
    return X if numX <= numO else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # We know that its 3x3 board, loop through and find all empty spaces
    available = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                available.add((i, j))
    
    return available


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # deepcopy the board
    resultBoard = copy.deepcopy(board)
    row = action[0]
    col = action[1]

    # out of bounds/invalid move
    if resultBoard[row][col] != EMPTY:
        raise Exception("INVALID MOVE")
    
    if row not in range(3) or col not in range(3):
        raise Exception("INVALID MOVE")
    
    # update new board
    resultBoard[row][col] = player(resultBoard)

    return resultBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows
    for row in range(3):
        if (board[row][0] == board[row][1] == board[row][2]) and board[row][0] != EMPTY:
            return board[row][0]
    
    # check cols
    for col in range(3):
        if (board[0][col] == board[1][col] == board[2][col]) and board[0][col] != EMPTY:
            return board[0][col]
    
    # check diags
    if ((board[0][0] == board[1][1] == board[2][2]) or (board[2][0] == board[1][1] == board[0][2])) and board[1][1] != EMPTY:
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    else:
        if any(EMPTY in row for row in board):
            return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    won = winner(board)

    if won == X:
        return 1
    elif won == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    turn = player(board)

    # if im X, want to calc move for the minValue AI
    if turn == X:
        v = -math.inf
        for action in actions(board):
            score = minValue(result(board, action))
            if score > v:
                v = score
                actionTaken = action
    # if im O, want to calc move for the maxValue AI
    else:
        v = math.inf
        for action in actions(board):
            score = maxValue(result(board, action))
            if score < v:
                v = score
                actionTaken = action
    
    return actionTaken

def maxValue(board):
    """ 
    picks action a in actions(state) that produces highest value of minValue(result(s, a)) -- taken from slides
    """
    if terminal(board):
        return utility(board)
    
    v = -math.inf
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v

def minValue(board):
    """ 
    picks action a in actions(state) that produces smallest value of maxValue(result(s, a)) -- taken from slides
    """
    if terminal(board):
        return utility(board)
    
    v = math.inf
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    return v