DROP TABLE if exists runners;
CREATE TABLE runners(
  id INTEGER primary key autoincrement,
  venuecode TEXT not NULL,
  course INTEGER not NULL,
  punch INTEGER,
  punch_on_course INTEGER,
  punch_time TEXT,
  start_time TEXT,
  end_time TEXT,
  finished INTEGER
);
DROP TABLE if exists courses;
CREATE TABLE courses(
    id INTEGER primary key autoincrement,
    venuecode TEXT not NULL,
    venue_fullname TEXT not NULL,
    course INTEGER not NULL,
    start INTEGER not NULL,
    controls BLOB not NULL,
    finish INTEGER not NULL,
    course_name TEXT not NULL,
    distance TEXT not NULL
);
