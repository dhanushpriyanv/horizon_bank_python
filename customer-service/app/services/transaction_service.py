from app.db import transaction_repo, account_repo
from app.models.transaction import Transaction
from app.models.account import Account
from app.db import db
from datetime import datetime
from sqlalchemy import text
from app.decorators.transactional_decorator import transactional
from app.exceptions.exceptions import AccountNotFoundException, InsufficientFundsException
from app.db import customer_repo
### working python
# @transactional
# def send_money(data):
#     from_customer_id = data['fromCustomerId']
#     to_customer_id = data['toCustomerId']
#     amount = data['amount']

#     # Get sender and receiver accounts
#     sender_account = db.session.query(Account).filter_by(customer_id=from_customer_id).first()
#     receiver_account = db.session.query(Account).filter_by(customer_id=to_customer_id).first()

#     if not sender_account:
#         raise AccountNotFoundException("Sender account not found")
#     if not receiver_account:
#         raise AccountNotFoundException("Receiver account not found")
#     if sender_account.balance < amount:
#         raise InsufficientFundsException("Insufficient funds")

#     # Perform balance transfer
#     sender_account.balance -= amount
#     receiver_account.balance += amount

#     #### working python
#     transaction = Transaction(
#         sender_account_id=sender_account.id,
#         receiver_account_id=receiver_account.id,
#         amount=amount,
#         timestamp=datetime.utcnow()
#     )

#     db.session.add(transaction)
    
#     db.session.flush()  # Optional but ensures `transaction.id` is set

#     # ✅ Attach customers for frontend
#     transaction.fromCustomer = transaction.sender.customer
#     transaction.toCustomer = transaction.receiver.customer
#     return transaction

@transactional
def send_money(data):
    from_customer_id = data['fromCustomerId']
    to_customer_id = data['toCustomerId']
    amount = data['amount']

    sender = account_repo.get_account_by_customer_id(from_customer_id)
    receiver = account_repo.get_account_by_customer_id(to_customer_id)

    if not sender:
        raise AccountNotFoundException("Sender account not found")
    if not receiver:
        raise AccountNotFoundException("Receiver account not found")
    if sender.balance < amount:
        raise InsufficientFundsException("Insufficient funds")

    # Update balances
    sender.balance -= amount
    receiver.balance += amount

    # Create DEBIT transaction (money deducted from sender)
    debit_tx = Transaction(
        account_id=sender.id,
        from_customer=sender.customer_id,
        to_customer=receiver.customer_id,
        amount=-abs(amount),
        timestamp=datetime.utcnow(),
        type="DEBIT"
    )
    db.session.add(debit_tx)

    # Create CREDIT transaction (money added to receiver)
    credit_tx = Transaction(
        account_id=receiver.id,
        from_customer=sender.customer_id,
        to_customer=receiver.customer_id,
        amount=abs(amount),
        timestamp=datetime.utcnow(),
        type="CREDIT"
    )
    db.session.add(credit_tx)

    return credit_tx  # return the CREDIT as confirmation


def get_transaction_by_id(id):
    return transaction_repo.get_transaction_by_id(id)


def get_all_transactions():
    return transaction_repo.get_all_transactions()

def get_transactions_by_customer_id(customer_id):
    transactions = (
        db.session.query(Transaction)
        #.join(Account, (Transaction.sender_account_id == Account.id) | (Transaction.receiver_account_id == Account.id))
        #.join(Account, Transaction.account_id == Account.id).filter(Account.customer_id == customer_id)
        .join(Account, Transaction.account_id == Account.id)
        .filter(Account.customer_id == customer_id)
        .order_by(Transaction.timestamp.desc())
        .all()
    )


    for tx in transactions:
        tx.fromCustomer = tx.from_customer_ref  # ✅ VALID
        tx.toCustomer = tx.to_customer_ref

    return transactions

