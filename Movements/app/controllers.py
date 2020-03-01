from flask import request, jsonify
from flask_restplus import Resource, fields
from app import db, api, app
from app.models import Movement, Budget
import traceback
from datetime import datetime

movements = api.namespace('api/v1.0/movements', description ='CRUD operation for movements')

budgetModel = movements.model('budgetModel', {
    'name' : fields.String(required=True, validate=True)
    }
)

movementModel = movements.model('movementModel', {
    'amount' : fields.Float(required=True, validate=True),
    'date' : fields.DateTime(required=False, validate=True),
    'entry' : fields.Boolean(required=True, validate=True),
    'description' : fields.String(required=False, validate=True)
    }
)

resp = {200: 'Success', 400: 'movement already in db', 400: 'Content not allowed', \
    400: 'Payload too large', 500: 'Server Error'}


@movements.route('/<int:id_user>')
class Budget_Requests(Resource):
    @movements.expect(budgetModel)
    def post(self,id_user):
        """Post a user budget"""
        data = request.get_json()
        budget = Budget(id_user=id_user, name=data.get('name'))
        db.session.add(budget)
        db.session.commit()
        return jsonify(budget.asDict())

    def get(self,id_user):
            '''Get all budgets of one user'''
            budgets = Budget.query.filter_by(id_user=id_user).all()
            j = {}
            j['data'] = []
            j['metadata'] = {}
            j['metadata']['n_results'] = Budget.query.filter_by(id_user=id_user).count()
            j['metadata']['n_page'] = 1

            for budget in budgets:
                j['data'].append(budget.asDict())
            return jsonify(j)    

    
 

@movements.route('/<int:id_user>/<int:id_budget>')
class Movement_Requests(Resource):
    @movements.expect(movementModel)
    def post(self,id_user,id_budget):
        '''Post a movement'''
        budget = Budget.query.get(id_budget)
        if not budget:
            return 'budget not found', 404
        if id_user != budget.id_user:
            return 'not allow', 406
        data = request.get_json()
        amount = data.get('amount') 
        date = data.get('date')
        entry = data.get('entry')
        description =  data.get('description')
        date = datetime.strptime(date, '%d/%m/%Y')
        movement = Movement(id_budget=id_budget, amount=amount, 
            date=date, entry=entry, description=description)
        if entry:
            budget.amount += amount
        else:
            budget.amount -= amount
        db.session.add(movement)
        db.session.commit()
        return jsonify(movement.asDict())

    def get(self,id_user,id_budget):
        '''view movements of one budget'''
        budget = Budget.query.get(id_budget)
        if not budget:
            return 'budget not found', 404
        response={budget.amount : []}
        print(budget.movements[0].asDict())
        for movement in budget.movements:
            response[budget.amount]+= [movement.id, movement.amount, movement.date, movement.entry, movement.description]
            print(movement.asDict())
        return jsonify(response)

    
    @movements.expect(budgetModel)
    def put(self,id_budget,id_user):
        '''Mod a User budget'''
        try:
            data = request.get_json()
            budget_name_request = data.get("name")
            

            #checking if user exists
            u = Budget.query.filter_by(id_user=id_user ,id = id_budget ).first()
            if(u is None):
                return 'user not in DB', 404
            u.name = budget_name_request if budget_name_request else u.name
            # u.name = budget_name_request
            
            db.session.commit()
            return jsonify(u.asDict())
        except:
            
            return 'Error server side', 500    



    def delete(self,id_user,id_budget):
        '''delete a budget '''
        try:
            u = Budget.query.filter_by(id_user=id_user,id =id_budget).first()
            if (u is None):
                return 'Budget not found', 404
            db.session.delete(u)
            db.session.commit()
            return  204
        except:
            return 'Error server side', 500

@movements.route('/<int:id_user>/<int:id_budget>/<int:id_movement>')
class Movement_Put(Resource):
    @movements.expect(movementModel)
    def put(self,id_movement,id_budget,id_user):
        '''Mod a Budget Movement'''
        try:
            budget = Budget.query.get(id_budget)
            if not budget:
                return 'budget not found', 404
            if id_user != budget.id_user:
                return 'not allow', 406
            data = request.get_json()
            amount_request = data.get("amount")
            entry_request = data.get("entry")
            description_request =  data.get('description')
            date_request= data.get('date')
            date_request = datetime.strptime(date_request, '%d/%m/%Y')
            

            #checking if user exists
            u = Movement.query.filter_by(id_budget=id_budget,id = id_movement).first()
            if(u is None):
                return 'movement not in DB', 404
            u.amount = amount_request if amount_request else u.amount
            u.entry = entry_request if entry_request else u.entry
            u.date = date_request if date_request else u.date
            u.description =description_request if description_request else u.description
            
            db.session.commit()
            return jsonify(u.asDict())
        except:
            return 'Error server side', 500  

    def delete(self,id_user,id_budget,id_movement):
        '''delete a movement '''
        try:
            
            budget = Budget.query.get(id_budget)
            if not budget:
                return 'budget not found', 404
            if id_user != budget.id_user:
                return 'not allow', 406
            u = Movement.query.filter_by(id_budget=id_budget,id = id_movement).first()
            if (u is None):
                return 'Budget not found', 404

            
            if(u is None):
                return 'movement not in DB', 404
            
            db.session.delete(u)
            db.session.commit()
            return  204
        
        except:
            return 'Error server side', 500
