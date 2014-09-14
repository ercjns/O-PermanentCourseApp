################################################
# Permanent Orienteering Course WebApp
#
#    (c) 2014 Eric Jones
#    Licensed under the MIT License
#    https://github.com/ercjns/o-webapp
################################################


#Switching to PostgreSQL for deployment on heroku dev.


# imports
import os
from flask.ext.sqlalchemy import SQLAlchemy
from contextlib import closing
from flask import Flask, render_template, url_for, redirect, g, session


################################################
# Create the Flask application, connect to the db
################################################

app =  Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URL'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:////tmp/test.db'
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
	finished = db.Column(db.Integer)

	def __init__(self, venuecode, course):
		self.venuecode = venuecode
		self.course = course

	def __repr__(self):
		return '<Runner at %s on course %d>' % self.venuecode, self.course

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
	finish = db.Columb(db.Integer)

	def __init__(self, venuecode, venuefull, coursecode, coursefull,
				distance, climb, start, controls, finish):
		self.venuecode = venuecode
		self.venuefull = venuefull
		self.coursecode = cousecode
		self.coursefull = coursefull
		self.distance = distance
		self.climb = climb
		self.start = start
		self.controls = controls
		self.finish = finish

	def __repr__(self):
		return '<course %i at %s>' % self.coursecode, self.venuefull


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
	print "INDEX FUNCTION"
	### CONVERT THIS DB CALL
	locs = query_db('SELECT venuecode, venue_fullname FROM courses')
	venues = []
	for d in locs:
		venues.append((d['venuecode'], d['venue_fullname']))
	venues = list(set(venues))

	return render_template("index.html",
							venues=venues)


@app.route('/<venuecode>')
def venue(venuecode):
	'''look up the code in the db, get the name + courses, display it
	if the code is not valid, redirect to a landing page'''

	### CONVERT THIS DB CALL
	courses = query_db('SELECT venuecode, venue_fullname, course, course_name, distance FROM courses WHERE venuecode = ?', [venuecode])
	if len(courses) == 0:
		#should probably error here, but for now redirect
		return redirect(url_for('index'))
	venuename = str(courses[0]['venue_fullname'])
	venuecode = str(courses[0]['venuecode'])

	return render_template('venuehome.html',
							venuecode=venuecode,
							venuename=venuename,
							courses = courses)


@app.route('/<venuecode>/start/<int:course>')
def init_course(venuecode, course):
	''' to start a coruse, add a row to the runners table,
	set a session on the client, and re-direct to the proper control page'''

	#to-do VALIDATE that venue and course are valid values!!!

	### CONVERT THIS DB CALL
	sql  = 'INSERT INTO runners '
	sql += '(venuecode, course, finished) '
	sql += 'VALUES (?, ?, ?)'
	sqlvals = [venuecode, course, 0]

	### CONVERT THIS DB CALL
	c = get_db().cursor()
	c.execute(sql, sqlvals)
	get_db().commit()

	### CONVERT THIS DB CALL
	session['runnerID'] = c.lastrowid

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

	### CONVERT THIS DB CALL
	runner = query_db("SELECT * FROM runners WHERE id = ?", [runnerid], True)
	### CONVERT THIS DB CALL
	course = query_db("SELECT * FROM courses WHERE venuecode=? AND course=?",
					  [runner['venuecode'], runner['course']], True)
	controls = [int(a.strip(',')) for a in str(course['controls']).split()]

	#some input validation
	if (venuecode != runner['venuecode']) or (len(course) == 0)
		print "SOMETHING HAS GONE WRONG"
		return redirect(url_for('venue', venuecode=venuecode))

	#evaluate control's validity for this runner
	if (control == controls[0]) and (runner['punch_on_course'] == None):
		#START case
		### CONVERT THIS DB CALL
		query_db('UPDATE runners SET punch=?, punch_on_course=? WHERE id=?',
				[control, control, runner['id']])
		get_db().commit()
		nextcontrol = controls[1]
		message = "Just getting started? Good luck and have fun!"

	elif (control == controls[-1]) and (controls.index(runner['punch_on_course']) == len(controls)-2):
		#FINISH case
		#to-do add a "finished" state to the db so re-loads don't mess up.
		### CONVERT THIS DB CALL
		query_db('UPDATE runners SET punch=?, punch_on_course=?, finished=? WHERE id=?',
				[control, control, 1, runner['id']])
		get_db().commit()
		nextcontrol = None
		message = 'Congrats, you finished!'

	elif runner['finished'] == 1:
		#FINISHED case
		nextcontrol = None
		url = url_for('venue', venuecode=venuecode)
		message = 'You already finished. Go to ' + url + ' to try another course.'
		return 'You already finished. Go to ' + url + ' to try another course.'

	elif (controls.index(control)-1 == controls.index(runner['punch_on_course'])):
		#on course case
		### CONVERT THIS DB CALL
		query_db('UPDATE runners SET punch=?, punch_on_course=? WHERE id=?',
				[control, control, runner['id']])
		get_db().commit()
		nextcontrol = controls[controls.index(control)+1]
		message = 'Keep going!'

	else:
		#incorrect case
		### CONVERT THIS DB CALL
		query_db('UPDATE runners SET punch=? WHERE id=?', [control, runner['id']])
		get_db().commit()
		nextcontrol = controls[controls.index(runner['punch_on_course'])+1]
		message = "You're off course!"


	return render_template('controloncourse.html',
						venuename = str(course['venue_fullname']),
						venuecode = course['venuecode'],
						coursename = str(course['course_name']),
						course = str(course['course']),
						control = str(control),
						next = str(nextcontrol),
						message = message)


################################################
# Webapp Debug Routes
################################################

@app.route('/viewdb')
def show_runners():
	### CONVERT THIS DB CALL
	runners = query_db('SELECT * FROM runners')
	if len(runners) == 0:
		return "oops, looks like the DB is empty."
	else:
		rows = [d.values() for d in runners]
		head = d.keys()
		return render_template("showdbitems.html", rows=rows, head=head)



################################################
# Run the app
################################################

if __name__ == '__main__':
	app.run(debug=True)
