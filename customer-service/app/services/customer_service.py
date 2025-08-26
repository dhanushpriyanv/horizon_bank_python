
from app.db import db
from app.models.customer import Customer
from app.exceptions.exceptions import CustomerNotFoundException

def create_customer(data):
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return customer

def get_customer_by_id(customer_id):
    customer = db.session.query(Customer).filter_by(id=customer_id).first()
    return customer

def get_all_customers():
    return db.session.query(Customer).all()

def update_customer(customer_id, data):
    customer = get_customer_by_id(customer_id)
    if not customer:
        raise CustomerNotFoundException(f"Customer {customer_id} not found")
    for key, value in data.items():
        setattr(customer, key, value)
    db.session.commit()
    return customer

def delete_customer(customer_id):
    customer = get_customer_by_id(customer_id)
    if not customer:
        raise CustomerNotFoundException(f"Customer {customer_id} not found")
    db.session.delete(customer)
    db.session.commit()
