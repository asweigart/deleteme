"""THE TOWER OF HANOI, by Al Sweigart al@inventwithpython.com
A stack-moving puzzle game."""

import copy
import sys

# Set up towers A, B, and C. The end of the list is the top of the tower.
TOTAL_DISKS = 5

# Start with all disks on tower A:
COMPLETE_TOWER = list(reversed(range(1, TOTAL_DISKS + 1)))


def main():
    """Runs a single game of The Tower of Hanoi."""
    print(
        """THE TOWER OF HANOI, by Al Sweigart al@inventwithpython.com

Move the tower of disks, one disk at a time, to another pole. Larger
disks cannot rest on top of a smaller disk.

More info at https://en.wikipedia.org/wiki/Tower_of_Hanoi
"""
    )

    towers = {'A': copy.copy(COMPLETE_TOWER), 'B': [], 'C': []}

    while True:  # Main program loop.
        # Display the poles and disks:
        displayPoles(towers)

        # Ask the user for a move:
        fromPole, toPole = getPlayerMove(towers)

        # Move the top disk from fromPole to toPole:
        disk = towers[fromPole].pop()
        towers[toPole].append(disk)

        # Check if the user has solved the puzzle:
        if COMPLETE_TOWER in (towers['B'], towers['C']):
            displayPoles(towers)  # Display the poles one last time.
            print('You have solved the puzzle! Well done!')
            sys.exit()


def getPlayerMove(towers):
    """Ask the player which disk to move. Returns a two-string tuple
    (fromPole, toPole) where the "poles" are 'A', 'B', or 'C'."""
    while True:
        # Keep asking player until they enter a valid move:
        print('Enter the letters of "from" and "to" poles, or QUIT.')
        print('(e.g. AB to moves a disk from pole A to pole B.)')
        print()
        playerMove = input().upper().strip()

        if playerMove == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        # Make sure the user entered valid tower letters:
        if playerMove not in ('AB', 'AC', 'BA', 'BC', 'CA', 'CB'):
            print('Enter one of AB, AC, BA, BC, CA, or CB.')
            input('Press Enter to continue...')
            continue

        # Syntactic sugar - Use more descriptive variable names:
        fromPole, toPole = playerMove[0], playerMove[1]

        # Make sure there is at least one disk on the "from" pole:
        if len(towers[fromPole]) == 0:
            print('You selected a pole with no disks.')
            input('Press Enter to continue...')
            continue

        # Any disk can be moved onto an empty "to" pole:
        if len(towers[toPole]) == 0:
            return fromPole, toPole

        # Make sure the topmost disk on the "from" pole is smaller than
        # the topmost disk on the "to" pole:
        if towers[toPole][-1] < towers[fromPole][-1]:
            print('Can\'t put larger disks on top of smaller ones.')
            input('Press Enter to continue...')
            continue

        return fromPole, toPole


def displayDisk(width):
    """Display a single disk of the given width."""
    emptySpace = ' ' * (TOTAL_DISKS - width)

    if width == 0:
        # Just draw a pole segment without a disk.
        print(f'{emptySpace}||{emptySpace}', end='')
    else:
        # Draw the disk.
        disk = '@' * width
        numLabel = str(width).rjust(2, '_')
        print(emptySpace + disk + numLabel + disk + emptySpace, end='')


def displayPoles(towers):
    """Display the current state."""

    # Draw the three poles, with disks:
    for level in range(TOTAL_DISKS, -1, -1):
        for tower in (towers['A'], towers['B'], towers['C']):
            if level >= len(tower):
                displayDisk(0)  # Display the bare pole with no disk.
            else:
                displayDisk(tower[level])  # Display the disk.
        print()

    # Display the pole labels A, B, and C.
    emptySpace = ' ' * (TOTAL_DISKS)
    print('{0} A{0}{0} B{0}{0} C\n'.format(emptySpace))


# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()
