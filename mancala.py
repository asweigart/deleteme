"""MANCALA, by Al Sweigart al@inventwithpython.com
The ancient seed-sowing game."""

import sys

# fmt: off
# Every pit label, in counterclockwise order starting with A:
PIT_LABELS = 'ABCDEF1LKJIHG2'

# A tuple of the player's pits:
PLAYER_1_PITS = ('A', 'B', 'C', 'D', 'E', 'F')
PLAYER_2_PITS = ('G', 'H', 'I', 'J', 'K', 'L')

# A dictionary whose keys are pits and values are opposite pit:
OPPOSITE_PIT = {'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K',
                   'F': 'L', 'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D',
                   'K': 'E', 'L': 'F'}

# A dictionary whose keys are pits and values are the next pit in order:
NEXT_PIT = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
            '1': 'L', 'L': 'K', 'K': 'J', 'J': 'I', 'I': 'H', 'H': 'G',
            'G': '2', '2': 'A'}

# The template string for displaying the board:
BOARD_TEMPLATE = """
+------+--<<<<<-Player 2---+----+----+------+
|2     |G   |H   |I   |J   |K   |L   |1     |
S      | {} | {} | {} | {} | {} | {} |      S
T      |    |    |    |    |    |    |      T
O  {}  +----+----+----+----+----+----+  {}  O
R      |A   |B   |C   |D   |E   |F   |      R
E      | {} | {} | {} | {} | {} | {} |      E
|      |    |    |    |    |    |    |      |
+------+----+---Player 1->>>>>--+----+------+
"""

# How many seeds are in each pit at the start of a new game:
STARTING_NUMBER_OF_SEEDS = 4
# fmt: on


def main():
    """Runs a single game of Mancala."""
    print(
        """MANCALA, by Al Sweigart al@inventwithpython.com

The ancient seed-sowing game. Grab the seeds from a pit on your side
and place one in each following pit, going counterclockwise and
skipping your opponent's store. If your last seed lands in an empty
pit of yours, move the opposite pit's seeds into that pit. The
goal is to get the most seeds in your store on the side of the board.
If the last placed seed is in your store, you get a free turn.

The game ends when all of one player's pits are empty. The other player
claims the remaining seeds for their store, and the winner is the one
with the most seeds.

More info at https://en.wikipedia.org/wiki/Mancala
"""
    )

    gameBoard = getNewBoard()
    playerTurn = '1'  # Player 1 goes first.

    while True:  # Main game loop.
        # Display board and get the player's move:
        displayBoard(gameBoard)
        playerMove = getPlayerMove(playerTurn, gameBoard)

        # Carry out the player's move:
        playerTurn = makeMove(gameBoard, playerTurn, playerMove)

        # Check if the game ended and a player has won:
        winner = checkForWinner(gameBoard)
        if winner == '1' or winner == '2':
            displayBoard(gameBoard)
            print(f'Player {winner} has won!')
            break
        elif winner == 'tie':
            displayBoard(gameBoard)
            print('There is a tie!')
            break


def getNewBoard():
    """Return a dictionary representing a Mancala board in the starting
    state: 4 seeds in each pit and 0 in the stores."""

    # Syntactic sugar - Use a shorter variable name:
    s = STARTING_NUMBER_OF_SEEDS

    # Create the data structure for the board, with 0 seeds in the
    # stores and the starting number of seeds in the pits:
    # fmt: off
    return {'1': 0, '2': 0, 'A': s, 'B': s, 'C': s, 'D': s, 'E': s,
            'F': s, 'G': s, 'H': s, 'I': s, 'J': s, 'K': s, 'L': s}
    # fmt: on


def displayBoard(board):
    """Displays the game board as ASCII-art based on the `board`
    dictionary."""

    seedAmounts = []
    # This 'GHIJKL21ABCDEF' string is the order of the pits left to
    # right and top to bottom:
    for pit in 'GHIJKL21ABCDEF':
        numSeedsInThisPit = str(board[pit]).rjust(2)
        seedAmounts.append(numSeedsInThisPit)

    print(BOARD_TEMPLATE.format(*seedAmounts))


def getPlayerMove(turn, board):
    """Asks the player which pit on their side of the board they
    select to sow seeds from. Returns the uppercase letter label of the
    selected pit as a string."""

    while True:  # Keep asking the player until they enter a valid move.
        # Ask the player to select a pit on their side:
        if turn == '1':
            print('Player 1, choose move: A-F (or QUIT)')
        elif turn == '2':
            print('Player 2, choose move: G-L (or QUIT)')
        pit = input().upper().strip()

        # Check if the player wants to quit:
        if pit == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        # Make sure it is a valid pit to select:
        if (turn == '1' and pit not in PLAYER_1_PITS) or (
            turn == '2' and pit not in PLAYER_2_PITS
        ):
            print('Please pick a letter on your side of the board.')
            continue  # Ask again.
        if board.get(pit) == 0:
            print('Please pick a non-empty pit.')
            continue  # Ask again.
        return pit


def makeMove(board, turn, pit):
    """Modify the `board` data structure so that the player 1 or 2 in `turn`
    selected `pit` as their pit to sow seeds from. Returns either '1'
    or '2' for whose turn it is next."""

    seedsToSow = board[pit]  # Get number of seeds from selected pit.
    board[pit] = 0  # Empty out the selected pit.

    while seedsToSow > 0:  # Continue sowing until we have no more seeds.
        pit = NEXT_PIT[pit]  # Next pit.
        if (turn == '1' and pit == '2') or (turn == '2' and pit == '1'):
            continue  # Skip opponent's store.
        board[pit] += 1  # Add one seed to the pit.
        seedsToSow -= 1  # Decrease one seed from seedsToSow.

    # If the last seed went into the player's store, they go again.
    if (pit == turn == '1') or (pit == turn == '2'):
        return turn  # Last seed in player's store; take another turn.

    # Check if last seed was in an empty pit; take opposite pit's seeds.
    if turn == '1' and pit in PLAYER_1_PITS and board[pit] == 1:
        oppositePit = OPPOSITE_PIT[pit]
        board['1'] += board[oppositePit]
        board[oppositePit] = 0
    elif turn == '2' and pit in PLAYER_2_PITS and board[pit] == 1:
        oppositePit = OPPOSITE_PIT[pit]
        board['2'] += board[oppositePit]
        board[oppositePit] = 0

    # Return the other player as the next player:
    if turn == '1':
        return '2'
    elif turn == '2':
        return '1'


def checkForWinner(board):
    """Looks at `board` and returns either '1' or '2' if there is a
    winner or 'tie' or 'no winner' if there isn't. The game ends when a
    player's pits are all empty; the other player claims the remaining
    seeds for their store. The winner is whoever has the most seeds."""

    b = board  # Make a shorter variable name to use in this function.
    player1Total = b['A'] + b['B'] + b['C'] + b['D'] + b['E'] + b['F']
    player2Total = b['G'] + b['H'] + b['I'] + b['J'] + b['K'] + b['L']

    if player1Total == 0:
        # Player 2 gets all the remaining seeds on their side:
        board['2'] += player2Total
        for pit in PLAYER_2_PITS:
            board[pit] = 0  # Set all pits to 0.
    elif player2Total == 0:
        # Player 1 gets all the remaining seeds on their side:
        board['1'] += player1Total
        for pit in PLAYER_1_PITS:
            board[pit] = 0  # Set all pits to 0.
    else:
        return 'no winner'  # No one has won yet.

    # Game is over, find player with largest score.
    if b['1'] > b['2']:
        return '1'
    elif b['2'] > b['1']:
        return '2'
    else:
        return 'tie'


# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()
