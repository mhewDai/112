import random
from board import Board
# this program makes hints that are translated into the board on the other program
class hint:
    def __init__(self,board,flagged):
        self.board = board
        self.looked = board.looked
        self.numBombs = board.numBombs
        self.flagged = flagged
        self.nearbyBombs = 0
        self.possibleHints = set()

    def naiveSolution(self):
        flaggingTiles = []
        for (row,col) in self.board.looked:
            count = 0
            neighbors = nearbyTiles(row,col,9,9)
            for tiles in neighbors:
                if tiles not in self.board.looked:
                    count += 1
                    flaggingTiles.append(tiles)
            if count == self.board.board[row][col]:
                for values in flaggingTiles:
                    self.possibleHints.add(values)
            flaggingTiles = []
            
    def hint(self):
        for locations in self.flagged:
            if locations in self.possibleHints:
                self.possibleHints.remove(locations)
        if len(self.possibleHints) > 0:
            clue = random.sample(self.possibleHints,1)[0]
            return clue
        return None        
	
def nearbyTiles(row,col,rows,cols):
    nearSquares = []
    for i in range(-1,2):
        for j in range(-1,2):
            newRow,newCol = row + i, col + j
            if ((newRow,newCol) != (row,col) and 
                0 <= newRow < rows and 0 <= newCol != cols):
                nearSquares.append((newRow,newCol))
    return nearSquares

