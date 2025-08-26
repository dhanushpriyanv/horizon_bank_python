# app/models/account.py
from app.db import db

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float, nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customer', backref='accounts')

sent_transactions = db.relationship(
    'Transaction',
    foreign_keys='Transaction.sender_id',
    back_populates='sender'
)

received_transactions = db.relationship(
    'Transaction',
    foreign_keys='Transaction.receiver_id',
    back_populates='receiver'
)

    
