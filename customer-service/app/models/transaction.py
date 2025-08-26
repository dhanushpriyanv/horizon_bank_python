# app/models/transaction.py
from app.db import db
from datetime import datetime

#### python working
# from sqlalchemy import Sequence

# class Transaction(db.Model):
#     __tablename__ = 'transaction'

#     id = db.Column(db.Integer, Sequence('transaction_seq'), primary_key=True)
#     amount = db.Column(db.Float, nullable=False)
#     sender_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
#     receiver_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     sender = db.relationship('Account', foreign_keys=[sender_account_id], backref='sent_transactions')
#     receiver = db.relationship('Account', foreign_keys=[receiver_account_id], backref='received_transactions')


from sqlalchemy.schema import Sequence

class Transaction(db.Model):
    __tablename__ = 'transactions'

    # id = db.Column(db.Integer, primary_key=True)
    id = db.Column(
        db.Integer,
        Sequence('transaction_seq'),  # 👈 Use the existing Oracle sequence
        primary_key=True
    )
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)

    from_customer = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    to_customer = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)

    # Relationships (if needed)
    account = db.relationship('Account', foreign_keys=[account_id])
    from_customer_ref = db.relationship('Customer', foreign_keys=[from_customer])
    to_customer_ref = db.relationship('Customer', foreign_keys=[to_customer])


