def sudokuSolver (userInput):
	#this mess generates the board using unique nested lists rather than references
	#(that bug took some serious debugging to find!)
	board = [[[2]*10 for _ in xrange(9)] for _ in xrange(9)]
	for i in range(9):
		for j in range(9):
			board[i][j][0] = 0
	givens = 0
	for i in range(9):
		for j in range(9):
			if (userInput[i][j] > 0):
				givens += 1
				board[i][j][0] = userInput[i][j]
				clearSquareConflicts(board, i, j, userInput[i][j])
				
	for i in range(9):
		for j in range(9):
			if (board[i][j][0] >= 1):
				clearBoardConflicts(board, i, j, board[i][j][0])
	if givens < 12:
		return userInput, givens
	#board, givens = branchNbound(board)
	
	for i in range(10):
		board = solveSingletons(board)
		board = findLoneSolutions(board)
	
	if board:
		for i in range(9):
			for j in range(9):
				userInput[i][j] = board[i][j][0]
	return userInput, givens


def branchNbound (board):
	iters = 0
	q = collections.deque() #use a deque as a queue
	q.append(board)
	while q and not solution(q[0]):
		iters += 1
		#traverse rows and cols
		copy = q.popleft()
		for i in range(9):
			for j in range(9):
				#guess each unsolved square, eliminate conflicts that arise
				if not board[i][j][0] == 0:
					#if this square is solved, don't guess it
					continue
				#if a guess is possible, try it
				n = 1
				while n < 10:
					if (copy[i][j][n] == 2):
						temp = copy
						temp = clearSquareConflicts(temp, i, j, n)
						temp = clearBoardConflicts(temp, i, j, n)
						temp = solveSingletons(temp)
						temp = findLoneSolutions(temp)

						if valid(temp):
							q.append(temp)
						n += 1
	if q:
		return q[0], iters
	else:
		#error occured!
		return board, iters


def valid (board):
	for i in range(9):
		for j in range(9):
			if board[i][j][0] == 0:
				anyPossible = False;
				for n in range(1, 10):
					if board[i][j][n] != 0:
						anyPossible = True
				if (not anyPossible):
					return False
	return True

def clearSquareConflicts (board, row, col, basis):
	board[row][col][0] = basis
	board[row][col][basis] = 1
	for n in range(1, 10):
		if not n == basis:
			board[row][col][n] = 0
	return board

def clearBoardConflicts (board, row, col, basis):
	board = eliminateSubBoard(board, row, col, basis)
	board = eliminateRow (board, row, col, basis)
	return eliminateCol (board, row, col, basis)


