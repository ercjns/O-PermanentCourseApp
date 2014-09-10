/**************************************
insert known courses in the courses db

CREATE TABLE courses(
	id INTEGER primary key,
	venuecode TEXT not NULL,
	venue_fullname TEXT not NULL,
	course INTEGER not NULL,
	start INTEGER not NULL,
	controls TEXT not NULL,
	finish INTEGER not NULL,
	course_name TEXT not NULL,
	distance TEXT not NULL

);
**************************************/


-- Manguson Park --
-- --
INSERT INTO courses VALUES (
	11,
	'mag',
	'Magnuson Park',
	1,
	0,
	'0, 31, 32, 33, 34, 35, 36, 999',
	999,
	'Course 1',
	'1.4 km'
);

INSERT INTO courses VALUES (
	12,
	'mag',
	'Magnuson Park',
	2,
	0,
	'0, 42, 43, 33, 44, 45, 46, 40, 47, 41, 999',
	999,
	'Course 2',
	'1.7 km'
);

INSERT INTO courses VALUES (
	13,
	'mag',
	'Magnuson Park',
	3,
	0,
	'0, 36, 37, 38, 39, 40, 35, 41, 43, 32, 999',
	999,
	'Course 3',
	'2.8 km'
);

-- Not Magnuson Park --
-- --
INSERT INTO courses VALUES (
	21,
	'fts',
	'Ft. Steilacoom Park',
	1,
	0,
	'0, 36, 40, 37, 35, 32, 999',
	999,
	'Course 1',
	'1.8 km'
);
