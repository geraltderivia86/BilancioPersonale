from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app,
       version='0.1',
       title='Api Users Bilancio Personale',
       description='api Bilancio personale',
       endpoint='api')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../site.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

db.create_all()

from app.controllers import users

api.add_namespace(users)