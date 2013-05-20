import os
from flask import Flask,render_template,send_from_directory
import pyjade

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

	myClasses = ["EECS 183: Elementary Programming Concepts", "EECS 203: Discrete Mathematics",
		"EECS 280: Programming & Data Structures", "EECS 281: Data Structures & Algorithms",
		"EECS 370: Computer Architecture", "EECS 376: Foundations of Computer Science",
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
	
	
# this guy handles static files
@app.route('/<path:filename>')
def send_pic(filename):
	print(filename)
	return send_from_directory('./public/', filename)

if __name__ == '__main__':
	# Bind to PORT if defined (environment variable on heroku)
	port = int(os.environ.get('PORT', 3000))

	app.run(host='0.0.0.0', port=port, debug=True)
	
	
	

