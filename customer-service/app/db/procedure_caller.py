from sqlalchemy.sql import text
from app.db import db

def call_procedure(name, params):
    placeholders = ', '.join(f":{k}" for k in params)
    sql = text(f"CALL {name}({placeholders})")
    db.session.execute(sql, params)
    db.session.commit()


def call_pay_bill_procedure(customer_id, bill_type, account_number, amount):
    call_procedure("PAY_BILL", {
        "customer_id": customer_id,
        "bill_type": bill_type,
        "account_number": account_number,
        "amount": amount
    })

def call_transfer_money_procedure(from_customer_id, to_customer_id, amount):
    call_procedure("TRANSFER_MONEY", {
        "from_customer_id": from_customer_id,
        "to_customer_id": to_customer_id,
        "amount": amount
    })

def call_add_money_procedure(customer_id, amount):
    call_procedure("ADD_MONEY", {
        "customer_id": customer_id,
        "amount": amount
    })
