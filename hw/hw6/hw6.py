#################################################
# hw6.py
#
# Your name:Matthew Dai
# Your andrew id:mdai2
#
# Your partner's name: Anna Hong
# Your partner's andrew id: annahong
#################################################

import cs112_s22_week6_linter
import math, copy, random

from cmu_112_graphics import *

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

def isPerfectSquare(n):
    n = abs(n)
    squareRootOfN = int(math.sqrt(n))
    #check if the square is the same value
    if squareRootOfN ** 2 == n:
        return True
    return False

def isSortOfSquarish(n):
    result = []
    result1 = 0
    if not isPerfectSquare(n) and n > 0:
        #isolating individual digits into list for sorting
        while n > 0:
            if n % 10 == 0: return False
            result.append(n%10)
            n //= 10
        result.sort()
        for i in range(len(result)):
            result1 += result[i] * 10**(len(result)-1-i)
        if isPerfectSquare(result1):
            return True
    return False

def nthSortOfSquarish(n):
    found = 0
    guess = 0
    #checking values until it satisfies n
    while (found <= n):
        guess += 1
        if isSortOfSquarish(guess):
            found += 1
    return guess

#################################################
# s21-midterm1-animation
#################################################

def s21MidtermAnimation_appStarted(app):
    app.circleCenters = []
    app.timePassed = 0
    app.paused = False
    app.timeCount = 0
    app.r = 20

def s21MidtermAnimation_mousePressed(app,event):
    #the timer only starts when the keyboard or mouse is pressed
    app.timeCount = 0
    app.circleCenters.append((event.x, event.y))
    
def s21MidtermAnimation_keyPressed(app, event):
    app.timeCount = 0
    #the timer only starts when the keyboard or mouse is pressed
    if (event.key == 'r'):
        app.circleCenters = []
    elif (event.key == 'p'):
        app.paused = not app.paused

def s21MidtermAnimation_timerFired(app):
    if (not app.paused):
    #app.pause was put here for testing purposes
        app.timeCount += app.timerDelay
        if app.timeCount  % 5000 == 0:
            app.circleCenters = []

def nearestCircle(currentCircle, lst):
    currX,currY = currentCircle
    firstX,firstY = lst[0]
    dX,dY = currX - firstX, currY-firstY
    distance1 = (dX**2 + dY**2)**0.5
    #preloads with the value of the first coordinate 
    #in order to have something to compare
    for i in range(1, len(lst)):
        tempX,tempY = lst[i]
        tempDX, tempDY = currX - tempX, currY-tempY
        distance2 = (tempDX**2 + tempDY**2)**0.5
        if distance2 < distance1:
            distance1 = distance2
            firstX, firstY = tempX,tempY
    return firstX,firstY

def s21MidtermAnimation_redrawAll(app, canvas):
    #app.circleCenters is a list of center coordinates drawn in this loop
    for (cx, cy) in app.circleCenters:
        canvas.create_oval(cx - app.r, cy - app.r, cx + app.r, 
        cy + app.r, fill = 'green')
    #loops through of the coordinates and checks for closest 
    if ((len(app.circleCenters) >= 1)):
        #this loop will not activate until 2 values are found in the list
        for i in range(1, len(app.circleCenters)):
            closestX, closestY, = nearestCircle(app.circleCenters[i], 
            app.circleCenters[:i])
            canvas.create_line(app.circleCenters[i][0], app.circleCenters[i][1]
            , closestX, closestY, fill = 'black', width = 2)

def s21Midterm1Animation():
    runApp(width=400, height=400, fnPrefix='s21MidtermAnimation_')


#################################################
# Tetris
#################################################

def appStarted(app):
    app.rows,app.cols,app.margin,app.cellSize = gameDimensions()
    app.emptyColor = 'blue'
    app.board = [([app.emptyColor] * app.cols) for i in range(app.rows)]
    # The seven tetris pieces:
    iPiece = [
             [True,True,True,True]
                                 ]
    jPiece = [
              [True, False, False],
              [True, True,  True ]
                                  ]
    oPiece = [
              [True, True],
              [True, True]
                          ]
    sPiece = [
              [False, True, True],
              [True, True, False]
                                 ]
    tPiece = [
              [False, True, False],
              [ True ,True, True ]
                                  ]
    zPiece = [
              [True, True, False],
              [False, True, True]
                                  ]
    app.tetrisPieces = [iPiece,jPiece,oPiece,sPiece,tPiece,zPiece]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", 
                              "pink", "cyan", "green", "orange" ]
    app.isGameOver = False
    app.score = 0
    #controls how fast the game is
    app.timerDelay = 250
    newFallingPieces(app)
    app.isBonusMode = False
    app.highScoreList = []

def gameDimensions():
    rows = 15
    cols = 10
    margin = 25
    cellSize = 20
    return (rows,cols,margin,cellSize)

