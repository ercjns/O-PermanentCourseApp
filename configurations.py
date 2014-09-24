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
	dburl = 'postgresql://postgres:postgresPW!@localhost/postgres'

#need to figure out if there's a better way around the database URL key error
#implemented this way because localhost env (dev) doesn't have this key
#and it would throw an error at import/runtime
#not sure if it makes sense to add that env variable to the local machine

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
