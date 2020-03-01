from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app,
       version='0.1',
       title='Api Bilacio Personale Movements',
       description='api Bilancio personale gestione Controllers movimenti',
       endpoint='api')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../site.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.controllers import movements

api.add_namespace(movements)