def timerFired(app):
    if app.isGameOver == False:
    #when the game stops, the pieces stop falling
        if not moveFallingPieces(app,+1,0):
            placeFallingPiece(app)
            newFallingPieces(app)
            if not fallingPieceIsLegal(app):
                app.isGameOver = True
    if app.isGameOver and app.isBonusMode:
        if app.score not in app.highScoreList:
            app.highScoreList.append(app.score)

def newGame(app):
    app.board = [([app.emptyColor] * app.cols) for i in range(app.rows)]
    app.isGameOver = False
    app.score = 0

def keyPressed(app, event):
    if app.isGameOver == False:
    #when the game stops, you are not allowed to move any pieces
        if (event.key == 'Up'): rotatingFallingPiece(app)
        elif (event.key == 'Down'):  moveFallingPieces(app,+1,0) 
        elif (event.key == 'Left'):  moveFallingPieces(app,0,-1) 
        elif (event.key == 'Right'): moveFallingPieces(app,0,+1) 
        elif (event.key == 'Space'): hardDrop(app)
        elif (event.key == 'b'): 
            #Press b to activate bonus mode
            app.isBonusMode = True
        if app.isBonusMode:
            if (event.key == 's'): app.timerDelay = 300
            if (event.key == 'f'): app.timerDelay = 50
    else:
        if(event.key == 'r'): newGame(app)
    
def cellBound(app,row,col):
    #taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
    gridWidth  = app.width - 2 * app.margin
    gridHeight = app.height - 2 * app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

def drawCell(app,canvas,row,col,color):
    #draws the individual rectangles
    x0, y0, x1, y1 = cellBound(app,row,col)
    canvas.create_rectangle(x0, y0, x1, y1,
                                    fill = color, outline = 'black',width = 3)

def drawBoard(app, canvas):
    #makes the board that the game is on
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, canvas, row, col, color)

def newFallingPieces(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingTetrisPiece = app.tetrisPieces[randomIndex]
    app.randomColor = app.tetrisPieceColors[randomIndex]
    #the rows the tetris piece list
    app.numFallingPieceRow = len(app.fallingTetrisPiece)
    #the cols of the tetris piece list
    app.numFallingPieceCol = len(app.fallingTetrisPiece[0])
    #the row position of the falling Piece with respect to board
    app.fallingPieceRow = 0
    #the col position of the falling piece with respect to board
    app.fallingPieceCol = app.cols//2 - app.numFallingPieceCol//2
    
def drawFallingPieces(app,canvas):
    #draws the fallingPiece with respect to the board
    for rows in range(app.numFallingPieceRow):
        for cols in range(app.numFallingPieceCol):
            if app.fallingTetrisPiece[rows][cols]:
                drawCell(app, canvas, app.fallingPieceRow + rows, 
                app.fallingPieceCol + cols, app.randomColor)

def moveFallingPieces(app,drow,dcol):
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    if not fallingPieceIsLegal(app):
    #checks if the fallingPiece position is on the board or not
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        return False
    return True
        
def fallingPieceIsLegal(app):
    for row in range(app.numFallingPieceRow):
        for col in range(app.numFallingPieceCol):
            if app.fallingTetrisPiece[row][col]:
                tempRow, tempCol = (app.fallingPieceRow + row, 
                                   app.fallingPieceCol + col)
                #checks if the tetris piece is off the board or not and 
                #returns False if it is
                if ((tempRow < 0) or (tempRow >= app.rows) 
                   or (tempCol < 0) or (tempCol >= app.cols)):
                    return False
                elif app.board[tempRow][tempCol] != app.emptyColor:
                    return False
    return True

def rotatingFallingPiece(app):
    initialPiece = copy.deepcopy(app.fallingTetrisPiece)
    oldNumRow, oldNumCol = app.numFallingPieceRow, app.numFallingPieceCol
    #since the position of the tetris is reversed, the new rows and the 
    #new cols are the old cols and old rows
    newNumRow,newNumCol = app.numFallingPieceCol, app.numFallingPieceRow
    newPiece = [[0] * app.numFallingPieceRow
                for rows in range(app.numFallingPieceCol)]
    for row in range(oldNumRow):
        for col in range(oldNumCol):
            newPiece[oldNumCol-col-1][row] = initialPiece[row][col]
    
    oldRow,oldCol = app.fallingPieceRow, app.fallingPieceCol
    #stores the original piece of the falling piece
    newRow = oldRow + oldNumRow//2 - newNumRow//2
    newCol = oldCol + oldNumCol//2 - newNumCol//2
    #newRow and newCol are different variables that update the position 
    #rather than the number of rows or cols of the tetris piece
    app.numFallingPieceRow, app.numFallingPieceCol = newNumRow, newNumCol
    app.fallingTetrisPiece  = newPiece 
    app.fallingPieceRow, app.fallingPieceCol = newRow, newCol
    if not fallingPieceIsLegal(app):
    #i have to reverse the number of rows and number of 
    #cols to its original state to prevent an index error
        app.fallingTetrisPiece = initialPiece
        app.numFallingPieceRow = oldNumRow
        app.numFallingPieceCol = oldNumCol
        app.fallingPieceRow = oldRow
        app.fallingPieceCol = oldCol

def placeFallingPiece(app):
    for row in range(app.numFallingPieceRow):
        for col in range(app.numFallingPieceCol):
            if app.fallingTetrisPiece[row][col]: 
            # Changes the board position with the new piece
                newRow = app.fallingPieceRow + row
                newCol = app.fallingPieceCol + col
                app.board[newRow][newCol] = app.randomColor
    #After placing the piece, it checks if the row can be cleared or not
    removeFullRows(app)

def hardDrop(app):
    while fallingPieceIsLegal(app):
        #it moves through all the rows and see if the next move is legal or not
        #when it hits the bottom or an unfinished row with a random color,
        #the loop will be broken and the place function will activate
        if moveFallingPieces(app,+1,0) == False:
            placeFallingPiece(app)

def removeFullRows(app):
    newBoard = []
    fullRow = 0
    for row in range(len(app.board)):
        emptyColorCount = 0
        for col in range(len(app.board[0])):
            #checks reach space on the board for blue
            if app.board[row][col] == app.emptyColor:
                emptyColorCount += 1
        if emptyColorCount == 0:
            #if the row is full or has no blue in it, this part activates
            fullRow += 1
        else:
            #when there is still some blue left the new board adds this row
            newBoard.append(app.board[row])
    app.score += fullRow ** 2
    #for ever row removed a new row that has blue in it is added along with the
    #rows that has a mix of blue and random color
    newBoard = [[app.emptyColor] * app.cols for i in range(fullRow)] + newBoard
    app.board = newBoard

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'orange')
    drawBoard(app,canvas)
    drawFallingPieces(app,canvas)
    if app.isGameOver:
    #when gameover happens, the canvas 
    # draws the gameover sign at the top of the board
        canvas.create_rectangle(app.margin, app.margin + app.cellSize, 
                            app.cols * app.cellSize + app.margin, app.margin + 
                            3 * app.cellSize, fill ='black')
        canvas.create_text(app.margin + 5 * app.cellSize,
                           app.margin + 1.25 * app.cellSize, fill ='Yellow',
                            text = 'Game Over',anchor = N, 
                            font = 'Times 28 bold')
        if app.isBonusMode:
            canvas.create_rectangle(app.margin, app.margin + app.cellSize * 3, 
                                app.cols * app.cellSize + app.margin, 
                                app.margin + app.rows * app.cellSize, 
                                fill ='purple')
            for i in range(len(app.highScoreList)):
                canvas.create_text(app.margin + 5 * app.cellSize,
                            app.margin + 3 * app.cellSize + i * app.cellSize, 
                            fill ='Yellow',
                            text = f'{app.highScoreList[i]}',
                            anchor = N, 
                            font = 'Times 28 bold')                            
    canvas.create_text(app.margin + 5* app.cellSize,
                        app.cellSize * app.rows + app.margin,fill ='black', 
                        text = f'To activate Bonus Mode press b', 
                        anchor = N,font = 'Times 14 bold')
    #the score is at the top of the screen and is constantly updating
    canvas.create_text(app.margin + 5 * app.cellSize,
                        0.25*app.margin,fill ='black', 
                        text = f'Score: {app.score}', anchor = N,
                        font = 'Times 14 bold')

