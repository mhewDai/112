from cmu_112_graphics import *
import random
import string
from board import Board
import pygame
from hintGenerator import hint
#main program including the sound and other features, such as the game itself
class Sound(object):
    #taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#playingSoundsWithPygame
    def __init__(self, path):
        self.path = path
        self.loops = 1
        pygame.mixer.music.load(path)

    # Returns True if the sound is currently playing
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())

    # Loops = number of times to loop the sound.
    # If loops = 1 or 1, play it once.
    # If loops > 1, play it loops + 1 times.
    # If loops = -1, loop forever.
    def start(self, loops=1):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        pygame.mixer.music.stop()

def newGame(app):
    app.rows,app.cols = None,None
    app.bombLocations = None
    app.count = 0
    app.selection = (-1,-1)
    app.margin,app.cellSize = 15,24
    app.mode = 'gameMenuScreen'
    app.mhx,app.mhy = None,None
    app.hover = None
    app.mcx,app.mcy = None,None
    app.currentMode = None
    app.difficulty = None
    app.selection = (-1,-1)
    app.numBombs = None
    app.gameOver = False
    app.gameStart = False
    app.winner = False
    app.flagMode = False
    app.restartPress = False
    app.flagged = set()
    app.firstClick = True 
    app.board = None #it is None since you havent generated yet
    app.incorrectFlags = []
    app.clue = None
    app.undo = False

def softNewGame(app):
    app.bombLocations = None
    app.count = 0
    app.selection = (-1,-1)
    app.margin,app.cellSize = 15,24
    app.gameOver = False
    app.gameStart = False
    app.winner = False
    app.flagMode = False
    app.restartPress = False
    app.flagged = set()
    app.firstClick = True 
    app.board = None #it is None since you havent generated yet
    app.incorrectFlags = []
    app.clue = None
    app.undo = False

def createBoard(difficulty):
    if difficulty == 'easy':
        numBombs = 10
        rows = 9
        cols = 9
    elif difficulty == 'medium':
        numBombs = 40
        rows = 16
        cols = 16
    elif difficulty == 'hard':
        numBombs = 99
        rows = 16
        cols = 30
    return rows,cols,numBombs 

def getCellBounds(app, row, col):
    #taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2 * app.margin
    gridHeight = app.height - 2 * app.margin - 2.5 * app.cellSize
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + (row+2) * cellHeight
    y1 = app.margin + (row+3) * cellHeight
    return (x0, y0, x1, y1)

def drawCell(app,canvas,row,col,color):
    #draws the individual rectangles
    x0,y0,x1,y1 = getCellBounds(app,row,col)
    canvas.create_rectangle(x0,y0-1,x1,y1-1)  
    ix,iy = abs(x0-x1)/2,abs(y0-y1)/2
    canvas.create_image(x0 + ix, y0 - 0.01 * iy, image = 
                        ImageTk.PhotoImage(app.tileDict['tile']),anchor = N)

def drawBoard(app, canvas):
    #makes the board that the game is on
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col,'white')

def drawTile(app,canvas,row,col,picture):
    x0,y0,x1,y1 = getCellBounds(app,row,col)
    ix,iy = abs(x0-x1)/2,abs(y0-y1)/2
    canvas.create_image(x0 + ix, y0 + 0.01 * iy, image = 
                        ImageTk.PhotoImage(picture),anchor = N)

def drawClickedRegion(app,canvas):
    for (row,col) in app.board.looked:
        if app.board.board[row][col] in list(range(1,9)):
            number = app.board.board[row][col]
            drawTile(app,canvas,row,col,app.tileDict[f'{number}'])
        if app.board.board[row][col] == 0:
            drawTile(app,canvas,row,col,app.tileDict['clickedtile'])
            
def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin <= x <= app.width - app.margin) and
            (2 * app.margin + 1.5 * app.cellSize <= y <= app.height - 2 * app.margin))

def getCell(app, x, y):
    #taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2 * app.margin
    gridHeight = app.height - 2 * app.margin - 2.5 * app.cellSize
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.margin - 2*app.cellSize) / cellHeight)
    col = int((x - app.margin) / cellWidth)
    return (row, col)

