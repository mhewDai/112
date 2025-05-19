#################################################
# hw9.py
#
# Your name: Matthew Dai
# Your andrew id: mdai2
#################################################

import math, copy, os
import cs112_s22_week9_linter

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

def oddCount(L):
    if L == []:
        return 0
    else:
        if L[0] % 2 == 1:
            return 1 + oddCount(L[1:]) 
        else:
            return oddCount(L[1:])

def oddSum(L):
    if L == []:
        return 0
    else:
        if L[0] % 2 == 1:
            return L[0] + oddSum(L[1:]) 
        else:
            return oddSum(L[1:])

def oddsOnly(L):
    if len(L) == 0:
        return []
    else:
        firstNumber = L[0]
        rest = L[1:]
        if firstNumber % 2 == 1:
            return [firstNumber] + oddsOnly(rest)
        else:
            return oddsOnly(rest)

def maxOdd(L):
    if len(L) == 0:
        return None
    else:
        if L[0] % 2 == 1:
            temp = maxOdd(L[1:])
            if temp != None:
                return max(L[0],temp)
            else:
                return L[0]
        else:
            return maxOdd(L[1:])

def hasConsecutiveDigits(n):
    if n == 0:
        return False
    else:
        n = abs(n)
        currDigit,n = n % 10, n//10
        if currDigit == n%10:
            return True
        else:
            return hasConsecutiveDigits(n)
        
def alternatingSum(L):
    if L == []:
        return 0
    else:
        currValue = L[-1]
        if len(L) % 2 == 1:
            return alternatingSum(L[:-1]) + currValue
        else:
            return  alternatingSum(L[:-1]) - currValue

#################################################
# Freddy Fractal Viewer
#################################################

from cmu_112_graphics import *

def appStarted(app):
    app.level = 1

def keyPressed(app, event):
    if event.key in ['Up','Right'] and app.level < 5:
        app.level += 1
    elif event.key in ['Down','Left'] and app.level > 0:
        app.level -= 1

def drawFreddyFracter(app,canvas,level,x,y,size):
    if level == 0:
        #freddie head
        canvas.create_oval(x + size , y + size, x - size, y - size, 
        outline = 'black', width = size/12, fill = 'brown')
        #freddie eyes left
        canvas.create_oval((x-size/2) + size/6, (y-size/2.5) + size/6, 
        (x-size/2) - size/6, (y-size/2.5) - size/6, 
        outline = 'black', fill = 'black')
        #freddie eyes right
        canvas.create_oval((x+size/2) + size/6, (y- size/2.5) + size/6, 
        (x+size/2) - size/6, (y-size/2.5) - size/6, 
        outline = 'black', fill = 'black')
        #mouse circle
        canvas.create_oval(x + size/2,(y+size/4) - size/2, x - size/2, 
        (y+size/4) + size/2, outline = 'black',width = size/10, fill = 'tan')
        #nose
        canvas.create_oval(x + size/6, y + size/6, x - size/6, y - size/6, 
        outline = 'black', fill = 'black')
        #freddie mouse
        canvas.create_arc((x - size/6) + size/7,(y+size/3) - size/7, 
        (x - size/6) - size/7, (y+size/3) + size/7, outline = 'black',
        fill = 'black',style = ARC,extent = -180,width = size/10)
        canvas.create_arc((x + size/7) + size/7,(y+size/3) - size/7, 
        (x + size/7) - size/7, (y+size/3) + size/7, outline = 'black',
        fill = 'black',style = ARC,extent = -180,width = size/10)
    else:
        distance = (1.5 * size)/(2**0.5)
        #left freddy ear
        drawFreddyFracter(app,canvas,level-1,x+distance,y-distance,size//2)
        #right freddy ear
        drawFreddyFracter(app,canvas,level-1,x-distance,y-distance,size//2)
        #large freddy
        drawFreddyFracter(app,canvas,0,x,y,size)

def redrawAll(app, canvas):
    drawFreddyFracter(app,canvas,app.level,app.width/2,(app.height+100)/2,
                      app.width/4)
    canvas.create_text(app.width/2,0,text = 'Current Level: ' + str(app.level),
    font = 'Arial 20 bold', anchor = N, fill = 'blue')

       
def runFreddyFractalViewer():
    print('Running Freddy Fractal Viewer!')
    runApp(width=400, height=400)



#################################################
# Test Functions
#################################################

def testOddCount():
    print('Testing oddCount()...', end='')
    assert(oddCount([ ]) == 0)
    assert(oddCount([ 2, 4, 6 ]) == 0) 
    assert(oddCount([ 2, 4, 6, 7 ]) == 1)
    assert(oddCount([ -1, -2, -3 ]) == 2)
    assert(oddCount([ 1,2,3,4,5,6,7,8,9,10,0,0,0,11,12 ]) == 6)
    print('Passed!')

def testOddSum():
    print('Testing oddSum()...', end='')
    assert(oddSum([ ]) == 0)
    assert(oddSum([ 2, 4, 6 ]) == 0) 
    assert(oddSum([ 2, 4, 6, 7 ]) == 7)
    assert(oddSum([ -1, -2, -3 ]) == -4)
    assert(oddSum([ 1,2,3,4,5,6,7,8,9,10,0,0,0,11,12 ]) == 1+3+5+7+9+11)
    print('Passed!')

def testOddsOnly():
    print('Testing oddsOnly()...', end='')
    assert(oddsOnly([ ]) == [ ])
    assert(oddsOnly([ 2, 4, 6 ]) == [ ]) 
    assert(oddsOnly([ 2, 4, 6, 7 ]) == [ 7 ])
    assert(oddsOnly([ -1, -2, -3 ]) == [-1, -3])
    assert(oddsOnly([ 1,2,3,4,5,6,7,8,9,10,0,0,0,11,12 ]) == [1,3,5,7,9,11])
    print('Passed!')

def testMaxOdd():
    print('Testing maxOdd()...', end='')
    assert(maxOdd([ ]) == None)
    assert(maxOdd([ 2, 4, 6 ]) == None) 
    assert(maxOdd([ 2, 4, 6, 7 ]) == 7)
    assert(maxOdd([ -1, -2, -3 ]) == -1)
    assert(maxOdd([ 1,2,3,4,5,6,7,8,9,10,0,0,0,11,12 ]) == 11)
    print('Passed!')

def testHasConsecutiveDigits():
  print('Testing hasConsecutiveDigits()...', end='')
  assert(hasConsecutiveDigits(1123) == True)
  assert(hasConsecutiveDigits(-1123) == True)
  assert(hasConsecutiveDigits(1234) == False)
  assert(hasConsecutiveDigits(0) == False)
  assert(hasConsecutiveDigits(1233) == True)
  print("Passed!")

def testAlternatingSum():
    print('Testing alternatingSum()...', end='')
    assert(alternatingSum([1,2,3,4,5]) == 1-2+3-4+5)
    assert(alternatingSum([ ]) == 0)
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    testOddCount()
    testOddSum()
    testOddsOnly()
    testMaxOdd()
    testHasConsecutiveDigits()
    testAlternatingSum()
    runFreddyFractalViewer()

def main():
    cs112_s22_week9_linter.lint()
    testAll()

if (__name__ == '__main__'):
    main()