def playTetris():
    rows,cols,margin,cellSize = gameDimensions()
    height, width = rows * cellSize + 2 * margin, cols * cellSize + 2 * margin
    runApp(width = width, height = height)

#################################################
# Test Functions
#################################################

def testIsPerfectSquare():
    print('Testing isPerfectSquare(n))...', end='')
    assert(isPerfectSquare(4) == True)
    assert(isPerfectSquare(9) == True)
    assert(isPerfectSquare(10) == False)
    assert(isPerfectSquare(225) == True)
    assert(isPerfectSquare(1225) == True)
    assert(isPerfectSquare(1226) == False)
    print('Passed')

def testIsSortOfSquarish():
    print('Testing isSortOfSquarish(n))...', end='')
    assert(isSortOfSquarish(52) == True)
    assert(isSortOfSquarish(16) == False)
    assert(isSortOfSquarish(502) == False)
    assert(isSortOfSquarish(414) == True)
    assert(isSortOfSquarish(5221) == True)
    assert(isSortOfSquarish(6221) == False)
    assert(isSortOfSquarish(-52) == False)
    print('Passed')

def testNthSortOfSquarish():
    print('Testing nthSortOfSquarish()...', end='')
    assert(nthSortOfSquarish(0) == 52)
    assert(nthSortOfSquarish(1) == 61)
    assert(nthSortOfSquarish(2) == 63)
    assert(nthSortOfSquarish(3) == 94)
    assert(nthSortOfSquarish(4) == 252)
    assert(nthSortOfSquarish(8) == 522)
    print('Passed')

def testAll():
    testIsPerfectSquare()
    testIsSortOfSquarish()
    testNthSortOfSquarish()

#################################################
# main
#################################################

def main():
    cs112_s22_week6_linter.lint()
    testAll()
    s21Midterm1Animation()
    playTetris()

if __name__ == '__main__':
    main()
