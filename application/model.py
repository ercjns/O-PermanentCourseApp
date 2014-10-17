from application import db

################################################
# Set up the databases, define database access functions
################################################

class Runner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	venuecode = db.Column(db.String(10))
	course = db.Column(db.Integer)
	punch = db.Column(db.Integer)
	punch_on_course = db.Column(db.Integer)
	punch_time = db.Column(db.DateTime)
	start_time = db.Column(db.DateTime)
	end_time = db.Column(db.DateTime)
	finished = db.Column(db.Boolean)

	def __init__(self, venuecode, course):
		self.venuecode = venuecode
		self.course = course
		self.finished = False

	def __repr__(self):
		try:
			return '<Runner %d, at %s on course %d, punch %d>' % (self.id, self.venuecode, self.course, self.punch)
		except:
			return '<Runner %d, at %s>' % (self.id, self.venuecode)
		

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
		return '<Course %i, %s (%i) at %s>' % (self.id, self.coursefull, self.coursecode, self.venuefull)


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
