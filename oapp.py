#TODO
# update db schema to keep track of all control visits
# update db to know last known on-course control
# implement second table for storing course definitions
	# load maps correctly
	# do lots of other magic / logic

#commands:
#go to directory
# setting a path for my orienteering app settings to be loaded from
# OAPP_TEST_SETTINGS='/home/eric/code/oapp/config.ini'
#start the viretual envrionment (. venv/bin/activate)
#python prompt from oapp import init_db
#init_db()
#quit python, run the app



# imports
import sqlite3
from contextlib import closing
from flask import Flask, render_template, url_for, redirect, g, session

#create the application

app =  Flask(__name__)
app.config.from_envvar('OAPP_TEST_SETTINGS', silent=True)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def update_course_db():
	with closing(connect_db()) as db:
		with app.open_resource('courses.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

def make_dicts(cursor, row):
	return dict((cursor.description[idx][0], value)
				for idx, value in enumerate(row))

def get_db():
	db = getattr(g, 'db', None)
	if db is None:
		db = g.db = connect_db()
	db.row_factory = make_dicts
	return db

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	if one:
		rv = cur.fetchone()
	else:
		rv = cur.fetchall()
	cur.close()
	return rv

def dbstr_to_str(dbstr):
	pass

@app.route('/viewdb')
def show_runners():
	runners = query_db('SELECT * FROM runners')
	if len(runners) == 0:
		return "oops, looks like the DB is empty."
	else:
		rows = [d.values() for d in runners]
		head = d.keys()
		return render_template("showdbitems.html", rows=rows, head=head)


@app.route('/')
def index():
	'''page should display general information about what courses are avaiable'''
	print "INDEX FUNCTION"
	locs = query_db('SELECT venuecode, venue_fullname FROM courses')
	venues = []
	for d in locs:
		venues.append((d['venuecode'], d['venue_fullname']))
	venues = list(set(venues))
	return render_template("index.html", venues=venues)


@app.route('/<venuecode>')
def venue(venuecode):
	'''look up the code in the db, get the name + courses, display it
	if the code is not valid, redirect to a landing page'''
	print "VENUE FUNCTION"
	#to-do: get the courses here, not all have three
	courses = query_db('SELECT venuecode, venue_fullname, course, course_name, distance FROM courses WHERE venuecode = ?', [venuecode])
	if courses is None:
		#should probably error here, but for now redirect
		return redirect(url_for('index'))

	print courses

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
	#add a row to the runners table
	sql  = 'INSERT INTO runners '
	sql += '(venuecode, course, finished) '
	sql += 'VALUES (?, ?, ?)'
	sqlvals = [venuecode, course, 0]

	c = get_db().cursor()
	c.execute(sql, sqlvals)
	get_db().commit()
	#create a session with the id
	session['runnerID'] = c.lastrowid
	#redirect to the first control
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

	runner = query_db("SELECT * FROM runners WHERE id = ?", [runnerid], True)
	course = query_db("SELECT * FROM courses WHERE venuecode=? AND course=?",
					  [runner['venuecode'], runner['course']], True)
	controls = [int(a.strip(',')) for a in str(course['controls']).split()]

	if (control == controls[0]) and (runner['punch_on_course'] == None):
		#START case
		query_db('UPDATE runners SET punch=?, punch_on_course=? WHERE id=?',
				[control, control, runner['id']])
		get_db().commit()
		nextcontrol = controls[1]
		message = "Just getting started? Good luck and have fun!"

	elif (control == controls[-1]) and (controls.index(runner['punch_on_course']) == len(controls)-2):
		#FINISH case
		#to-do add a "finished" state to the db so re-loads don't mess up.
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
		query_db('UPDATE runners SET punch=?, punch_on_course=? WHERE id=?',
				[control, control, runner['id']])
		get_db().commit()
		nextcontrol = controls[controls.index(control)+1]
		message = 'Keep going!'

	else:
		#incorrect case
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

if __name__ == '__main__':
	app.run(debug=True)
