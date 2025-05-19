import copy

class Matrix:
	def __init__(self,matrix):
		self.matrix = matrix
		self.rows = len(matrix)
		self.cols = len(matrix[0])

	def __repr__(self):
		return f'<{self.rows}x{self.cols} Matrix: {self.matrix}>'

	def getRow(self,row):
		if row <= self.rows:
			return self.matrix[row]

	def getCol(self,col):
		if col <= self.cols:
			result = []
			for rows in range(self.rows):
				result.append(self.matrix[rows][col])
			return result

	def addMatrix(self,otherMatrix):
		newClass = copy.deepcopy(self)
		if self.rows == otherMatrix.rows and self.cols == otherMatrix.cols:
			result = [[0] * self.cols for i in range(self.rows)]
			for rows in range(self.rows):
				for cols in range(self.cols):
					result[rows][cols] += self.getRow(rows)[cols] + otherMatrix.getRow(rows)[cols]
			newClass.matrix = result
			return newClass



def testMatrixClass():
	print('Testing Matrix class...', end='')
	m1 = Matrix([[1,2,3],[4,5,6]])
	assert(str(m1) == '<2x3 Matrix: [[1, 2, 3], [4, 5, 6]]>')
	assert(m1.rows == 2)
	assert(m1.cols == 3)
	assert(m1.getRow(0) == [1,2,3])
	assert(m1.getCol(0) == [1,4])
	assert(m1.getRow(5) == m1.getCol(42) == None) # handle out-of-bounds indexes
	m2 = Matrix([[10,20,30],[40,50,60]]) # make another matrix
	assert(str(m2) == '<2x3 Matrix: [[10, 20, 30], [40, 50, 60]]>')
	m3 = m1.addMatrix(m2) # create new Matrix instance where each
	# value in m1 is added to the corresponding
	# value in m2
	assert(str(m3) == '<2x3 Matrix: [[11, 22, 33], [44, 55, 66]]>')
	# Be sure the previous operation was non-destructive:
	assert(str(m1) == '<2x3 Matrix: [[1, 2, 3], [4, 5, 6]]>')
	m4 = Matrix([[1]])
	assert(str(m4) == '<1x1 Matrix: [[1]]>')
	assert(m1.addMatrix(m4) == None) # handle mismatched dimensions when adding
	print('Passed!')

testMatrixClass()

def removeEvens(L):
	if L == []:
		return []
	else:
		if L[0] % 2 == 0:
			return removeEvens(L[1:])
		else:
			return [L[0]] + removeEvens(L[1:])

def removeEvens2(L):
	return removeEvens2Helper(L,[])

def removeEvens2Helper(L,M):
	if L == []:
		return M
	else:
		if L[0] % 2 == 1:
			M.append(L[0])
		return removeEvens2Helper(L[1:],M)

def removeEvens3(L,i = 0):
	if i >= len(L):
		return None
	else:
		if L[i] % 2 == 0:
			L.remove(L[i])
		else:
			i += 1
		removeEvens3(L,i)

def testremovEvens():
	print('Testing Remove evens...', end='')
	assert((removeEvens([1,2,3,4,5,6]) == [1,3,5]))
	assert((removeEvens2([1,2,3,4,5,6]) == [1,3,5]))
	L = [1,2,3,4,5,6]
	removeEvens3(L)
	assert(L == [1,3,5])
	print('Passed!')

testremovEvens()

def arrange(L, d):
	return solve([], copy.copy(L), d)

def solve(resultSoFar, remainingList, d):
	if remainingList == []:
		return resultSoFar # Blank 1
	else:
		#For each remaining element
		for i in range(len(remainingList)):
		#Get element for next attempted move
			v = remainingList[i]
			if (resultSoFar == []) or abs(remainingList[len(remainingList) - 1] - v <= d): # Blank 2
				remainingList.pop(i) # remove v from the remaining list
				resultSoFar.append(v) # and add it to the resultSoFar list
				result = solve(resultSoFar,remainingList,d)  # Blank 3
				if result != None: # Blank 4
					return result #Hint: You need to define result somewhere
			#Undo the move if no solution
			remainingList.insert(i, v) # replace v in the remaining list
			resultSoFar.pop() # and remove it from the resultSoFar list
	return None

class Table(object):
	def __init__(self,table):
		self.table = table
		self.rows,self.cols = len(table),len(table[0])

	def __eq__(self,other):
		return isinstance(other,Table) and (self.table == other.table)

	def getDims(self):
		return self.rows,self.cols

	def lookup(self,row,col):
		if 0 <= row < self.rows and 0 <= col < self.cols:
			return self.table[row][col]
		return "Out Of Bounds"

	def find(self,n):
		L = []
		for rows in range(self.rows):
			for cols in range(self.cols):
				if self.table[rows][cols] == n:
					L.append((rows,cols))
		return L

	def add(self, L):
		result = [[0] * self.cols for i in range(self.rows)]
		if type(L) != Table:
			return "Can't add non-Table"
		elif self.rows != L.rows and self.cols != L.cols:
			return "Can't add different dimensions"
		for rows in range(self.rows):
			for cols in range(self.cols):
				result[rows][cols] += L.table[rows][cols] + self.table[rows][cols]
		return Table(result)
	def __repr__(self):
		return f"Table of size ({self.rows}, {self.cols})"

def testTable():
	print("Testing Table class...", end="")
	T1 = Table([[1, 5, 1, 1, 2],
	[1, 5, 1, 2, 2],
	[1, 5, 1, 5, 0]])
	assert(T1.getDims() == (3, 5)) # get the dimensions.
	assert(T1.lookup(0, 0) == 1)
	assert(T1.lookup(2, 4) == 0)
	assert(T1.lookup(-1, 1) == "Out Of Bounds")
	assert(T1.lookup(1, 5) == "Out Of Bounds")
	assert(T1.find(0) == [(2, 4)]) # find all zeros and return their (row,col).
	assert(T1.find(2) == [(0, 4), (1, 3), (1, 4)])
	T1Copy = Table([[1, 5, 1, 1, 2],
	[1, 5, 1, 2, 2],
	[1, 5, 1, 5, 0]])
	T2 = Table([[1, 2],
	[3, 4]])
	T3 = Table([[5, 7],
	[6, 8]])
	assert(T1 == T1Copy) # equality should work!
	assert(T1 != T2)
	assert(T2 != T3)
	assert(T2.add(42) == "Can't add non-Table")
	assert(T2.add(T1) == "Can't add different dimensions")
	T4 = T2.add(T3)
	assert(T4.lookup(0, 0) == 6)
	assert(T4.lookup(0, 1) == 9)
	assert(T4.lookup(1, 0) == 9)
	assert(T4.lookup(1, 1) == 12)
	assert(T2.lookup(0, 0) == 1) # Make sure that .add() is nondestructive...
	assert(T3.lookup(1, 1) == 8)
	assert(repr(T1) == "Table of size (3, 5)")
	assert(repr(T4) == "Table of size (2, 2)")
	print("Passed!")

testTable()


def gcd(x, y):
    if (y == 0): return x
    else: return gcd(y, x%y)
