from app import db
from datetime import datetime

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable = False)
    email = db.Column(db.String(80), unique=True, nullable = False)
    password = db.Column(db.String(80), unique=False, nullable = False)
    budget = db.relationship('Budget', backref='author', lazy=True)

    def asDict(self):
        return {
            'id': self.id,
            'username' : self.username,
            'email': self.email,
            'password': self.password
        }

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movements  = db.relationship('Movement', backref='budget', lazy=True)

    def asDict(self):
        return { 'id' : self.id,
                 'name' : self.name,
                 'amount': self.amount
                }

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=0)
    date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    entry = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    id_budget = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    
    def asDict(self):
        return { 'id' : self.id,
                'amount' : self.amount,
                'date' : self.date,
                'entry' : self.entry,
                'description': self.description
                }