################################################
# Permanent Orienteering Course WebApp
#
#    (c) 2014 Eric Jones
#    Licensed under the MIT License
#    https://github.com/ercjns/o-webapp
################################################

import os


try:
	dburl = os.environ['DATABASE_URL']
except:
	basedir = os.path.abspath(os.path.dirname(__file__))
	dburl = 'sqlite:///' + os.path.join(basedir, 'app.db')

#need to figure out if there's a better way around the database URL key error
#implemented this way because localhost env (dev) doesn't have this key
#and it would throw an error at import/runtime

class Config(object):
	DEBUG = False
	TESTING = False
	PERMANENT_SESSION_LIFETIME = 24*60*60
	SECRET_KEY = 'Tiny Development Key'
	SQLALCHEMY_DATABASE_URI = dburl

class DevelopmentConfig(Config):
	DEBUG = True

class ProductionConfig(Config):
	SECRET_KEY = 'CHANGE THIS KEY BEFORE YOU DEPLOY'
