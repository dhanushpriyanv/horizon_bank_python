# app/models/customer.py
from app.db import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    #email = db.Column(db.String(120), nullable=False)


    # accounts = db.relationship('Account', backref='customer', cascade='all, delete-orphan')
