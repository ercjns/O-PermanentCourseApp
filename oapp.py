#TODO
# update db schema to keep track of all control visits
# update db to know last known on-course control
# implement second table for storing course definitions
	# load maps correctly
	# do lots of other magic / logic

#commands:
#go to directory
#start the viretual envrionment (. /venv/bin/activate)
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

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

def get_db():
	db = getattr(g, 'db', None)
	if db is None:
		db = g.db = connect_db()
	return db

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

@app.route('/viewdb')
def show_runners():
	runners = query_db('SELECT id, venue, course, last_known FROM runners ORDER BY id DESC')
	if runners is None:
		return "not found"
	else:
		return render_template("showdbitems.html", rv=runners)


@app.route('/')
def index():
	return 'Index Page'

@app.route('/<venue>/<int:control>/')
def visit_control(venue, control):

	runnerid = session['runnerID']
	if runnerid == None:
		print "No session, re-directing"
		return redirect(url_for('start', venue=venue))

	runner = query_db("SELECT * FROM runners WHERE id = ?", [runnerid], True)

	cur = get_db().cursor()
	cur.execute('UPDATE runners SET last_known=? WHERE id = ?', [control, runnerid])
	get_db().commit()

	#get the course the user is on from DB
	#get the previous control from DB
	#compute if the control is correct
		#correct - show the next map
		#incorrect - show a message, show the same map
	return render_template('controloncourse.html',
						   venue = venue,
						   course = "hard-coded",
						   control = str(control),
						   next = '102')

@app.route('/<venue>/')
def start(venue):
	return render_template('venuehome.html',
						   venue = venue
						   )

@app.route('/<venue>/start/<course>')
def init_course(venue, course):
	#add a row to the runners table
	cur = get_db().cursor()
	cur.execute('INSERT INTO runners (venue, course, last_known) VALUES (?, ?, ?)', ['Mag', course, 101])
	userkey = cur.lastrowid
	get_db().commit()

	#create a session with the id
	session['runnerID'] = userkey

	return redirect(url_for('visit_control', venue=venue, control=101))


if __name__ == '__main__':
	app.run(debug=True)
