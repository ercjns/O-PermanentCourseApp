/**************************************
insert known courses in the courses db

CREATE TABLE courses(
	id INTEGER primary key,
	venuecode TEXT not NULL,
	venue_fullname TEXT not NULL,
	course INTEGER not NULL,
	start INTEGER not NULL,
	controls TEXT not NULL,
	finish INTEGER not NULL
);
**************************************/


-- Manguson Park --
-- this is fake for testing --
INSERT INTO courses VALUES (
	11,
	'mag',
	'Magnuson Park',
	1,
	101,
	'101, 102, 103, 104, 105, 106',
	106
);

INSERT INTO courses VALUES (
	12,
	'mag',
	'Magnuson Park',
	2,
	101,
	'101, 105, 107, 108, 106',
	106
);

INSERT INTO courses VALUES (
	13,
	'mag',
	'Magnuson Park',
	3,
	101,
	'101, 111, 115, 114, 113, 104, 102, 117, 126, 106',
	106
);
