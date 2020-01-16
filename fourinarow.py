"""FOUR IN A ROW, by Al Sweigart al@inventwithpython.com
A tile-dropping game to get four in a row, similar to Connect Four."""

import sys

# Constants used for displaying the board:
EMPTY_SPACE = '.'
PLAYER_X = 'X'
PLAYER_O = 'O'

# The template string for displaying the board:
BOARD_TEMPLATE = """
     1234567
    +-------+
    |{}{}{}{}{}{}{}|
    |{}{}{}{}{}{}{}|
    |{}{}{}{}{}{}{}|
    |{}{}{}{}{}{}{}|
    |{}{}{}{}{}{}{}|
    |{}{}{}{}{}{}{}|
    +-------+"""


def main():
    """Runs a single game of Four in a Row."""
    print(
        """FOUR IN A ROW, by Al Sweigart al@inventwithpython.com

Two players take turns dropping tiles into one of seven columns, trying
to make four in a row horizontally, vertically, or diagonally.
"""
    )

    # Set up a new game:
    gameBoard = getNewBoard()
    playerTurn = PLAYER_X

    while True:  # Main game loop.
        # Draw board and get player's move:
        displayBoard(gameBoard)
        playerMove = getPlayerMove(playerTurn, gameBoard)
        gameBoard[playerMove] = playerTurn

        # Check for a win or tie:
        if isWinner(playerTurn, gameBoard):
            displayBoard(gameBoard)
            print('Player {} has won!'.format(playerTurn))
            break
        elif isFull(gameBoard):
            displayBoard(gameBoard)
            print('There is a tie!')
            break

        # Switch turns to other player:
        if playerTurn == PLAYER_X:
            playerTurn = PLAYER_O
        elif playerTurn == PLAYER_O:
            playerTurn = PLAYER_X


def getNewBoard():
    """Returns a dictionary that represents a Four in a Row board.

    The keys are (x, y) tuples of two integers, and the values are one
    of the 'X', 'O' or '.' (empty space) strings."""
    board = {}
    for y in range(6):
        for x in range(7):
            board[(x, y)] = EMPTY_SPACE
    return board


def displayBoard(board):
    """Display the board and its tiles on the screen."""

    # Prepare a list to pass to the format() string method for the board
    # template. The list holds all of the board's tiles (and empty
    # spaces) going left to right, top to bottom:
    tileChars = []
    for y in range(6):
        for x in range(7):
            tileChars.append(board[(x, y)])

    # Display the board:
    print(BOARD_TEMPLATE.format(*tileChars))


def getPlayerMove(playerTile, board):
    """Let the player select a column to drop a tile into. Returns a
    tuple of the (column, row) that the tile ends up on."""
    while True:
        print(f'Player {playerTile}, enter 1 to 7 or QUIT:')
        move = input().upper().strip()

        if move == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if move not in ('1', '2', '3', '4', '5', '6', '7'):
            print('Enter a number from 1 to 7.')
            input('Press Enter to continue...')
            continue  # Ask again for their move.

        move = int(move) - 1  # The -1 adjusts for 0-based index.

        # Starting from the bottom, find the first not-occupied space.
        for i in range(5, -1, -1):
            if board[(move, i)] == EMPTY_SPACE:
                return (move, i)
        # At this point, go back to the start of the loop.


def isFull(board):
    """Returns True if the `board` has no empty spaces, otherwise returns
    False."""
    for y in range(6):
        for x in range(7):
            if board[(x, y)] != EMPTY_SPACE:
                return False  # Found an empty space, so return False.
    return True  # All spaces are full.


def isWinner(playerTile, board):
    """Returns True if `playerTile` has four tiles in a row on `board`,
    otherwise returns False."""
    b = board  # Syntactic sugar - a shorter name instead of `board`.

    # Go through the entire board, checking for four-in-a-row:
    for x in range(4):
        for y in range(6):
            # Check for four-in-a-row going across to the right:
            space1 = b[(x, y)]
            space2 = b[(x + 1, y)]
            space3 = b[(x + 2, y)]
            space4 = b[(x + 3, y)]
            if space1 == space2 == space3 == space4 == playerTile:
                return True

    for x in range(7):
        for y in range(3):
            # Check for four-in-a-row going down:
            space1 = b[(x, y)]
            space2 = b[(x, y + 1)]
            space3 = b[(x, y + 2)]
            space4 = b[(x, y + 3)]
            if space1 == space2 == space3 == space4 == playerTile:
                return True

    for x in range(4):
        for y in range(3):
            # Check for four-in-a-row going right-down diagonal:
            space1 = b[(x, y)]
            space2 = b[(x + 1, y + 1)]
            space3 = b[(x + 2, y + 2)]
            space4 = b[(x + 3, y + 3)]
            if space1 == space2 == space3 == space4 == playerTile:
                return True

            # Check for four-in-a-row going left-down diagonal:
            space1 = b[(x + 3, y)]
            space2 = b[(x + 2, y + 1)]
            space3 = b[(x + 1, y + 2)]
            space4 = b[(x, y + 3)]
            if space1 == space2 == space3 == space4 == playerTile:
                return True
    return False


# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()