def imageConvertToDictionary(app,path):
    d = dict()
    number = False
    for images in os.listdir(path):
        if not (images == '.DS_Store'):
            image,png = images.split('.')
            for letters in image:
                if letters.isdigit():
                    original = app.loadImage(images)
                    d[letters] = app.scaleImage(original,3/2)
                    number = True
            if number == False:
                original = app.loadImage(images)
                d[image] = app.scaleImage(original,3/2)
        number = False
    return d

def nearbyTiles(row,col,rows,cols):
    nearSquares = []
    for i in range(-1,2):
        for j in range(-1,2):
            newRow,newCol = row + i, col + j
            if ((newRow,newCol) != (row,col) and 
                0 <= newRow < rows and 0 <= newCol != cols):
                nearSquares.append((newRow,newCol))
    return nearSquares

def massClear(app,row,col):
    r,c = row,col
    neighbors = nearbyTiles(r,c,app.rows,app.cols)
    s = set()
    count = 0
    for tiles in neighbors:
        if tiles in app.flagged:
            count += 1
        elif tiles not in app.flagged and tiles not in app.board.looked:
            s.add(tiles)
    if count == app.board.board[r][c]:
        return True,s
    return False,s

def clock(app,canvas):
    time = app.count // 10
    if time < 10:
        canvas.create_image(12,16, image = 
                            ImageTk.PhotoImage(app.redNum['0']),anchor = NW)
        canvas.create_image(32,16, image = 
                            ImageTk.PhotoImage(app.redNum['0']),anchor = NW)
        canvas.create_image(52,16, image = 
                            ImageTk.PhotoImage(app.redNum[f'{time}']),anchor = NW)
    elif 10 <= time < 100:
        canvas.create_image(12,16, image = 
                    ImageTk.PhotoImage(app.redNum['0']),anchor = NW)
        canvas.create_image(32,16, image = 
                    ImageTk.PhotoImage(app.redNum[f'{time//10}']),anchor = NW)
        canvas.create_image(52,16, image = 
                    ImageTk.PhotoImage(app.redNum[f'{time%10}']),anchor = NW)
    else:
        digit1,digit2,digit3 = time//100,(time//10)%10,time%10
        canvas.create_image(12,16, image = 
                    ImageTk.PhotoImage(app.redNum[f'{digit1}']),anchor = NW)
        canvas.create_image(32,16, image = 
                    ImageTk.PhotoImage(app.redNum[f'{digit2}']),anchor = NW)
        canvas.create_image(52,16, image = 
                    ImageTk.PhotoImage(app.redNum[f'{digit3}']),anchor = NW)

def drawBombCount(app,canvas):
    bombs = 0 if app.winner == True else app.numBombs - len(app.flagged) 
    digit1,digit2 = abs(bombs) // 10,abs(bombs) % 10
    if bombs < 0:    
        canvas.create_image(app.width-(52+1.5*app.margin),16, image = 
                            ImageTk.PhotoImage(app.redNum['negative']),anchor = NW)
        canvas.create_image(app.width-(32+1.5*app.margin),16, image = 
                            ImageTk.PhotoImage(app.redNum[f'{digit1}']),anchor = NW)
        canvas.create_image(app.width-(12+1.5*app.margin),16, image = 
                            ImageTk.PhotoImage(app.redNum[f'{digit2}']),anchor = NW) 
    else:
        canvas.create_image(app.width-(52+1.5*app.margin),16, image = 
                            ImageTk.PhotoImage(app.redNum['0']),anchor = NW)
        canvas.create_image(app.width-(32+1.5*app.margin),16, image = 
                                ImageTk.PhotoImage(app.redNum[f'{digit1}']),anchor = NW)
        canvas.create_image(app.width-(12+1.5*app.margin),16, image = 
                                ImageTk.PhotoImage(app.redNum[f'{digit2}']),anchor = NW) 

def win(app):
    uncleared,unfoundBomb = 0,0
    for row in range(app.rows):
        for col in range(app.cols):
            if ((row,col) not in app.board.looked 
                and (row,col) not in app.flagged
                and (app.board.board[row][col] == '*')):
                unfoundBomb += 1
            elif ((row,col) not in app.board.looked 
                and (row,col) not in app.flagged):
                uncleared += 1
    for r,c in app.flagged:
        if (r,c) not in app.bombLocations:
            return False
    if (uncleared == 0) or (unfoundBomb == 0):
        app.gameStart = False
        return True
    return False

