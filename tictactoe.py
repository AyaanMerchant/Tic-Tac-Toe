import math  # Importing the math module for mathematical operations
from copy import deepcopy  # Importing the deepcopy function from the copy module
import numpy as np  # Importing the numpy library for numerical operations

X = "X"  # Constant representing player X
O = "O"  # Constant representing player O
EMPTY = None  # Constant representing an empty cell on the board


def initial_state():
    # Returns starting state of the board.
    return [[EMPTY, EMPTY, EMPTY],  # Creating a 3x3 board with all cells initially empty
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


# Helper function to get the diagonal cells of the board
def get_diagonal(board):
    return [[board[0][0], board[1][1], board[2][2]],  # Returns a list containing the main diagonal cells
            [board[0][2], board[1][1], board[2][0]]]  # Returns a list containing the opposite diagonal cells


# Helper function to get the columns of the board
def get_columns(board):
    columns = []

    for i in range(3):
        columns.append([row[i] for row in board])  # Appends each column of the board to the columns list
    return columns  # Returns the list of columns


# Helper function to check if a row has three identical symbols (X or O)
def three_in_a_row(row):
    return True if row.count(
        row[0]) == 3 else False  # Returns True if all elements in the row are the same, False otherwise


def player(board):
    # Returns the player who has the next turn on the board.
    count_x = 0  # Counter for X
    count_o = 0  # Counter for O
    for i in board:  # Iterate over each row of the board
        for j in i:  # Iterate over each element in the row
            if j == "X":  # If the element is X, increment the X counter
                count_x += 1
            if j == "O":  # If the element is O, increment the O counter
                count_o += 1
    return O if count_x > count_o else X  # Returns O if X has made more moves, otherwise returns X


def actions(board):
    # Returns a set of all possible actions (i, j) available on the board.
    action = set()  # Initialize an empty set to store actions
    for i, row in enumerate(board):  # Iterate over each row of the board
        for j, val in enumerate(row):  # Iterate over each element in the row
            if val == EMPTY:  # If the cell is empty, add the action (i, j) to the set of actions
                action.add((i, j))
    return action  # Returns the set of available actions


def result(board, action):
    # Returns the board that results from making move (i, j) on the board.
    i, j = action  # Unpack the action tuple into i and j
    if board[i][j] != EMPTY:  # If the selected cell is not empty, raise an exception
        raise Exception("Invalid Move")
    next_move = player(board)  # Get the next player's move
    deep_board = deepcopy(board)  # Create a deep copy of the board to avoid modifying the original board
    deep_board[i][j] = next_move  # Make the move on the deep copy of the board
    return deep_board  # Returns the resulting board after making the move


def winner(board):
    rows = board + get_diagonal(board) + get_columns(board)  # Concatenate rows, diagonals, and columns
    for row in rows:  # Iterate over each row, diagonal, and column
        current_player = row[0]  # Get the first element of the row (assuming all elements are the same)
        if current_player is not None and three_in_a_row(row):  # If the row has three identical symbols and not empty
            return current_player  # Return the current player as the winner
    return None  # If no player has won, return None


def terminal(board):
    # Returns True if the game is over, False otherwise.
    xx = winner(board)  # Check if there is a winner
    if xx is not None:  # If there is a winner, the game is over
        return True
    if all(all(j != EMPTY for j in i) for i in board):  # If all cells are filled, the game is over
        return True
    return False


def utility(board):
    # Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    xx = winner(board)  # Get the winner
    if xx == X:  # If X is the winner, return 1
        return 1
    elif xx == O:  # If O is the winner, return -1
        return -1
    else:  # If no one has won, return 0
        return 0


# Helper function for alpha-beta pruning
def max_alpha_beta_pruning(board, alpha, beta):
    if terminal(board):  # If the game is over, return the utility value and None
        return utility(board), None
    vall = float("-inf")  # Initialize the value to negative infinity
    best = None  # Initialize the best action to None
    for action in actions(board):  # Iterate over available actions
        min_val = min_alpha_beta_pruning(result(board, action), alpha, beta)[
            0]  # Get the minimum value from the opponent's turn
        if min_val > vall:  # If the minimum value is greater than the current maximum value
            best = action  # Update the best action
            vall = min_val  # Update the maximum value
        alpha = max(alpha, vall)  # Update the alpha value
        if beta <= alpha:  # If beta is less than or equal to alpha, break the loop (pruning)
            break
    return vall, best  # Return the maximum value and the best action


def min_alpha_beta_pruning(board, alpha, beta):
    if terminal(board):  # If the game is over, return the utility value and None
        return utility(board), None
    vall = float("inf")  # Initialize the value to positive infinity
    best = None  # Initialize the best action to None
    for action in actions(board):  # Iterate over available actions
        max_val = max_alpha_beta_pruning(result(board, action), alpha, beta)[
            0]  # Get the maximum value from the opponent's turn
        if max_val < vall:  # If the maximum value is smaller than the current minimum value
            best = action  # Update the best action
            vall = max_val  # Update the minimum value
        beta = min(beta, vall)  # Update the beta value
        if beta <= alpha:  # If beta is less than or equal to alpha, break the loop (pruning)
            break
    return vall, best  # Return the minimum value and the best action


def minimax(board):
    # Returns the optimal action for the current player on the board.
    if terminal(board):  # If the game is over, return None
        return None
    if player(board) == X:  # If it's player X's turn
        return max_alpha_beta_pruning(board, float("-inf"), float("inf"))[
            1]  # Find the optimal action using max_alpha_beta_pruning
    elif player(board) == O:  # If it's player O's turn
        return min_alpha_beta_pruning(board, float("-inf"), float("inf"))[
            1]  # Find the optimal action using min_alpha_beta_pruning
    else:
        raise Exception(
            "Error in Calculating Optimal Move")  # Raise an exception if the current player is neither X nor O
