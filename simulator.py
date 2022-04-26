from globalSetting import *

# how many rotations of block we need to check
def turnsToCheck(tetromino):
    match tetromino:
        case 'O':
            return 1
        case 'S' | 'Z' | 'I':
            return 2
        case _:
            return 4

# how many shift to left and right we need to check
def shiftsToCheck(tetromino):
    match tetromino:
        case 'O':
            return (4, 4)
        case 'S' | 'Z':
            return (3, 5)
        case _:
            return (4, 5)

def getBestMoves():
    pass