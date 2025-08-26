# app/db/transaction_repo.py
from app.models.transaction import Transaction
from app.db import db
from app.models.account import Account

def get_all_transactions():
    return Transaction.query.all()

def get_transaction_by_id(transaction_id):
    return Transaction.query.get(transaction_id)

def create_transaction(transaction):
    db.session.add(transaction)
    db.session.commit()
    return transaction

def delete_transaction(transaction):
    db.session.delete(transaction)
    db.session.commit()

def get_transactions_by_customer_id(customer_id):
    return Transaction.query.join(Account, Transaction.sender_account_id == Account.id == Account.id == Account.id).filter(Account.customer_id == customer_id).all()