################################################
# Permanent Orienteering Course WebApp
#
#    (c) 2014 Eric Jones
#    Licensed under the MIT License
#    https://github.com/ercjns/o-webapp
################################################


# Switching to PostgreSQL (and flask-sqlalchemy) for deployment on heroku dev.
# http://blog.y3xz.com/blog/2012/08/16/flask-and-postgresql-on-heroku/
# http://tech.pro/tutorial/1259/how-to-deploy-simple-and-larger-flask-apps-on-heroku

# >>>from oapp import db
# >>>db.create_all()
# >>>from oapp import _fillCourseTable
# >>>_fillCourseTable()




# imports
import os
from flask.ext.sqlalchemy import SQLAlchemy
from contextlib import closing
from flask import Flask, render_template, url_for, redirect, g, session


################################################
# Create the Flask application, connect to the db
################################################

app =  Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'My Development Key is Public!'

db = SQLAlchemy(app)


################################################
# Set up the databases, define database access functions
################################################

class Runner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	venuecode = db.Column(db.String(10))
	course = db.Column(db.Integer)
	punch = db.Column(db.Integer)
	punch_on_course = db.Column(db.Integer)
	punch_time = db.Column(db.String(100))
	start_time = db.Column(db.String(100))
	end_time = db.Column(db.String(100))
	finished = db.Column(db.Boolean)

	def __init__(self, venuecode, course):
		self.venuecode = venuecode
		self.course = course
		self.finished = False

	def __repr__(self):
		return '<RunnerID %d, at %s on course %d>' % (self.id, self.venuecode, self.course)

class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	venuecode = db.Column(db.String(10))
	venuefull = db.Column(db.String(100))
	coursecode = db.Column(db.Integer)
	coursefull = db.Column(db.String(100))
	distance = db.Column(db.String(20))
	climb = db.Column(db.String(20))
	start = db.Column(db.Integer)
	controls = db.Column(db.String(100))
	finish = db.Column(db.Integer)

	def __init__(self, venuecode, venuefull, coursecode, coursefull,
				distance, climb, start, controls, finish):
		self.venuecode = venuecode
		self.venuefull = venuefull
		self.coursecode = coursecode
		self.coursefull = coursefull
		self.distance = distance
		self.climb = climb
		self.start = start
		self.controls = controls
		self.finish = finish

	def __repr__(self):
		return '<CourseID: %i, %s (%i) at %s>' % (self.id, self.coursefull, self.coursecode, self.venuefull)


def _fillCourseTable():
	mag1 = Course('mag', 'Magnuson Park', 1, 'Beginner', '1.4 km', '0m', 0, '0,31,32,33,34,35,36,999', 999)
	mag2 = Course('mag', 'Magnuson Park', 2, 'Intermediate', '1.7 km', '0m', 0, '0,42,43,33,44,45,46,40,47,41,999', 999)
	mag3 = Course('mag', 'Magnuson Park', 3, 'Advanced', '2.8 km', '0m', 0, '0,36,37,38,39,40,35,41,43,32,999', 999)
	fts1 = Course('fts', 'Ft. Steilacoom Park', 1, 'Beginner', '1.1 km', '15m', 0, '0,33,34,35,36,37,38,999', 999)
	db.session.add(mag1)
	db.session.add(mag2)
	db.session.add(mag3)
	db.session.add(fts1)
	db.session.commit()
	return 'done'


################################################
# Webapp Routes
################################################

@app.route('/')
def index():
	'''page should display general information about what courses are avaiable'''
	locs = Course.query.all()

	venues = []
	for l in locs:
		venues.append((l.venuecode, l.venuefull))
	venues = list(set(venues))

	# to-do clean this up to pass a list of objects to the template
	return render_template("index.html",
							venues=venues)


