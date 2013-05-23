import os
import pyjade
import collections
#import sudokuSolver
from flask import Flask,render_template,send_from_directory
#from flask.ext.wtf import Form, TextField, TextAreaField, TextArea

app = Flask(__name__)
# use the jade template engine
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route('/')
def index():
	obj = {
		"title": "Chris Jeakle",
		"text": "#YOLO"
	};
	return render_template('index.jade', **obj)

@app.route('/myClasses')
def myClasses():

	myClasses = ["EECS 183: Elementary Programming Concepts",
				"EECS 203: Discrete Mathematics",
				"EECS 280: Programming & Data Structures",
				"EECS 281: Data Structures & Algorithms",
				"EECS 370: Computer Architecture",
				"EECS 376: Foundations of Computer Science",
				"EECS 481: Software Engineering"]
	
	myEnrollment = ["EECS 381: Object-Oriented and Advanced Programming",
					"EECS 484: Database Management Systems"]
	
	myFutureClasses = ["EECS 443: Senior Thesis Course (Honors)",
					"EECS 482: Introduction to Operating Systems"]
	
	obj = {
		"myClasses": myClasses,
		"myEnrollment": myEnrollment,
		"myFutureClasses": myFutureClasses
	};
	return render_template('myClasses.jade', **obj)

@app.route('/sudokuSolver')
def sudokuSolver():

	#userInput = sudokuSolver(userInput)
	obj = {
		#"userInput": userInput
	};
	return render_template('sudokuSolver.jade', **obj)
	
# this guy handles static files
@app.route('/<path:filename>')
def send_pic(filename):
	print(filename)
	return send_from_directory('./public/', filename)



################################################################################



def sudokuSolver (userInput):
	#generate a board of unique nested lists rather than references
	#(using append in three dimensions creates shallow rather than deep copies)
	board = [[[2]*10 for _ in xrange(9)] for _ in xrange(9)]
	for i in range(9):
		for j in range(9):
			board[i][j][0] = 0
			
	for i in range(9):
		for j in range(9):
			if (userInput[i][j] > 0):
				board[i][j][0] = userInput[i][j]
				clearSquareConflicts(board, i, j, userInput[i][j])
				
	for i in range(9):
		for j in range(9):
			if (board[i][j][0] >= 1):
				clearBoardConflicts(board, i, j, board[i][j][0])
	
	#solve the sudoku
	for i in range(10):
		board = solveSingletons(board)
		board = findLoneSolutions(board)
	board = branchNbound(board)
	
	if board:
		for i in range(9):
			for j in range(9):
				userInput[i][j] = board[i][j][0]
	return userInput


def branchNbound (board):
	q = collections.deque() #use a deque as a queue
	q.append(board)
	while q and not solution(q[0]):
		#traverse rows and cols
		copy = q.popleft()
		for i in range(9):
			for j in range(9):
				#guess each unsolved square, eliminate conflicts that arise
				if copy[i][j][0] == 0:
					n = 1
					while n < 10:
						temp = clearSquareConflicts(copy, i, j, n)
						temp = clearBoardConflicts(temp, i, j, n)
						
						for k in range(10):
								temp = solveSingletons(temp)
								temp = findLoneSolutions(temp)
						
						if valid(temp):
							q.append(temp)
						n += 1
	if q:
		return q[0]
	else:
		#error occured!
		return board


def valid (board):
	for i in range(9):
		for j in range(9):
			if board[i][j][0] == 0:
				anyPossible = False;
				for n in range(1, 10):
					if board[i][j][n] != 0:
						anyPossible = True
				if not anyPossible:
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
	return True
	
#finds squares with only one possible solution and makes that the answer
def solveSingletons (board):
	for i in range(9):
		for j in range(9):
			#if no solution for this square, check possibilities
			if board[i][j][0] == 0:
				numPossible = 0
				possibleAns = 0
				for n in range (1, 10):
					if board[i][j][n] == 2:
						numPossible += 1
						possibleAns = n
				#if there is only one possibility, that is sol
				if numPossible == 1:
					clearSquareConflicts(board, i, j, possibleAns)
					clearBoardConflicts(board, i, j, possibleAns)
	return board

#finds lone possibilities and makes them the designated solution
def findLoneSolutions (board):
	for i in range(9):
		for j in range(9):
			board = rowLoneSolutions (board, i, j)
			board = colLoneSolutions (board, i, j)
			board = eliminateOutsideSubboardRow (board, i, j)
			board = eliminateOutsideSubboardCol (board, i, j)
	board = subBoardLoneSolution (board)
	return board
	
	
def rowLoneSolutions (board, row, col):
	#iterate possible square solutions
	for n in range(1, 10):
		#if the number is possible in the given row and col
		if board[row][col][n] == 2:
			alternatives = 0
			for j in range(9): 
				if board [row][j][0] == 0 and not j == col and\
				board[row][j][n] == 2:
					alternatives += 1
			#if a number is a possible in the given location and 
			#nowhere else in the row, then it is that square's sol
			if alternatives == 0:
				clearSquareConflicts(board, row, col, n)
				clearBoardConflicts(board, row, col, n)
	return board
	

def colLoneSolutions (board, row, col):
	#iterate possible square solutions
	for n in range (1, 10):
		#if the number is possible in the given row and col
		if board[row][col][n] == 2:
			alternatives = 0
			for i in range (9):
				if board [i][col][0] == 0 and not i == row and\
				board[i][col][n] == 2:
					alternatives += 1
			#if a number is a possible in the given location and 
			#nowhere else in the col, then it is that square's sol
			if alternatives == 0:
				clearSquareConflicts(board, row, col, n)
				clearBoardConflicts(board, row, col, n)
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
					clearSquareConflicts(board, row, col, n)
					clearBoardConflicts(board, row, col, n)
	return board

#Identifies possible solutions that only exist in a single col of a sub-board
#This information allows us to eliminate the number as a possibility in the col outside
#the current sub-board
def eliminateOutsideSubboardCol (board, row, col):
	subBoardRow = row//3
	subBoardCol = col//3
	outsideCol = 0

	#iterate through possible square solutions
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

#see eliminateOutsideSubboardCol for details on this function
def eliminateOutsideSubboardRow (board, row, col):
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






################################################################################






if __name__ == '__main__':
	# Bind to PORT if defined (environment variable on heroku)
	port = int(os.environ.get('PORT', 3000))

	app.run(host='0.0.0.0', port=port, debug=True)
	

	