def undoButton(app):
    app.undo = True
    app.gameOver = False
    app.flagged.add(app.gameoverSelection) 
    app.gameStart = True
    app.gameoverSelection = None
##########################################
# Game Menu Screen
##########################################
def gameMenuScreen_redrawAll(app, canvas):
    #title region
    canvas.create_text(app.width/2,app.height/8,
                       text = 'Minesweeper',font = 'Times 28 bold',
                       fill = 'blue', anchor = N)
    #Easy box
    canvas.create_rectangle(20,app.height/4+20, app.width-20,app.height/2-20,fill = 'blue')
    canvas.create_text((20 + app.width-20)/2,(app.height/2-20 + app.height/4+20)/2,
                        text = 'Easy', font = 'Times 24 bold', fill = 'white')
    if app.hover == 'easy':
        canvas.create_rectangle(20,app.height/4+20, app.width-20,
                                app.height/2-20,outline = 'red', width = 4)
    #medium box
    canvas.create_rectangle(20,app.height/2+20, app.width-20,3 * app.height/4-20,fill = 'blue')
    canvas.create_text((20 + app.width-20)/2,(app.height/2+20 + 3 * app.height/4-20)/2,
                        text = 'Medium', font = 'Times 24 bold', fill = 'white')
    if app.hover == 'medium':
        canvas.create_rectangle(20,app.height/2+20, app.width-20,
                                3 * app.height/4-20, width = 4, outline = 'red')

    #hard box
    canvas.create_rectangle(20,3 * app.height/4+20, app.width-20,app.height-20,fill = 'blue')
    canvas.create_text((20 + app.width-20)/2,(3 * app.height/4+20 + app.height-20)/2,
                        text = 'Hard', font = 'Times 24 bold', fill = 'white')
    if app.hover == 'hard':
        canvas.create_rectangle(20,3 * app.height/4+20, app.width-20,
                                app.height-20,width = 4, outline = 'red')
    canvas.create_text((20 + app.width-20)/2,(app.height/3.5-20 + app.height/4+20)/2,
                        text = 'Press h for instructions', font = 'Times 12 bold', fill = 'red')

def gameMenuScreen_mousePressed(app,event):
    app.mcx,app.mcy = event.x,event.y
    if (20 <= app.mcx <= app.width-20 and 
        app.height/4+20 <= app.mcy <= app.height/2-20):
        app.mode = 'game'    
        app.difficulty = 'easy'
        app.rows,app.cols,app.numBombs = createBoard('easy')
        height, width = (app.rows+3) * app.cellSize + 3 * app.margin, app.cols * app.cellSize + 2 * app.margin
        app.setSize(width, height)
    
    if (20 <= app.mcx <= app.width-20 
        and app.height/2+20 <= app.mcy <= 3 * app.height/4-20):
        app.mode = 'game'    
        app.currentMode = 'game'
        app.difficulty = 'medium'
        app.rows,app.cols,app.numBombs = createBoard('medium')
        height, width = (app.rows+2) * app.cellSize + 3 * app.margin, app.cols * app.cellSize + 2 * app.margin
        app.setSize(width, height)

    elif (20 <= app.mcx <= app.width-20
        and 3 * app.height/4+20 <= app.mcy <= app.height-20):
        app.mode = 'game'
        app.diffculty = 'hard'
        app.rows,app.cols,app.numBombs = createBoard('hard')
        height, width = (app.rows+2) * app.cellSize + 3 * app.margin, app.cols * app.cellSize + 2 * app.margin
        app.setSize(width, height)

def gameMenuScreen_keyPressed(app,event):
    if event.key == 'h':
        app.mode = 'helpMode'
        app.currentMode = 'gameMenuScreen'
        app.setSize(400,400)
        
def gameMenuScreen_mouseMoved(app,event):
    app.mhx,app.mhy = event.x,event.y
    if (20 <= app.mhx <= app.width-20 and 
        app.height/4+20 <= app.mhy <= app.height/2-20):
        app.hover = 'easy'    
    elif (20 <= app.mhx <= app.width-20 
        and app.height/2+20 <= app.mhy <= 3 * app.height/4-20):
        app.hover = 'medium'    
    elif (20 <= app.mhx <= app.width-20
        and 3 * app.height/4+20 <= app.mhy <= app.height-20):
        app.hover = 'hard'
    else:
        app.hover = None

