from flask import request, jsonify
from flask_restplus import Resource, fields
from app import db, api, app
from app.models import User
import traceback

users = api.namespace('api/v1.0/users', description ='CRUD operation for users')

userModel = users.model('userModel', {
    'username' : fields.String(required=True, validate=True),
    'email' : fields.String(required=True, validate=True),
    'password' : fields.String(required=True, validate=True)
    }
)

resp = {200: 'Success', 400: 'user already in db', 400: 'Content not allowed', \
    400: 'Payload too large', 500: 'Server Error'}


@users.route('')
class Users(Resource):
    def get(self):
        '''get all users'''
        users = User.query.all()
        j = {}
        j['data'] = []
        j['metadata'] = {}
        j['metadata']['n_results'] = User.query.count()
        j['metadata']['n_page'] = 1

        for user in users:
            j['data'].append(user.asDict())
        return jsonify(j)

    @users.expect(userModel, validate=True)
    @users.doc(responses=resp)
    def post(self):
        '''create a new user'''
        #create a new record in the DB
        try:
            data = request.get_json()
            username_request = data.get("username")
            email_request = data.get("email")
            password_request = data.get("password")

            #checking if user exists
            if(User.query.filter( (User.username==username_request) | (User.email==email_request)).count() > 0):
                return 'user already in DB', 400

            u = User(username=username_request, email=email_request, password=password_request)
            db.session.add(u)
            db.session.commit()
            return jsonify(u.asDict())
        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500


    


@users.route('/<int:user_id>')
class UsersId(Resource):
    @users.expect(validate=True)
    @users.doc(responses=resp)
    def get(self, user_id):
        '''gets a user by id'''
        try:
            u = User.query.filter_by(id = user_id).first()
            if not u:
                return 'User not found', 404
            return  jsonify(u.asDict())
        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500

    @users.expect(validate=True)
    @users.doc(responses=resp)
    def delete(self, user_id):
        '''deletes a user '''
        try:
            u = User.query.filter_by(id = user_id).first()
            if (u is None):
                return 'User not found', 404
            db.session.delete(u)
            db.session.commit()
            return  204
        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500

    @users.expect(userModel, validate=True)
    @users.doc(responses=resp)
    def put(self, user_id):
        '''update user'''
        try:
            data = request.get_json()
            username_request = data.get("username")
            email_request = data.get("email")
            password_request = data.get("password")
            #checking if user exists
            u = User.query.get(user_id)
            if not u:
                return 'user not in DB', 404
            u.username = username_request if username_request else u.username
            u.email = email_request if email_request else u.email
            u.password = password_request if password_request else u.password
            db.session.commit()
            return jsonify(u.asDict())
        except:
            app.logger.error(traceback.format_exc())
            return 'Error server side', 500
