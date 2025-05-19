"""
andrew id: mdai2
#partner's andrew id: haisuz

#style grading: 
Matthew' code:

#Line 53 has unnecessary white space
#the rest looks fine, no need for improvement

"""
import random
#https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html

def playLightsOut():
    gridSize = int(input("What size grid would you like:",))
    #determines size of gride
    board = makeBoard(gridSize,gridSize) 
    solvedBoard = [([0] * gridSize) for gridSize in range(gridSize)]
    while board != solvedBoard:
        print(repr2dList(board))
        print("Which switches would you like to press?",
        "The correct format is row,column.")
        choice = input("Position:")
        #accounts for wrong inputs like out of bounds or strings
        if wrongInputs(choice,gridSize):
            board = flipSwitch(board,int(choice[0]),int(choice[2]))
        else:
            print("Please use the correct format")
    print("Congrats You Have Won!")

def repr2dList(L):
    if (L == []): return '[]'
    output = [ ]
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)

def makeBoard(row,col):
    outsideList = []
    for i in range(row):
    #making a random lights out gride 
        insideList = []
        for j in range(col):
            num = random.randint(0,1)
            insideList.append(num)
        outsideList.append(insideList)
    
    return outsideList

def wrongInputs(input,row):
    #input is a string
    inputLength = 3
    if len(input) < inputLength or len(input) > inputLength:
        return False
    else:
        if (not input[1].isspace() or not input[0].isdigit() or 
             not input[2].isdigit()):
            return False
        elif input[0].isdigit() or input[2].isdigit():
            if int(input[0]) > row or int(input[2]) > row:
                print("Submission is out of bounds")
                return False
    return True
    
def flipSwitch(board,foundR,foundC):
    rows, cols = len(board), len(board[0])
    result = board[foundR][foundC]
    if result == 0:
        board[foundR][foundC] += 1
    else:
        board[foundR][foundC] = 0
    for drow in [-1, 0, +1]:
        for dcol in [-1, 0, +1]:
            if ((drow, dcol) != (0, 0) and 
                ((foundR + drow)>=0 and (foundR + drow)< rows and 
                (foundC + dcol)>=0 and (foundC + dcol)< cols) 
                and abs(drow) != abs(dcol)):
                dResult = board[foundR+drow][foundC+dcol]
                #add one to turn on place and minus one to turn off
                if dResult==0:
                    board[foundR+drow][foundC+dcol] += 1
                else:
                    board[foundR+drow][foundC+dcol] -= 1
    return board

playLightsOut()