def gameMenu_keyPressed(app, event):
    if (event.key == 'h'):
        app.mode = 'helpMode'

##########################################
# Minesweeper
##########################################
def game_keyPressed(app,event):
    if event.key == 'f':
        if app.flagMode:
            app.flagMode = False
        else:
            app.flagMode = True
    elif event.key == 'r':
        app.currentMode = app.mode
        newGame(app)
        app.mode = 'gameMenuScreen'
        app.setSize(400,400)
    elif event.key == 'h':
        app.currentMode = app.mode
        app.mode = 'helpMode'
        app.setSize(400,400)
    elif event.key == 'c' and app.gameStart:
        solver = hint(app.board,app.flagged)
        solver.naiveSolution()
        if solver.hint() != None:
            app.flagged.add(solver.hint())
        elif solver.hint() == None:
            app.clue = None
    elif event.key == 'u' and app.gameStart == False:
        undoButton(app)

def game_mousePressed(app, event):
    (row, col) = getCell(app, event.x, event.y)
    app.selection = (row,col)
    if ((app.width/2 -13 <= event.x <= app.width/2 + 13) 
             and (14 <= event.y <= 40)):
            #activating the smile face which will be a soft reset(same difficulty)
            softNewGame(app)
    elif app.gameOver == False:
        if app.firstClick:
            #generates the board based on the row and col of the first click 
            app.gameStart = True
            app.board = Board(app.rows,app.cols,row,col,app.numBombs)
            app.bombLocations = app.board.bombPlaces
            app.board.search(row,col)
            app.firstClick = False
            app.gameStart = True
        elif app.flagMode:
            #during flag mode the user can add 
            #or remove a flag the areas of the grid 
            if app.selection in app.flagged:
                app.flagged.remove(app.selection)
            else:
                if ((row,col) not in app.board.looked):
                    app.flagged.add((row,col))
                    if (row,col) not in app.bombLocations:
                        app.incorrectFlags.append((row,col))
        elif app.selection in app.board.looked:
            #if the number of bombs around a tile is correct then you can click 
            #on it to clear any remaining uncovered tiles
            r,c = app.selection
            clear = massClear(app,r,c)
            if clear[0]:
                for (r,c) in clear[1]:
                    app.board.search(r,c)
                    if app.board.board[r][c] == '*':
                        if app.loseSound.isPlaying(): app.loseSound.stop()
                        else: app.loseSound.start()
        else:
            app.board.search(row,col)
            if app.board.board[row][col] == '*':
                if app.loseSound.isPlaying(): app.loseSound.stop()
                else: app.loseSound.start()

def game_redrawAll(app, canvas):
    if app.winner:
        canvas.create_rectangle(5, 5, app.width-5, app.height-5, fill = 'light gray',
                                                    outline = 'gray', width = 8)
        drawClickedRegion(app,canvas)
        for rows in range(app.rows):
            for cols in range(app.cols):
                if ((rows,cols) not in app.board.looked 
                    and (rows,cols) not in app.flagged):
                    drawTile(app,canvas,rows,cols,app.tileDict['clickedtile'])
        for row,col in app.flagged:
            drawTile(app,canvas,row,col,app.tileDict['flag'])
        canvas.create_image(app.width/2,27, image = 
                            ImageTk.PhotoImage(app.win))
        for row,col in app.bombLocations:
            drawTile(app,canvas,row,col,app.tileDict['flag'])
    else:
        canvas.create_rectangle(5, 5, app.width-5, app.height-5, fill = 'light gray',
                                                    outline = 'gray', width = 8)
        drawBoard(app,canvas)
        canvas.create_image(app.width/2,27, image = 
                            ImageTk.PhotoImage(app.restartButton))
        if (app.gameStart and (app.gameOver == False)):
            drawClickedRegion(app,canvas)
            for row,col in app.flagged:
                drawTile(app,canvas,row,col,app.tileDict['flag'])
        if app.flagMode:
            canvas.create_text(app.width/2,app.height - 1.25 * app.margin,
                    text = 'Flag Mode On', font = 'Times 8 bold', 
                    fill = 'black')
        else:
            canvas.create_text(app.width/2,app.height - 1.25 * app.margin,
                    text = 'Flag Mode Off', font = 'Times 8 bold', 
                    fill = 'black')
        if app.gameOver and app.undo == False:
            drawClickedRegion(app,canvas)
            for rows in range(app.rows):
                for cols in range(app.cols):
                    if app.board.board[rows][cols] == '*':
                        drawTile(app,canvas,rows,cols,app.tileDict['mine'])
                        if (app.gameoverSelection == (rows,cols)):
                            drawTile(app,canvas,rows,cols,app.tileDict['gameoverMine'])
            for row,col in app.flagged:
                if (row,col) not in app.bombLocations:
                    drawTile(app,canvas,row,col,app.tileDict['incorrect'])
                else:
                    drawTile(app,canvas,row,col,app.tileDict['flag'])
            canvas.create_image(app.width/2,27, image = 
                            ImageTk.PhotoImage(app.lose))
    clock(app,canvas)
    drawBombCount(app,canvas)
                    
