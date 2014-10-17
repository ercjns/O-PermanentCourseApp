Orienteering Web App for Permanent Courses
==========================================

The goal of this app is to be a mobile browser based app for exploring orienteering in parks were permanent orienteering courses are installed. Permanent courses typically include posts with the control code and a letter painted or carved on them. In the app, progress will be recorded by oreinteers visiting a simple url (by typing or scanning a qr code with a mobile device) on each control post. The initial development of this is app is based on maps provided by Cascade Orienteering Club in Seattle, WA, USA.

Features
--------
* Enumerate Venues and Courses from db table
* Initialize a course
* Indicate if the visited control is on course or not
* Show a map to the next control from previous control (in progress)
* Finish a course
* Show map of the full venue
* Report the time taken to complete course

To Do
-----
* Migrate to using secret codes rather than control numbers.
* error handling and data validation
* record every control visited in db
* testing on small devices - make maps look great
* debug device qr code scanning and sessions
* integrate with the device compass?
* integrate with the device GPS? (for help mode or navigate to start)
* support more courses
* show data from previous orienteers


Architecture
------------
This project uses the [Flask](http://flask.pocoo.org/) python framework. It is deployed and running on Heroku, with a database in Heroku's PosgreSQL db.


Notes To Myself
---------------
To run locally:
 1. set the environment variable FLASK_ENV='DEVELOPMENT'
 2. foreman start OR python run.py
 3. visit http://127.0.0.1:5000/


Mumbo-Jumbo
-----------
Work in this repository is licensed under the [MIT License](http://mit-license.org/)
