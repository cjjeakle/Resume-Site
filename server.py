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

@app.route('/education')
def myClasses():
	obj = {
	};
	return render_template('education.jade', **obj)

@app.route('/sudokusolver')
def sudokuSolver():
	boardNames = []
	for i in range(9):
		temp = []
		for j in range(9):
			temp.append('sq' + str(i*9+j))
		boardNames.append(temp)
		
	obj = {
		"boardNames": boardNames,
	};
	return render_template('sudokuSolver.jade', **obj)
	
@app.route('/pingpong')
def pong():
	obj = {
	};
	return render_template('pingPong.jade', **obj)

@app.route('/about')
def about():
	obj = {
	};
	return render_template('about.jade', **obj)

# Handles static files
@app.route('/<path:filename>')
def send_pic(filename):
	print(filename)
	return send_from_directory('./static/', filename)

if __name__ == '__main__':
	# Bind to PORT if defined (environment variable on heroku)
	port = int(os.environ.get('PORT', 3000))

	app.run(host='0.0.0.0', port=port, debug=True)
	

	