@transactional
def pay_bill_service(customerId, billType, accountNumber, amount):
    customer = customer_repo.get_customer_by_id(customerId)
    if not customer:
        raise AccountNotFoundException("Customer not found")

    account = account_repo.get_account_by_customer_id(customerId)
    if not account:
        raise AccountNotFoundException("Account not found")

    if account.balance < amount:
        raise InsufficientFundsException("Insufficient funds")

    account.balance -= amount
    db.session.add(account)

    tx = Transaction(
        from_customer=customer.id,
        to_customer=customer.id,
        amount=-abs(amount),
        timestamp=datetime.utcnow(),
        account_id=account.id,
        type=f"BILL_PAY_{billType.upper()}"
    )
    db.session.add(tx)
    return tx


# Stored Procedure Integration

# from app.db.procedure_caller import call_procedure

# def transfer_money_by_plsql(from_customer_id, to_customer_id, amount):
#     call_procedure("TRANSFER_MONEY", {'from_id': from_customer_id, 'to_id': to_customer_id, 'amt': amount})

# def pay_bill_by_plsql(customer_id, bill_type, account_number, amount):
#     call_procedure("PAY_BILL", {'cust_id': customer_id, 'bill_type': bill_type, 'acc_no': account_number, 'amt': amount})

# def add_money_by_plsql(customer_id, amount):
#     call_procedure("ADD_MONEY", {'cust_id': customer_id, 'amt': amount})

# from app.models import Customer, Account, Transaction
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.models.account import Account
from app.db import db
from app.db import procedure_caller

def send_money_by_plsql(from_customer_id, to_customer_id, amount):
    print(f"[PLSQL] Transferring money from {from_customer_id} to {to_customer_id} amount {amount}")
    procedure_caller.call_transfer_money_procedure(from_customer_id, to_customer_id, amount)

    # sender = db.session.query(Customer).filter_by(id=from_customer_id).first()
    # if not sender or not sender.account:
    #     raise ValueError("Sender account not found")

    # account_id = sender.account.id
    sender = db.session.query(Customer).filter_by(id=from_customer_id).first()
    account = db.session.query(Account).filter_by(customer_id=from_customer_id).first()

    if not sender or not account:
        raise ValueError("Sender account not found")

    account_id = account.id

    return (
        db.session.query(Transaction)
        .filter(Transaction.account_id == account_id)
        .order_by(Transaction.timestamp.desc())
        .first()
    )

def pay_bill_by_plsql(customer_id, bill_type, account_number, amount):
    print(f"[PLSQL] Paying bill for customer {customer_id}, type {bill_type}, account {account_number}, amount {amount}")
    procedure_caller.call_pay_bill_procedure(customer_id, bill_type, account_number, amount)

    # customer = db.session.query(Customer).filter_by(id=customer_id).first()
    # if not customer or not customer.account:
    #     raise ValueError("Customer account not found")

    # account_id = customer.account.id
    customer = db.session.query(Customer).filter_by(id=customer_id).first()
    account = db.session.query(Account).filter_by(customer_id=customer_id).first()
    if not customer or not account:
        raise ValueError("Customer account not found")
    account_id = account.id

    return (
        db.session.query(Transaction)
        .filter(Transaction.account_id == account_id)
        .order_by(Transaction.timestamp.desc())
        .first()
    )

def add_money_by_plsql(customer_id, amount):
    print(f"[PLSQL] Adding money to customer {customer_id} amount {amount}")
    procedure_caller.call_add_money_procedure(customer_id, amount)

    # customer = db.session.query(Customer).filter_by(id=customer_id).first()
    # if not customer or not customer.account:
    #     raise ValueError("Customer account not found")

    # account_id = customer.account.id
    customer = db.session.query(Customer).filter_by(id=customer_id).first()
    account = db.session.query(Account).filter_by(customer_id=customer_id).first()

    if not customer or not account:
        raise ValueError("Customer account not found")

    account_id = account.id

    return (
        db.session.query(Transaction)
        .filter(Transaction.account_id == account_id)
        .order_by(Transaction.timestamp.desc())
        .first()
    )