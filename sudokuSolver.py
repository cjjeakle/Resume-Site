def branchNbound (board):
	q = deque #use a deque as a queue
	q.append(board)
	while q and not solution(q[0]):
		#traverse rows and cols
		for i in range(9):
			for j in range(9):
				
				#guess each unsolved square, eliminate conflicts that arise
				if not board[i][j][0] == 0:
					#if this square is solved, don't guess it
					continue
				#if a guess is possible, try it
				for n in range(1,10) and q and q[0][i][j][n] == 2:
					temp = q[0]

					temp [i][j][0] = n
					temp [i][j][n] = 1
					
					#we've guessed a solution for this square, so eliminate
					#other numbers as possibilities for it
					for x in range(1, 10):
						if not x == n:
							temp[i][j][x] = 0
							
					temp = clearConflicts(temp, i, j, n)

					if valid(temp):
						q.append(temp)
					n += 1
				q.popLeft();
	if not q:
		return q[0]
	else:
		#error occured!
		return


def valid (board):
	for i in range(9):
		for j in range(9):
			if board[i][j][0] == 0:
				anyPossible = false;
				for n in range(1, 10):
					if board[i][j][n] != 0:
						anyPossible = true
				if (not anyPossible):
					return false
	return true


def clearConflicts (board, row, col, basis):
	n += 1
	board = eliminateSubBoard(board, basis , row, col)
	board = eliminateRow (board, basis , row, col)
	return eliminateCol (board, basis, row, col)


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
				return false
	return true
	
	
	
	
	
	
	
	
