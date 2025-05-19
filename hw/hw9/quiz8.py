import cs112_s22_week9_linter
import math, copy, random

from cmu_112_graphics import *

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

def gameDimensions():
    rows = 16
    cols = 30
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

def keyPressed(app, event):
    if app.isGameOver == False:
    #when the game stops, you are not allowed to move any pieces
        if (event.key == 'Up'): rotatingFallingPiece(app)
        elif (event.key == 'Down'):  moveFallingPieces(app,+1,0) 
        elif (event.key == 'Left'):  moveFallingPieces(app,0,-1) 
        elif (event.key == 'Right'): moveFallingPieces(app,0,+1) 
        elif (event.key == 'Space'): hardDrop(app)
    if(event.key == 'r'): appStarted(app)
    
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
    #the score is at the top of the screen and is constantly updating
    canvas.create_text(app.margin + 5 * app.cellSize,
                           0.25*app.margin,fill ='black', 
                           text = f'Score: {app.score}', anchor = N,
                           font = 'Times 14 bold')

def playTetris():
    rows,cols,margin,cellSize = gameDimensions()
    height, width = rows * cellSize + 2 * margin, cols * cellSize + 2 * margin
    runApp(width = width, height = height)

playTetris()