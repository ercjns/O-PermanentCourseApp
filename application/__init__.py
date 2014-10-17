from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
import configurations

app = Flask(__name__)

app.config.from_object(configurations.Config)
if os.environ['FLASK_ENV'] == 'PRODUCTION':
	app.config.from_object(configurations.ProductionConfig)
elif os.environ['FLASK_ENV'] == 'DEVELOPMENT':
	app.config.from_object(configurations.DevelopmentConfig)

db = SQLAlchemy(app)

import application.views
