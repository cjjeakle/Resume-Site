import os
import copy
import pyjade
import SudokuSolver
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['TESTING'] = False

# use the jade template engine
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route('/')
def index():
	obj = {
		"title": "Chris Jeakle",
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
	boardNames = []
	for i in range(9):
		temp = []
		for j in range(9):
			temp.append('sq' + str(i*9+j))
		boardNames.append(temp)
	
	board = []
	for i in range(9):
		temp = []
		for j in range(9):
			temp.append(0)
		board.append(temp)
		
	obj = {
		"url": "/solveSudoku",
		"post": "post",
		"boardNames": boardNames,
		"board": board,
		"annotation": "",
	};
	return render_template('sudokuSolver.jade', **obj)

@app.route('/solveSudoku',  methods=['POST'])
def solveSudoku():
	boardNames = []
	for i in range(9):
		temp = []
		for j in range(9):
			temp.append('sq' + str(i*9+j))
		boardNames.append(temp)
		
	board = [[0]*9 for _ in xrange(9)]
	for i in range(9):
		for j in range(9):
			temp = request.form.get('sq'+str(i*9+j), '0')
			if temp.isdigit():
				board[i][j] = int(temp)
	
	annotation = "Success!"		
	try:
		SudokuSolver.sudokuSolver(board)
	except SudokuSolver.TooFewInputs:
		annotation = "Please provide more givens"
	except SudokuSolver.SolverFailed:
		annotation = ("The solver failed, something went wrong!</br>" +
					"Please ensure you provided a valid puzzle")
	
	obj = {
		"url": "/solveSudoku",
		"post": "post",
		"boardNames": boardNames,
		"board": board,
		"annotation": annotation,
	};
	return render_template('sudokuSolver.jade', **obj)

# this guy handles static files
@app.route('/<path:filename>')
def send_pic(filename):
	print(filename)
	return send_from_directory('./public/', filename)

if __name__ == '__main__':
	# Bind to PORT if defined (environment variable on heroku)
	port = int(os.environ.get('PORT', 3000))

	app.run(host='0.0.0.0', port=port, debug=True)
	

	

