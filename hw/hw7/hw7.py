#################################################
# hw7: One-Dimensional Connect Four
# name:
# andrew id:
# 
#################################################

import cs112_n22_week3_linter
from cmu_112_graphics import *
import random, string, math, time

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# main app
#################################################

def appStarted(app):
    app.circleNum = 10
    app.margin = app.width
    app.color = random.randint(0,1)
    app.board = [app.color] * app.circleNum

def createBoard(app):
    for i in range(len(app.board)-1):
        if app.board[i] == app.board[i+1] and app.board[i+1] == 0:
            app.board[i+1] = 1
        elif app.board[i] == app.board[i+1] and app.board[i+1] == 1:
            app.board[i+1] = 0
    
def mousePressed(app, event):
    pass

def timerFired(app):
    createBoard(app)

def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)

def redrawAll(app, canvas):
    drawTitle(app, canvas)
    drawInstructions(app, canvas)
    drawCurrentPlayerAndMessage(app, canvas)
    drawBoard(app, canvas)
    drawRules(app, canvas)

def drawTitle(app, canvas):
    canvas.create_text(app.width/2,20,text = 'One-Dimensional Connect Four!',
                        font = 'Times 25 bold',fill = 'black')

def drawInstructions(app, canvas):
    messages = ['See rules below.',
                'Click interior piece to select center of 3-piece block.',
                'Click end piece to move that block to that end.',
                'Change board size (and then restart) with arrow keys.',
                'For debugging, press c to set the color of selected block.',
                'For debugging, press p to change the current player.',
                'Press r to restart.',
               ]
    for i in range(len(messages)):
        canvas.create_text(app.width/2,40 + 15*i,
                text = messages[i],
                font = 'Times 15 bold',fill = 'black')

def drawRules(app, canvas):
    messages = [
  "The Rules of One-Dimensional Connect Four:",
  "Arrange N (10 by default) pieces in a row of alternating colors.",
  "Players take turns to move three pieces at a time, where:",
  "      The pieces must be in the interior (not on either end)",
  "      The pieces must be adjacent (next to each other).",
  "      At least one moved piece must be the player's color.",
  "The three pieces must be moved in the same order to either end of the row.",
  "The gap must be closed by sliding the remaining pieces together.",
  "The first player to get four (or more) adjacent pieces of their color wins!",
               ]
    for i in range(len(messages)):
        canvas.create_text(220, 400 + 15*i,
                text = messages[i],
                font = 'Times 13 bold',fill = 'black')

def drawCurrentPlayerAndMessage(app, canvas):
    pass

def drawPlayerPiece(app, canvas, player, cx, cy, r):
    pass

def drawBoard(app, canvas):
    for i in range(len(app.board)+1):
        canvas.create_oval(80*i - 30,app.height/2 - 30,
                           80*i + 30,app.height/2 + 30,fill = 'light blue'
                           , width = 4,outline = 'blue')

def main():
    cs112_n22_week3_linter.lint()
    runApp(width=800, height=550)

if __name__ == '__main__':
    main()