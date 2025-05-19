#################################################
# hw10.py
#
# Your name:Matthew Dai
# Your andrew id:mdai2
#################################################

import cs112_s22_week10_linter
import math, os

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################
#from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#nQueens
def removeTempFiles(path, suffix='.DS_Store'):
    if path.endswith(suffix):
        print(f'Removing file: {path}')
        os.remove(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            removeTempFiles(path + '/' + filename, suffix)

def findLargestFile(path):
    bestPath,bestSize = findLargestFileAndSize(path)
    return bestPath

def findLargestFileAndSize(path):
    removeTempFiles('sampleFiles')
    if os.path.isfile(path):
        size = os.path.getsize(path)
        return (path,size)
    else:
        bestSize,bestPath = 0, ''
        for filename in os.listdir(path):
            currentPath,currentSize = findLargestFileAndSize(path + 
                                                             '/' + filename)
            if bestSize < currentSize:
                bestSize = currentSize
                bestPath = currentPath
        return bestPath,bestSize

def knightsTour(rows, cols):
    board = [[-1 for i in range(cols)] for j in range(rows)]
    moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(2,-1),(2,1),(1,2),(1,-2)]
    board[0][0] = 1 
    return knightsTourHelper(board,0,0,rows,cols,0,moves)

def knightsTourHelper(board,startRow,startCol,rows,cols,counter,moves):
    if board[startRow][startCol] != -1:
        return None
    counter += 1
    board[startRow][startCol] = counter    
    if counter == rows * cols:
        return board 
    for drow,dcol in moves:
        newRow,newCol = startRow + drow, startCol + dcol
        if isLegal(rows, cols, newRow,newCol):
            board[newRow][newCol] = counter
            solution = knightsTourHelper(board,newRow,newCol,
                                        rows,cols,counter,moves)
            if solution != None:
                return solution
    board[startCol][startRow] = -1
    return None
    
def isLegal(rows,cols,newRow,newCol):
    if (newRow >= 0 and newRow < rows and newCol >= 0 and newCol < cols):
       return True
    return False

#################################################
# Test Functions
#################################################

def testFindLargestFile():
    print('Testing findLargestFile()...', end='')
    assert(findLargestFile('sampleFiles/folderA') ==
                           'sampleFiles/folderA/folderC/giftwrap.txt')
    assert(findLargestFile('sampleFiles/folderB') ==
                           'sampleFiles/folderB/folderH/driving.txt')
    assert(findLargestFile('sampleFiles/folderB/folderF') == '')
    print('Passed!')

def testKnightsTour():
    print('Testing knightsTour()....', end='')
    def checkDims(rows, cols, ok=True):
        T = knightsTour(rows, cols)
        s = f'knightsTour({rows},{cols})'
        if (not ok):
            if (T is not None):
                raise Exception(f'{s} should return None')
            return True
        if (T is None):
            raise Exception(f'{s} must return a {rows}x{cols}' +
                             ' 2d list (not None)')
        if ((rows != len(T)) or (cols != (len(T[0])))):
            raise Exception(f'{s} must return a {rows}x{cols} 2d list')
        d = dict()
        for r in range(rows):
            for c in range(cols):
                d[ T[r][c] ] = (r,c)
        if (sorted(d.keys()) != list(range(1, rows*cols+1))):
            raise Exception(f'{s} should contain numbers' +
                             ' from 1 to {rows*cols}')
        prevRow, prevCol = d[1]
        for step in range(2, rows*cols+1):
            row,col = d[step]
            distance = abs(prevRow - row) + abs(prevCol - col)
            if (distance != 3):
                raise Exception(f'{s}: from {step-1} to {step}' +
                                 ' is not a legal move')
            prevRow, prevCol = row,col
        return True
    assert(checkDims(4, 3))
    assert(checkDims(4, 4, ok=False))
    assert(checkDims(4, 5))
    assert(checkDims(3, 4))
    assert(checkDims(3, 6, ok=False))
    assert(checkDims(3, 7))
    assert(checkDims(5, 5))
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    testFindLargestFile()
    testKnightsTour()

def main():
    cs112_s22_week10_linter.lint()
    testAll()

if (__name__ == '__main__'):
    main()