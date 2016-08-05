from os.path import abspath, dirname

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config.dev import DevelopmentConfig
from config.test import TestConfig

app = Flask('CaloriesCounter', template_folder='templates', static_folder='static')

app.config.from_object(DevelopmentConfig)
#app.config.from_envvar('production_var')

db = SQLAlchemy(app)

app.root_path = abspath(dirname(__file__))
