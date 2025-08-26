# app/db/account_repo.py
from app.models.account import Account
from app.db import db

def get_all_accounts():
    return Account.query.all()

# def get_account_by_id(account_id):
#     return Account.query.get(account_id)

def create_account(account):
    db.session.add(account)
    db.session.commit()
    return account

def delete_account(account):
    db.session.delete(account)
    db.session.commit()

def get_account_by_customer_id(customer_id):
    return Account.query.filter_by(customer_id=customer_id).first()


def get_account_by_id(account_id):
    return Account.query.filter_by(id=account_id).first()

def get_account_by_username(username):
    return Account.query.filter_by(account_number=username).first()