def game_timerFired(app):
    if app.firstClick == False:
        if app.gameOver == False:
            for (row,col) in app.board.looked:
                if (app.board.board[row][col] == '*' 
                    and (row,col) not in app.flagged
                    and app.flagMode == False):
                    if app.undo == False:
                        app.gameStart = False
                        app.gameOver = True
                        app.gameoverSelection = (row,col)
        if win(app):
            app.winner = True
    if app.gameStart:
        app.count += 1
    
##########################################
# Help Mode
##########################################

def helpMode_redrawAll(app, canvas):
    font = 'Arial 14'
    p = '''The numbers on the board represent how many bombs
are adjacent to a square. For example, if a square 
has a "3" on it, then there are 3 bombs next to that 
square. The bombs could be above, below, right left, 
or diagonal to the square. Avoid all the bombs and 
expose all the empty spaces to win Minesweeper.'''
    canvas.create_text(app.width//2, 100, text = "Instructions", font = 'Arial 24 bold', fill = 'Black')
    canvas.create_text(app.width//2, 170, text= p, font=font, fill= 'black')
    canvas.create_text(app.width//2, 280, text = 'To go back press b', fill = 'black')
    canvas.create_text(app.width//2, 300, text = 'Press f to turn on flag mode', fill = 'black')
    canvas.create_text(app.width//2, 320, text = 'Press u to undo last move', fill = 'black')
    canvas.create_text(app.width//2, 340, text = 'Press r to go to main menu', fill = 'black')
    canvas.create_text(app.width//2, 360, text = 'Press smile face to reset board', fill = 'black')
    canvas.create_text(app.width//2, 380, text =  'Press c for a clue', fill = 'black')

def helpMode_keyPressed(app, event):
    if event.key == 'b':
        app.mode = app.currentMode
        if app.currentMode == 'gameMenuScreen':
            app.setSize(400,400)
        else:
            app.rows,app.cols,app.numBombs = createBoard(app.difficulty)
            height = (app.rows+2) * app.cellSize + 3 * app.margin 
            width = app.cols * app.cellSize + 2 * app.margin
            app.setSize(width, height)

##########################################
# Main App
##########################################

def appStarted(app):
    pygame.mixer.init()
    app.rows,app.cols = None,None
    app.selection = (-1,-1)
    app.margin,app.cellSize = 15,24
    app.mode = 'gameMenuScreen'
    app.mhx,app.mhy = None,None
    app.hover = None
    app.mcx,app.mcy = None,None
    app.currentMode = None
    app.selection = (-1,-1)
    app.numBombs = None
    app.gameOver = False
    app.gameStart = False
    app.winner = False
    app.flagMode = False
    app.restartPress = False
    app.flagged = set()
    app.firstClick = True 
    app.board = None #it is None since you havent generated yet
    app.restartButton = app.loadImage('restartButton.png')
    app.win = app.loadImage('victory.png')
    app.lose = app.loadImage('gameover.png')
    app.difficulty = None
    app.gameoverSelection = None
    app.tileDict = imageConvertToDictionary(app,'tiles')
    app.redNum = imageConvertToDictionary(app,'numbers')
    app.count = 0
    app.bombLocations = None
    app.incorrectFlags = []
    app.loseSound = Sound('lose.wav')
    app.clue = None
    app.undo = False

def startGame():
    width, height = 400,400
    runApp(width = width,height = height)

startGame()



