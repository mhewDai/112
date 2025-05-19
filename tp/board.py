import random
# this program makes hints generates the board and its many characteristics
class Board:
    def __init__(self,rows,cols,irow,icol,numBombs):
        self.rows,self.cols = rows,cols
        self.irow,self.icol = irow,icol
        self.looked = set()
        self.bombPlaces = None
        self.numBombs = numBombs
        self.board = self.settingDownBombs()
        self.makingNumbers()
        self.search(self.irow,self.icol)
        self.tilesList = None
        #when you dig at a specific location on the board, 
        #that get stored in this set and a new board is made
    def settingDownBombs(self):
        availableSpots = []
        unavailable = [(self.irow,self.icol)]
        board = [[None] * self.cols for i in range(self.rows)]
        neighborsL = nearbyTiles(self.irow,self.icol,self.rows,self.cols)
        unavailable.extend(neighborsL)
        for i in range(self.rows):
            for j in range(self.cols):
                if (i,j) not in unavailable:
                    availableSpots.append((i,j))
        self.bombPlaces = random.sample(availableSpots,self.numBombs)
        for i in range(self.rows):
            for j in range(self.cols):
                if (i,j) in self.bombPlaces:
                    board[i][j] = '*'
        return board

    def makingNumbers(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == '*':
                    continue
                self.board[i][j] = self.numSurroundingBombs(i,j)

    def numSurroundingBombs(self,row,col):
        numberOfNearbyBombs = 0
        for rows in range(max(0,row-1),min(self.rows,(row+1)+1)):
            for cols in range(max(0,col-1),min(self.cols,(col+1)+1)):
                if rows == row and cols == col:
                    continue
                if self.board[rows][cols] == '*':
                    numberOfNearbyBombs += 1
        return numberOfNearbyBombs

    def search(self,row,col):
        self.looked.add((row,col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        for rows in range(max(0,row-1),min(self.rows,(row+1)+1)):
            for cols in range(max(0,col-1),min(self.cols,(col+1)+1)):
                if (rows,cols) not in self.looked:
                    self.search(rows,cols)
        return True

def nearbyTiles(row,col,rows,cols):
    nearSquares = []
    for i in range(-1,2):
        for j in range(-1,2):
            newRow,newCol = row + i, col + j
            if ((newRow,newCol) != (row,col) and 
                0 <= newRow < rows and 0 <= newCol != cols):
                nearSquares.append((newRow,newCol))
    return nearSquares