@app.route('/<venuecode>')
def venue(venuecode):
	'''look up the code in the db, get the name + courses, display it
	if the code is not valid, redirect to a landing page'''

	courses = Course.query.filter_by(venuecode=venuecode).all()
	if len(courses) == 0:
		#should probably error here, but for now redirect
		return redirect(url_for('index'))

	venuefull = courses[0].venuefull
	venuecode = courses[0].venuecode

	# to-do rewrite this template with better course object handling
	return render_template('venuehome.html',
							venuecode=venuecode,
							venuename=venuefull,
							courses = courses)


@app.route('/<venuecode>/start/<int:course>')
def init_course(venuecode, course):
	''' to start a coruse, add a row to the runners table,
	set a session on the client, and re-direct to the proper control page'''

	#to-do VALIDATE that venue and course are valid values!!!

	runner = Runner(venuecode, course)
	print runner.id
	db.session.add(runner)
	db.session.commit()

	session['runnerID'] = runner.id

	return redirect(url_for('visit_control',
							venuecode=venuecode,
							control=0))


@app.route('/<venuecode>/<int:control>')
def visit_control(venuecode, control):
	print('FUNCTION: VISIT CONTROL', control)

	#to-do VALIDATE that venuecode and control are valid values
	#to-do Case for visiting the same control twice in a row (page reload)
	#to-do Show a map when you're off course...

	runnerid = session['runnerID']
	if runnerid == None:
		return redirect(url_for('venue', venuecode=venuecode))

	runner = Runner.query.filter_by(id=runnerid).first()
	course = Course.query.filter_by(venuecode=runner.venuecode, coursecode=runner.course).first()

	controls = [int(a) for a in str(course.controls).split(',')]

	#some input validation
	if (venuecode != runner.venuecode) or (course == None):
		print "SOMETHING HAS GONE WRONG"
		return redirect(url_for('venue', venuecode=venuecode))

	#evaluate control's validity for this runner
	if (control == controls[0]) and (runner.punch_on_course == None):
		#START case
		runner.punch = control
		runner.punch_on_course = control
		db.session.commit()

		nextcontrol = controls[1]
		message = "Just getting started? Good luck and have fun!"

	elif (control == controls[-1]) and (controls.index(runner.punch_on_course) == len(controls)-2):
		#FINISH case
		#to-do add a "finished" state to the db so re-loads don't mess up.

		runner.punch = control
		runner.punch_on_course = control
		runner.finished = True
		db.session.commit()

		nextcontrol = None
		message = 'Congrats, you finished!'

	elif runner.finished == True:
		#FINISHED case
		nextcontrol = None
		url = url_for('venue', venuecode=venuecode)
		message = 'You already finished. Go to ' + url + ' to try another course.'
		return 'You already finished. Go to ' + url + ' to try another course.'

	elif (controls.index(control)-1 == controls.index(runner.punch_on_course)):
		#on course case
		runner.punch = control
		runner.punch_on_course = control
		db.session.commit()

		nextcontrol = controls[controls.index(control)+1]
		message = 'Keep going!'

	else:
		#incorrect case
		runner.punch = control
		db.session.commit()

		nextcontrol = controls[controls.index(runner.punch_on_course)+1]
		message = "You're off course!"


	return render_template('controloncourse.html',
						venuename = course.venuefull,
						venuecode = course.venuecode,
						coursename = course.coursefull,
						course = str(course.coursecode),
						control = str(control),
						next = str(nextcontrol),
						message = message)


################################################
# Webapp Debug Routes
################################################

@app.route('/viewdb')
def show_runners():

	runners = Runner.query.all()
	if len(runners) == 0:
		return "oops, looks like the DB is empty."
	else:
		return render_template("showdbitems.html", items=runners)


@app.route('/viewcoursedb')
def show_courses():

	courses = Course.query.all()
	if len(courses) == 0:
		return "oops, looks like the DB is empty."
	else:
		return render_template("showdbitems.html", items=courses)



################################################
# Run the app
################################################

if __name__ == '__main__':
	app.run(debug=True)
