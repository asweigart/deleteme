"""FOUR IN A ROW, by Al Sweigart al@inventwithpython.com
A tile-dropping game to get four in a row, similar to Connect Four."""

import sys

# Constants used for displaying the board:
EMPTY_SPACE = '.'
PLAYER_X = 'X'
PLAYER_O = 'O'

# Note: Update BOARD_TEMPLATE if BOARD_WIDTH is changed.
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
COLUMN_LABELS = tuple([str(n) for n in range(1, BOARD_WIDTH + 1)])
assert len(COLUMN_LABELS) == BOARD_WIDTH

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

    while True:  # Run a player's turn.
        # Display the board and get player's move:
        displayBoard(gameBoard)
        playerMove = getPlayerMove(playerTurn, gameBoard)
        gameBoard[playerMove] = playerTurn

        # Check for a win or tie:
        if isWinner(playerTurn, gameBoard):
            displayBoard(gameBoard)  # Display the board one last time.
            print('Player {} has won!'.format(playerTurn))
            sys.exit()
        elif isFull(gameBoard):
            displayBoard(gameBoard)  # Display the board one last time.
            print('There is a tie!')
            sys.exit()
        else:
            pass  # Game hasn't ended, simply go on to the next turn.

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
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            board[(x, y)] = EMPTY_SPACE
    return board


def displayBoard(board):
    """Display the board and its tiles on the screen."""

    # Prepare a list to pass to the format() string method for the board
    # template. The list holds all of the board's tiles (and empty
    # spaces) going left to right, top to bottom:
    tileChars = []
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            tileChars.append(board[(x, y)])

    # Display the board:
    print(BOARD_TEMPLATE.format(*tileChars))


def getPlayerMove(playerTile, board):
    """Let the player select a column on the board to drop a tile (either
    'X' or 'O' into. Returns a tuple of the (column, row) that the tile
    ends up on."""
    while True:  # Keep asking player until they enter a valid move.
        print(f'Player {playerTile}, enter 1 to {BOARD_WIDTH} or QUIT:')
        move = input('> ').upper().strip()

        if move == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if move not in COLUMN_LABELS:
            print(f'Enter a number from 1 to {BOARD_WIDTH}.')
            input('Press Enter to continue...')
            continue  # Ask player again for their move.

        move = int(move) - 1  # The -1 adjusts for 0-based index.

        # Starting from the bottom, find the first empty space.
        for i in range(BOARD_HEIGHT - 1, -1, -1):
            if board[(move, i)] == EMPTY_SPACE:
                return (move, i)


def isFull(board):
    """Returns True if the `board` has no empty spaces, otherwise
    returns False."""
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[(x, y)] != EMPTY_SPACE:
                return False  # Found an empty space, so return False.
    return True  # All spaces are full.


def isWinner(playerTile, board):
    """Returns True if `playerTile` has four tiles in a row on `board`,
    otherwise returns False."""

    # Go through the entire board, checking for four-in-a-row:
    for x in range(BOARD_WIDTH - 3):
        for y in range(BOARD_HEIGHT - 1):
            # Check for four-in-a-row going across to the right:
            space1 = board[(x, y)]
            space2 = board[(x + 1, y)]
            space3 = board[(x + 2, y)]
            space4 = board[(x + 3, y)]
            if space1 == space2 == space3 == space4 == playerTile:
                return True

    for x in range(BOARD_WIDTH - 1):
        for y in range(BOARD_HEIGHT - 3):
            # Check for four-in-a-row going down:
            space1 = board[(x, y)]
            space2 = board[(x, y + 1)]
            space3 = board[(x, y + 2)]
            space4 = board[(x, y + 3)]
            if space1 == space2 == space3 == space4 == playerTile:
                return True

    for x in range(BOARD_WIDTH - 3):
        for y in range(BOARD_HEIGHT - 3):
            # Check for four-in-a-row going right-down diagonal:
            space1 = board[(x, y)]
            space2 = board[(x + 1, y + 1)]
            space3 = board[(x + 2, y + 2)]
            space4 = board[(x + 3, y + 3)]
            if space1 == space2 == space3 == space4 == playerTile:
                return True

            # Check for four-in-a-row going left-down diagonal:
            space1 = board[(x + 3, y)]
            space2 = board[(x + 2, y + 1)]
            space3 = board[(x + 1, y + 2)]
            space4 = board[(x, y + 3)]
            if space1 == space2 == space3 == space4 == playerTile:
                return True
    return False


# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()
