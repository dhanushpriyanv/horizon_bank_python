# app/services/account_service.py
from app.db import account_repo, customer_repo
from app.models.account import Account
from app.exceptions.errors import AccountNotFoundException
from app.db import account_repo
from app.db import db

def create_account(data):
    customer = customer_repo.get_customer_by_id(data['customer_id'])
    if not customer:
        raise ValueError("Customer not found")

    account = Account(
        account_number=data['account_number'],
        balance=data['balance'],
        customer_id=customer.id
    )
    return account_repo.create_account(account)

# def get_account_by_id(account_id):
#     return account_repo.get_account_by_id(account_id)
def get_account_by_id(account_id):
    account = account_repo.get_account_by_id(account_id)
    if not account:
        raise AccountNotFoundException()
    return account

def get_all_accounts():
    return account_repo.get_all_accounts()

def delete_account(account_id):
    account = account_repo.get_account_by_id(account_id)
    if account:
        account_repo.delete_account(account)
        return "Account deleted successfully"
    return "Account not found"

def get_account_by_customer_id(customer_id):
    return account_repo.get_account_by_customer_id(customer_id)


def get_account_by_username(username):
    return account_repo.get_account_by_username(username)

def get_account_balance(account_id):
    account = account_repo.get_account_by_id(account_id)
    return account.balance if account else None


def deposit_to_account(customer_id, amount):
    account = account_repo.get_account_by_customer_id(customer_id)
    if not account:
        raise AccountNotFoundException(f"Account for customer {customer_id} not found")
    account.balance += amount
    db.session.commit()
    return account


def withdraw_from_account(account_id, amount):
    account = account_repo.get_account_by_id(account_id)
    if not account:
        return None  # Not found
    if account.balance < float(amount):
        return False  # Insufficient funds
    account.balance -= float(amount)
    db.session.commit()
    return True