def eliminateSubBoard (board, row, col, basis):
	subBoardRow = row//3
	subBoardCol = col//3

	for i in range(9):
		for j in range(9):
			if ((board [i][j][0] == 0) and (i//3 == subBoardRow)\
			and (j//3 == subBoardCol) and (i != row) and (j != col)):
				board[i][j][basis] = 0
	return board


def eliminateRow (board, row, col, basis):
	for j in range(9):
		if ((board [row][j][0] == 0) and (j != col)):
			board[row][j][basis] = 0;
	return board


def eliminateCol (board, row, col, basis):
	for i in range(9):
		if ((board [i][col][0] == 0) and (i != row)):
			board[i][col][basis] = 0;
	return board


def solution (board):
	for i in range(9):
		for j in range(9):
			if board[i][j][0] == 0:
				return False
		raise WTF
	return True
	
#finds squares with only one possible solution and makes that the answer
def solveSingletons (board):
	for i in range(9):
		for j in range(9):
			#if no solution for this square, check possibilities
			if board[i][j][9] == 0:
				numPossible = 0
				possibleAns = 0
				for n in range (1, 10):
					if board[i][j][n] == 2:
						numPossible += 1
						possibleAns = n
				#if there is only one possibility, that is sol
				if numPossible == 1:
					board [i][j][possibleAns] = 1
					board [i][j][9] = possibleAns
					board = eliminateSubBoard(board, i, j, possibleAns)
					board = eliminateRow (board, i, j, possibleAns)
					board = eliminateCol (board, i, j, possibleAns)
	return board

#finds lone possibilities and makes them the designated solution
def findLoneSolutions (board):
	for i in range(9):
		for j in range(9):
			board = rowLoneSolutions (board, i, j)
			board = colLoneSolutions (board, i, j)
			board = onlyInARow (board, i, j)
			board = onlyInACol (board, i, j)
	board = subBoardLoneSolution (board)
	return board
	
	
def rowLoneSolutions (board, row, col):
	#iterate possible square solutions
	for n in range(1, 10):
		#if the number is possible in the given row and col
		if board[row][col][n] == 2:
			alternatives = 0
			for j in range(9): 
				if board [row][j][9] == 0 and not j == col and\
				board[row][j][n] == 2:
					alternatives += 1
			#if a number is a possible in the given location and 
			#nowhere else in the row, then it is that square's sol
			if alternatives == 0 and board[row][col][n] == 2:
				board[row][col][0] = n
				board[row][col][n] = 1
				for x in range(9):
					if not x == n:
						board[row][col][x] = 0;
				board = eliminateSubBoard (board, row, col, n)
				board = eliminateRow (board, row, col, n)
				board = eliminateCol (board, row, col, n)
	return board
	

def colLoneSolutions (board, row, col):
	#iterate possible square solutions
	for n in range (1, 10):
		#if the number is possible in the given row and col
		if board[row][col][n] == 2:
			alternatives = 0
			for i in range (9):
				if board [i][col][9] == 0 and not i == row and\
				board[i][col][n] == 2:
					alternatives += 1
			#if a number is a possible in the given location and 
			#nowhere else in the col, then it is that square's sol
			if alternatives == 0 and board[row][col][n] == 2:
				board[row][col][0] = n
				board[row][col][n] = 1
				for x in range(9):
					if not x == n:
						board[row][col][x] = 0
				board = eliminateSubBoard (board, row, col, n)
				board = eliminateRow (board, row, col, n)
				board = eliminateCol (board, row, col, n)
	return board


def subBoardLoneSolution (board):
	for subBoardRow in range(3):
		for subBoardCol in range(3):
			#iterate the possible square solutions
			for n in range(1, 10):
				possibilities = 0
				row = 0
				col = 0
				#identify any matches for the val in the sub-board
				for i in range(9):
					for j in range(9):
						if i//3 == subBoardRow and j//3 == subBoardCol\
						and board[i][j][n] == 2:
							possibilities += 1
							row = i
							col = j
				#if a number is possible in only one location,
				#it is that location's solution
				if possibilities == 1:
					board [row][col][0] = n
					board [row][col][n] = 1
					for x in range(9):
						if not x == n:
							board[row][col][x] = 0
					board = eliminateSubBoard(board, row, col, n)
					board = eliminateRow (board, row, col, n)
					board = eliminateCol (board, row, col, n)
	return board

def onlyInACol (board, row, col):
	subBoardRow = row//3
	subBoardCol = col//3
	outsideCol = 0

	#iterate through numbers
	for n in range (1, 10):
		#if a number is possible for the given square
		if board[row][col][n] == 2:
			for i in range(9):
				for j in range(9):
					#if another row in that sub-board contains the number
					if i//3 == subBoardRow and not j == col and\
					j//3 == subBoardCol and board[i][j][n] == 2:
						outsideCol += 1
		#if the current number "n" is only in this col, remove it as a 
		#possibility for for this col in other sub-boards
		if outsideCol == 0 and board[row][col][n] == 2:
			#eliminate that number as a possibility outside this 
			#sub-board but inside this col
			for i in range(9):
				if not i//3 == subBoardRow:
					board[i][col][n] = 0
	return board

def onlyInARow (board, row, col):
	subBoardRow = row//3
	subBoardCol = col//3
	outsideRow = 0

	#iterate through numbers
	for n in range (1, 10):
		#if a number is possible for the given square
		if board[row][col][n] == 2:
			for i in range(9):
				for j in range(9):
					#if another col in that sub-board contains the number,
					#iterate the counter
					if j//3 == subBoardCol and not i == row and\
					i//3 == subBoardRow and board[i][j][n] == 2:
						outsideRow += 1
		#if the current number "n" is only in this row, remove it as a 
		#possibility for for this row in other sub-boards
		if outsideRow == 0 and board[row][col][n] == 2:
			#eliminate that number as a possibility outside this 
			#sub-board but inside this row
			for j in range(9):
				if not j//3 == subBoardCol:
					board[row][j][n] = 0
	return board
